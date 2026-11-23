"""Domänenmodell des Flughafenservice.

Das Modell ist unabhängig von FastAPI und der Datenbank. Dadurch lassen sich
Service und Repository getrennt testen.
"""

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass(frozen=True)
class Airport:
    """Ein erfasster Flughafen."""

    id: UUID
    name: str
    code: str
    capacity: int
    created_at: datetime
