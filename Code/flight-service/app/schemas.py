"""Ein- und Ausgabeschemas der REST-API (Pydantic).

Die Prüfungen, die keine anderen Dienste brauchen (Format, UTC, Reihenfolge
der Zeiten, verschiedene Flughäfen), laufen hier. Erst danach fragt der
Service den Flughafenservice an.
"""

import re
from datetime import datetime, timedelta
from uuid import UUID

from pydantic import AwareDatetime, BaseModel, ConfigDict, Field, field_validator, model_validator

AIRPORT_CODE_PATTERN = re.compile(r"^[A-Z]{3}$")


def _normalize_code(value: str) -> str:
    normalized = value.strip().upper()
    if not AIRPORT_CODE_PATTERN.match(normalized):
        raise ValueError("Das Kürzel muss aus genau 3 Buchstaben bestehen (IATA, z. B. ZRH).")
    return normalized


class FlightCreate(BaseModel):
    """Eingabe für US-03: einen Flug erfassen."""

    model_config = ConfigDict(extra="forbid")

    departure_airport: str = Field(examples=["ZRH"])
    arrival_airport: str = Field(examples=["GVA"])
    departure_time: AwareDatetime = Field(examples=["2026-12-01T08:30:00Z"])
    arrival_time: AwareDatetime = Field(examples=["2026-12-01T09:25:00Z"])
    aircraft_type: str = Field(min_length=2, max_length=50, examples=["Boeing 727"])

    @field_validator("departure_airport", "arrival_airport")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        return _normalize_code(value)

    @field_validator("departure_time", "arrival_time")
    @classmethod
    def require_utc(cls, value: datetime) -> datetime:
        # Die Story verlangt UTC. Andere Zeitzonen weisen wir ab, statt still umzurechnen.
        if value.utcoffset() != timedelta(0):
            raise ValueError("Zeitangabe muss in UTC sein (Endung Z oder +00:00).")
        return value

    @field_validator("aircraft_type")
    @classmethod
    def strip_aircraft_type(cls, value: str) -> str:
        stripped = value.strip()
        if len(stripped) < 2:
            raise ValueError("Der Flugzeugtyp muss mindestens 2 Zeichen enthalten.")
        return stripped

    @model_validator(mode="after")
    def check_route_and_times(self) -> "FlightCreate":
        if self.departure_airport == self.arrival_airport:
            raise ValueError("Abflug- und Ankunftsflughafen müssen verschieden sein.")
        if self.arrival_time <= self.departure_time:
            raise ValueError("Der Landezeitpunkt muss nach dem Startzeitpunkt liegen.")
        return self


class FlightRead(BaseModel):
    """Ausgabe eines Flugs mit allen Feldern."""

    model_config = ConfigDict(from_attributes=True)

    id: UUID
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    aircraft_type: str
    created_at: datetime


class ErrorResponse(BaseModel):
    """Einheitliches Fehlerformat aller Endpoints."""

    detail: str
    errors: list[dict] = []
