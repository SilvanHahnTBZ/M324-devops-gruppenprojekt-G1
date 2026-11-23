"""
End-to-End-Test über beide laufenden Dienste (geplant für die CI in P3).

Voraussetzung: beide Dienste laufen, z. B. mit
``docker compose -f Code/docker-compose.yml up --build``.
Ohne ``E2E_AIRPORT_URL`` und ``E2E_FLIGHT_URL`` wird der Test übersprungen,
damit lokale Unit-Test-Läufe nicht davon abhängen.

@see <a href="https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/15">P3 #15</a>
@since 0.1.0
"""

import os
import random
import string

import httpx
import pytest

AIRPORT_URL = os.getenv("E2E_AIRPORT_URL")
FLIGHT_URL = os.getenv("E2E_FLIGHT_URL")

pytestmark = pytest.mark.skipif(
    not (AIRPORT_URL and FLIGHT_URL), reason="E2E_AIRPORT_URL und E2E_FLIGHT_URL nicht gesetzt"
)


def _random_code() -> str:
    return "".join(random.choices(string.ascii_uppercase, k=3))


def test_flight_service_validates_airports_via_airport_service():
    """
    Der Flugservice prüft Flughäfen über die echte API des Flughafenservice.

    Given zwei neu erfasste Flughäfen im laufenden Flughafenservice
    When ein Flug zwischen ihnen und danach einer zu einem unbekannten Kürzel erfasst wird
    Then wird der erste mit 201 gespeichert und der zweite mit 422 abgewiesen.

    Grenze: Zufällige Kürzel können mit bestehenden Daten kollidieren;
    in der CI startet die Datenbank deshalb leer.

    @expected 201 für bekannte Flughäfen, 422 für unbekannten Flughafen
    """
    departure, arrival = _random_code(), _random_code()
    while arrival == departure:
        arrival = _random_code()
    for code in (departure, arrival):
        created = httpx.post(f"{AIRPORT_URL}/airports", json={"name": f"E2E {code}", "code": code, "capacity": 1000})
        assert created.status_code in (201, 409)

    flight = {
        "departure_airport": departure,
        "arrival_airport": arrival,
        "departure_time": "2026-12-01T08:30:00Z",
        "arrival_time": "2026-12-01T09:25:00Z",
        "aircraft_type": "Airbus A320",
    }
    assert httpx.post(f"{FLIGHT_URL}/flights", json=flight).status_code == 201

    known = {a["code"] for a in httpx.get(f"{AIRPORT_URL}/airports").json()["items"]}
    unknown = next(c for c in (_random_code() for _ in range(100)) if c not in known)
    assert httpx.post(f"{FLIGHT_URL}/flights", json={**flight, "arrival_airport": unknown}).status_code == 422
