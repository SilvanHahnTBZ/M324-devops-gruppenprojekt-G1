"""Datenzugriff des Flughafenservice (Repository-Muster).

``AirportRepository`` beschreibt die Schnittstelle. Es gibt zwei Umsetzungen:

* ``SqlAlchemyAirportRepository`` für PostgreSQL im Betrieb,
* ``InMemoryAirportRepository`` für isolierte Unit Tests ohne Datenbank.
"""

from typing import Protocol

from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, Uuid, insert, select
from sqlalchemy.engine import Engine
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from app.models import Airport


class DuplicateAirportCodeError(Exception):
    """Das Kürzel ist bereits einem anderen Flughafen zugeordnet."""

    def __init__(self, code: str) -> None:
        super().__init__(code)
        self.code = code


class RepositoryError(Exception):
    """Die Datenbank ist nicht erreichbar oder die Abfrage ist fehlgeschlagen."""


class AirportRepository(Protocol):
    """Schnittstelle für die Speicherung von Flughäfen."""

    def add(self, airport: Airport) -> Airport:
        """Speichert einen Flughafen.

        Raises:
            DuplicateAirportCodeError: wenn das Kürzel schon existiert.
            RepositoryError: bei technischen Fehlern.
        """
        ...

    def list_all(self) -> list[Airport]:
        """Liefert alle Flughäfen, sortiert nach Kürzel.

        Raises:
            RepositoryError: bei technischen Fehlern.
        """
        ...


class InMemoryAirportRepository:
    """Speichert Flughäfen in einem Dictionary. Nur für Tests und lokale Versuche."""

    def __init__(self) -> None:
        self._by_code: dict[str, Airport] = {}

    def add(self, airport: Airport) -> Airport:
        if airport.code in self._by_code:
            raise DuplicateAirportCodeError(airport.code)
        self._by_code[airport.code] = airport
        return airport

    def list_all(self) -> list[Airport]:
        return [self._by_code[code] for code in sorted(self._by_code)]


metadata = MetaData()

#: Tabelle ``airports``. Der UNIQUE-Constraint auf ``code`` verhindert
#: doppelte Kürzel auch bei gleichzeitigen Anfragen.
airports_table = Table(
    "airports",
    metadata,
    Column("id", Uuid, primary_key=True),
    Column("name", String(100), nullable=False),
    Column("code", String(3), nullable=False, unique=True),
    Column("capacity", Integer, nullable=False),
    Column("created_at", DateTime(timezone=True), nullable=False),
)


class SqlAlchemyAirportRepository:
    """Speichert Flughäfen in einer relationalen Datenbank (PostgreSQL)."""

    def __init__(self, engine: Engine) -> None:
        self._engine = engine

    def create_schema(self) -> None:
        """Legt die Tabelle an, falls sie fehlt (v1 ohne Migrationstool)."""
        metadata.create_all(self._engine)

    def add(self, airport: Airport) -> Airport:
        try:
            with self._engine.begin() as conn:
                conn.execute(
                    insert(airports_table).values(
                        id=airport.id,
                        name=airport.name,
                        code=airport.code,
                        capacity=airport.capacity,
                        created_at=airport.created_at,
                    )
                )
        except IntegrityError as exc:
            raise DuplicateAirportCodeError(airport.code) from exc
        except SQLAlchemyError as exc:
            raise RepositoryError(str(exc)) from exc
        return airport

    def list_all(self) -> list[Airport]:
        # Eine einzige Abfrage für alle Einträge (kein N+1). Sortierung in der DB.
        try:
            with self._engine.connect() as conn:
                rows = conn.execute(select(airports_table).order_by(airports_table.c.code)).mappings().all()
        except SQLAlchemyError as exc:
            raise RepositoryError(str(exc)) from exc
        return [Airport(**row) for row in rows]
