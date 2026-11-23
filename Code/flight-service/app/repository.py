"""Datenzugriff des Flugservice (Repository-Muster, eigene Datenbank)."""

from typing import Protocol

from sqlalchemy import Column, DateTime, MetaData, String, Table, Uuid, insert
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from app.models import Flight


class RepositoryError(Exception):
    """Die Datenbank ist nicht erreichbar oder das Speichern ist fehlgeschlagen."""


class FlightRepository(Protocol):
    """Schnittstelle für die Speicherung von Flügen."""

    def add(self, flight: Flight) -> Flight: ...


class InMemoryFlightRepository:
    """Speichert Flüge in einer Liste. Nur für Tests."""

    def __init__(self) -> None:
        self.flights: list[Flight] = []

    def add(self, flight: Flight) -> Flight:
        self.flights.append(flight)
        return flight


metadata = MetaData()

#: Tabelle ``flights``. Die Flughafenkürzel sind bewusst kein Fremdschlüssel,
#: weil die Flughäfen in der Datenbank eines anderen Dienstes liegen.
flights_table = Table(
    "flights",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("departure_airport", String(3), nullable=False),
    Column("arrival_airport", String(3), nullable=False),
    Column("departure_time", DateTime(timezone=True), nullable=False),
    Column("arrival_time", DateTime(timezone=True), nullable=False),
    Column("aircraft_type", String(50), nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)


class SqlAlchemyFlightRepository:
    """Speichert Flüge in PostgreSQL."""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def create_schema(self) -> None:
        metadata.create_all(self._engine)

    def add(self, flight: Flight) -> Flight:
        try:
            with self._engine.begin() as conn:
                conn.execute(insert(flights_table).values(**flight.__dict__))
        except SQLAlchemyError as exc:
            raise RepositoryError(str(exc)) from exc
        return flight
