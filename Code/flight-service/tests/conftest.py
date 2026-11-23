"""Gemeinsame Test-Fixtures des Flugservice.

Die Unit Tests brauchen weder Datenbank noch laufenden Flughafenservice:
``FakeAirportClient`` simuliert den Flughafenservice, ``InMemoryFlightRepository``
ersetzt PostgreSQL.
"""

import pytest
from fastapi.testclient import TestClient

from app.airport_client import AirportServiceUnavailableError
from app.main import create_app
from app.repository import InMemoryFlightRepository


class FakeAirportClient:
    """
    Simulierter Flughafenservice für Unit Tests.

    Zählt die Aufrufe, damit Tests prüfen können, ob der Flughafenservice
    überhaupt angefragt wurde.
    """

    def __init__(self, codes: set[str] | None = None, available: bool = True) -> None:
        self.codes = codes if codes is not None else {"ZRH", "GVA", "BSL"}
        self.available = available
        self.calls = 0

    def get_airport_codes(self) -> set[str]:
        self.calls += 1
        if not self.available:
            raise AirportServiceUnavailableError("simuliert: Flughafenservice down")
        return set(self.codes)


@pytest.fixture
def airport_client() -> FakeAirportClient:
    """
    Liefert einen simulierten Flughafenservice mit ZRH, GVA und BSL.

    @return erreichbarer {@code FakeAirportClient}
    """
    return FakeAirportClient()


@pytest.fixture
def repository() -> InMemoryFlightRepository:
    """
    Liefert ein leeres Flug-Repository im Arbeitsspeicher.

    @return neues {@code InMemoryFlightRepository}
    """
    return InMemoryFlightRepository()


@pytest.fixture
def client(repository, airport_client):
    """
    Liefert einen HTTP-Testclient für den Flugservice ohne externe Abhängigkeiten.

    @param repository     In-Memory-Repository
    @param airport_client simulierter Flughafenservice
    @return {@code TestClient} für die App
    """
    with TestClient(create_app(repository=repository, airport_client=airport_client)) as test_client:
        yield test_client


@pytest.fixture
def valid_flight() -> dict:
    """
    Liefert eine gültige Eingabe für POST /flights (ZRH → GVA, 55 Minuten).

    @return JSON-Daten eines gültigen Flugs
    """
    return {
        "departure_airport": "ZRH",
        "arrival_airport": "GVA",
        "departure_time": "2026-12-01T08:30:00Z",
        "arrival_time": "2026-12-01T09:25:00Z",
        "aircraft_type": "Boeing 727",
    }
