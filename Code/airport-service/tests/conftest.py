"""Gemeinsame Test-Fixtures des Flughafenservice.

Alle Unit Tests verwenden ein ``InMemoryAirportRepository``. Sie brauchen
deshalb weder PostgreSQL noch Docker und laufen auf jedem Rechner.
"""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app
from app.repository import InMemoryAirportRepository


@pytest.fixture
def repository() -> InMemoryAirportRepository:
    """
    Liefert ein leeres Repository im Arbeitsspeicher.

    @return neues {@code InMemoryAirportRepository}, pro Test frisch erzeugt
    """
    return InMemoryAirportRepository()


@pytest.fixture
def client(repository: InMemoryAirportRepository):
    """
    Liefert einen HTTP-Testclient für die API ohne Datenbankverbindung.

    @param repository leeres In-Memory-Repository, das die App verwendet
    @return {@code TestClient}, der Anfragen direkt an die App schickt
    """
    with TestClient(create_app(repository=repository)) as test_client:
        yield test_client


@pytest.fixture
def valid_airport() -> dict:
    """
    Liefert eine gültige Eingabe für POST /airports.

    @return JSON-Daten für den Flughafen Zürich
    """
    return {"name": "Flughafen Zürich", "code": "ZRH", "capacity": 85000}
