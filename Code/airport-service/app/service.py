"""Geschäftslogik des Flughafenservice.

Der Service erzeugt ID und Erstellungsdatum. Uhr und ID-Generator werden
übergeben, damit Tests feste Werte verwenden können.
"""

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.models import Airport
from app.repository import AirportRepository
from app.schemas import AirportCreate


def utc_now() -> datetime:
    return datetime.now(UTC)


class AirportService:
    """Anwendungsfälle rund um Flughäfen."""

    def __init__(
        self,
        repository: AirportRepository,
        clock: Callable[[], datetime] = utc_now,
        id_factory: Callable[[], UUID] = uuid4,
    ) -> None:
        self._repository = repository
        self._clock = clock
        self._id_factory = id_factory

    def create_airport(self, data: AirportCreate) -> Airport:
        """US-01: erfasst einen Flughafen mit neuer ID und aktuellem UTC-Datum."""
        airport = Airport(
            id=self._id_factory(),
            name=data.name,
            code=data.code,
            capacity=data.capacity,
            created_at=self._clock(),
        )
        return self._repository.add(airport)

    def list_airports(self) -> list[Airport]:
        """US-02: liefert alle erfassten Flughäfen, sortiert nach Kürzel."""
        return self._repository.list_all()
