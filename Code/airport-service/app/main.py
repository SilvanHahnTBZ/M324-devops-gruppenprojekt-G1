"""REST-API des Flughafenservice.

Start lokal: ``uvicorn app.main:app --reload --port 8001``
"""

import os
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from sqlalchemy import create_engine

from app import __version__
from app.errors import validation_exception_handler
from app.repository import (
    AirportRepository,
    DuplicateAirportCodeError,
    RepositoryError,
    SqlAlchemyAirportRepository,
)
from app.schemas import AirportCreate, AirportList, AirportRead, ErrorResponse
from app.service import AirportService

DEFAULT_DATABASE_URL = "postgresql+psycopg://airport:airport@localhost:5433/airports"


def create_app(repository: AirportRepository | None = None) -> FastAPI:
    """Erstellt die Anwendung.

    Args:
        repository: Optionales Repository. Tests übergeben ein
            ``InMemoryAirportRepository``; ohne Angabe wird PostgreSQL
            über die Umgebungsvariable ``DATABASE_URL`` verwendet.
    """

    @asynccontextmanager
    async def lifespan(app: FastAPI):
        if repository is None:
            engine = create_engine(os.getenv("DATABASE_URL", DEFAULT_DATABASE_URL), pool_pre_ping=True)
            sql_repository = SqlAlchemyAirportRepository(engine)
            sql_repository.create_schema()
            app.state.repository = sql_repository
            yield
            engine.dispose()
        else:
            app.state.repository = repository
            yield

    app = FastAPI(title="Flughafenservice", version=__version__, lifespan=lifespan)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)

    def get_service(request: Request) -> AirportService:
        return AirportService(request.app.state.repository)

    ServiceDep = Annotated[AirportService, Depends(get_service)]

    @app.get("/health", tags=["Betrieb"])
    def health() -> dict:
        """Einfacher Lebenszeichen-Check für Betrieb und Smoke Tests."""
        return {"status": "ok", "version": __version__}

    @app.post(
        "/airports",
        status_code=201,
        response_model=AirportRead,
        tags=["Flughäfen"],
        responses={409: {"model": ErrorResponse}, 422: {"model": ErrorResponse}, 503: {"model": ErrorResponse}},
    )
    def create_airport(data: AirportCreate, service: ServiceDep):
        """US-01: Flughafen erfassen."""
        try:
            return service.create_airport(data)
        except DuplicateAirportCodeError as exc:
            return JSONResponse(
                status_code=409,
                content={
                    "detail": f"Das Kürzel '{exc.code}' ist bereits erfasst. Bitte ein anderes Kürzel wählen.",
                    "errors": [{"field": "code", "message": "Kürzel bereits vorhanden."}],
                },
            )
        except RepositoryError:
            return JSONResponse(
                status_code=503,
                content={"detail": "Der Flughafen konnte nicht gespeichert werden. Bitte später erneut versuchen."},
            )

    @app.get(
        "/airports",
        response_model=AirportList,
        tags=["Flughäfen"],
        responses={503: {"model": ErrorResponse}},
    )
    def list_airports(service: ServiceDep):
        """US-02: Alle Flughäfen auslesen.

        Ein leerer Bestand ist kein technischer Fehler: Antwort 200 mit
        ``count = 0`` und einem Hinweis. So kann der Flugservice die Liste
        immer gleich auswerten.
        """
        try:
            airports = service.list_airports()
        except RepositoryError:
            return JSONResponse(
                status_code=503,
                content={"detail": "Die Flughäfen konnten nicht geladen werden. Bitte später erneut versuchen."},
            )
        message = None if airports else "Es sind noch keine Flughäfen erfasst."
        return AirportList(count=len(airports), items=airports, message=message)

    return app


app = create_app()
