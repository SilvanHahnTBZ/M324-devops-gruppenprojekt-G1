"""Domänenmodell des Flugservice (unabhängig von FastAPI und Datenbank)."""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Flight:
    """Ein erfasster Flug. Alle Zeitangaben sind in UTC."""

    id: UUID
    departure_airport: str
    arrival_airport: str
    departure_time: datetime
    arrival_time: datetime
    aircraft_type: str
    created_at: datetime
