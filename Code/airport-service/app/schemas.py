"""Ein- und Ausgabeschemas der REST-API (Pydantic).

Hier liegt die Eingabevalidierung. Die Fehlermeldungen sind auf Deutsch,
damit der Administrator seine Eingabe direkt korrigieren kann.
"""

import re
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator

#: IATA-Flughafenkürzel: genau drei Buchstaben, z. B. ZRH.
AIRPORT_CODE_PATTERN = re.compile(r"^[A-Z]{3}$")

#: Plausibilitätsgrenze für Passagiere pro Tag. Die grössten Flughäfen
#: der Welt liegen deutlich darunter.
MAX_CAPACITY = 1_000_000


class AirportCreate(BaseModel):
    """Eingabe für US-01: einen Flughafen erfassen."""

    model_config = ConfigDict(extra="forbid")

    name: str = Field(min_length=2, max_length=100, examples=["Flughafen Zürich"])
    code: str = Field(examples=["ZRH"])
    capacity: int = Field(strict=True, gt=0, le=MAX_CAPACITY, examples=[85000])

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        stripped = value.strip()
        if len(stripped) < 2:
            raise ValueError("Der Name muss mindestens 2 Zeichen enthalten.")
        return stripped

    @field_validator("code")
    @classmethod
    def normalize_code(cls, value: str) -> str:
        normalized = value.strip().upper()
        if not AIRPORT_CODE_PATTERN.match(normalized):
            raise ValueError("Das Kürzel muss aus genau 3 Buchstaben bestehen (IATA, z. B. ZRH).")
        return normalized


class AirportRead(BaseModel):
    """Ausgabe eines Flughafens mit allen Feldern."""

    id: UUID
    name: str
    code: str
    capacity: int
    created_at: datetime


class ErrorResponse(BaseModel):
    """Einheitliches Fehlerformat aller Endpoints."""

    detail: str
    errors: list[dict] = []
