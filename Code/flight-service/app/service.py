"""Geschäftslogik des Flugservice."""

from collections.abc import Callable
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.airport_client import AirportClient
from app.models import Flight
from app.repository import FlightRepository
from app.schemas import FlightCreate


class UnknownAirportError(Exception):
    """Mindestens ein Flughafen ist im Flughafenservice nicht erfasst."""

    def __init__(self, fields: dict[str, str]) -> None:
        super().__init__(fields)
        #: Feldname -> unbekanntes Kürzel, z. B. {"arrival_airport": "XXX"}
        self.fields = fields


def utc_now() -> datetime:
    return datetime.now(UTC)


class FlightService:
    """Anwendungsfälle rund um Flüge."""

    def __init__(
        self,
        repository: FlightRepository,
        airport_client: AirportClient,
        clock: Callable[[], datetime] = utc_now,
        id_factory: Callable[[], UUID] = uuid4,
    ) -> None:
        self._repository = repository
        self._airport_client = airport_client
        self._clock = clock
        self._id_factory = id_factory

    def create_flight(self, data: FlightCreate) -> Flight:
        """US-03: prüft beide Flughäfen beim Flughafenservice und speichert den Flug.

        Raises:
            UnknownAirportError: wenn ein Kürzel nicht erfasst ist.
            AirportServiceUnavailableError: wenn der Flughafenservice nicht antwortet.
        """
        known_codes = self._airport_client.get_airport_codes()
        unknown = {
            field: code
            for field, code in (
                ("departure_airport", data.departure_airport),
                ("arrival_airport", data.arrival_airport),
            )
            if code not in known_codes
        }
        if unknown:
            raise UnknownAirportError(unknown)

        flight = Flight(
            id=self._id_factory(),
            departure_airport=data.departure_airport,
            arrival_airport=data.arrival_airport,
            departure_time=data.departure_time,
            arrival_time=data.arrival_time,
            aircraft_type=data.aircraft_type,
            created_at=self._clock(),
        )
        return self._repository.add(flight)
