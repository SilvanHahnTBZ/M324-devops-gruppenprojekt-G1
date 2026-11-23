"""REST-API des Flugservice.

Start lokal: ``uvicorn app.main:app --reload --port 8002``
"""

import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine

from app import __version__
from app.airport_client import AirportClient, AirportServiceUnavailableError, HttpAirportClient
from app.errors import validation_exception_handler
from app.repository import FlightRepository, RepositoryError, SqlAlchemyFlightRepository
from app.schemas import ErrorResponse, FlightCreate, FlightRead
from app.service import FlightService, UnknownAirportError

DEFAULT_DATABASE_URL = "postgresql+psycopg://flight:flight@localhost:5434/flights"
DEFAULT_AIRPORT_SERVICE_URL = "http://localhost:8001"


def create_app(repository: FlightRepository | None = None, airport_client: AirportClient | None = None) -> FastAPI:
    """Erstellt die Anwendung.

    Args:
        repository: Optional; Tests übergeben ein ``InMemoryFlightRepository``.
            Sonst PostgreSQL über ``DATABASE_URL``.
        airport_client: Optional; Tests übergeben einen simulierten Flughafenservice.
            Sonst HTTP-Aufruf an ``AIRPORT_SERVICE_URL``.
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        engine = None
        if repository is None:
            engine = create_engine(os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL), pool_pre_ping=True)
            sql_repository = SqlAlchemyFlightRepository(engine)
            sql_repository.create_schema()
            app.state.repository = sql_repository
        else:
            app.state.repository = repository
        app.state.airport_client = airport_client or HttpAirportClient(
            os.getenv("AIRPORT_SERVICE_URL", DEFAULT_AIRPORT_SERVICE_URL)
        )
        yield
        if engine is not None:
            engine.dispose()

    app = FastAPI(title="Flugservice", version=__version__, lifespan=lifespan)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    def get_service(request: Request) -> FlightService:
        return FlightService(request.app.state.repository, request.app.state.airport_client)

    ServiceDep = Annotated[FlightService, Depends(get_service)]

    @app.get("/health", tags=["Betrieb"])
    def health() -> dict:
        """Einfacher Lebenszeichen-Check für Betrieb und Smoke Tests."""
        return {"status": "ok", "version": __version__}

    @app.post(
        "/flights",
        status_code=201,
        response_model=FlightRead,
        tags=["Flüge"],
        responses={422: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
    )
    def create_flight(data: FlightCreate, service: ServiceDep):
        """US-03: Flug erfassen. Die Flughäfen werden über GET /airports des Flughafenservice geprüft."""
        try:
            return service.create_flight(data)
        except UnknownAirportError as exc:
            codes = ", ".join(sorted(set(exc.fields.values())))
            return JSONResponse(
                status_code=422,
                content={
                    "detail": f"Unbekannter Flughafen: {codes}. Bitte zuerst im Flughafenservice erfassen.",
                    "errors": [
                        {"field": field, "message": f"Flughafen '{code}' ist nicht erfasst."}
                        for field, code in exc.fields.items()
                    ],
                },
            )
        except AirportServiceUnavailableError:
            return JSONResponse(
                status_code=503,
                content={"detail": "Der Flughafenservice ist nicht erreichbar. Der Flug kann nicht geprüft werden."},
            )
        except RepositoryError:
            return JSONResponse(
                status_code=503,
                content={"detail": "Der Flug konnte nicht gespeichert werden. Bitte später erneut versuchen."},
            )

    return app


app = create_app()
