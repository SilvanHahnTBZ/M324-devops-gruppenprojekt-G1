"""
Unit Tests für US-03 – Flug erfassen (POST /flights).

Isoliert: Der Flughafenservice ist durch {@code FakeAirportClient} simuliert,
die Datenbank durch {@code InMemoryFlightRepository}.

@see <a href="https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/3">US-03 #3</a>
@since 0.1.0
"""

from datetime import datetime
from uuid import UUID

import pytest


def test_create_flight_returns_201_and_stores_flight(client, repository, airport_client, valid_flight):
    """
    Happy Path: Ein gültiger Flug zwischen zwei erfassten Flughäfen wird gespeichert.

    Given ZRH und GVA sind im (simulierten) Flughafenservice erfasst
    When POST /flights mit gültigen UTC-Zeiten aufgerufen wird
    Then antwortet der Dienst mit 201, liefert ID und Erstellungsdatum,
    speichert genau einen Flug und hat den Flughafenservice genau einmal gefragt.

    @param client         Testclient
    @param repository     In-Memory-Repository zur Kontrolle der Speicherung
    @param airport_client simulierter Flughafenservice (ZRH, GVA, BSL)
    @param valid_flight   gültige Eingabedaten
    @expected HTTP 201, ein gespeicherter Flug, ein Aufruf des Flughafenservice
    """
    response = client.post("/flights", json=valid_flight)

    assert response.status_code == 201
    body = response.json()
    UUID(body["id"])
    assert body["departure_airport"] == "ZRH"
    assert body["arrival_airport"] == "GVA"
    assert body["aircraft_type"] == "Boeing 727"
    assert datetime.fromisoformat(body["departure_time"]) == datetime.fromisoformat("2026-12-01T08:30:00+00:00")
    assert len(repository.flights) == 1
    assert airport_client.calls == 1


def test_create_flight_accepts_lowercase_codes(client, valid_flight):
    """
    Happy Path: Kürzel in Kleinbuchstaben werden vor der Prüfung vereinheitlicht.

    @param client       Testclient
    @param valid_flight gültige Eingabedaten als Basis
    @expected HTTP 201, Kürzel in Grossbuchstaben gespeichert
    """
    response = client.post("/flights", json={**valid_flight, "departure_airport": "zrh", "arrival_airport": "bsl"})

    assert response.status_code == 201
    assert (response.json()["departure_airport"], response.json()["arrival_airport"]) == ("ZRH", "BSL")


@pytest.mark.parametrize(
    ("field", "code"),
    [("departure_airport", "LHR"), ("arrival_airport", "XXX")],
)
def test_create_flight_rejects_unknown_airport_with_422(client, repository, valid_flight, field, code):
    """
    Sad Path: Ein Flughafen, den der Flughafenservice nicht kennt, wird abgewiesen.

    Given der Flughafenservice kennt nur ZRH, GVA und BSL
    When ein Flug mit unbekanntem Abflug- oder Ankunftsflughafen erfasst wird
    Then antwortet der Dienst mit 422, nennt Feld und Kürzel und speichert nichts.

    @param client       Testclient
    @param repository   In-Memory-Repository, muss leer bleiben
    @param valid_flight gültige Eingabedaten als Basis
    @param field        Feld mit dem unbekannten Kürzel
    @param code         unbekanntes Kürzel
    @expected HTTP 422, errors == [{field, "Flughafen '<code>' ist nicht erfasst."}]
    """
    response = client.post("/flights", json={**valid_flight, field: code})

    assert response.status_code == 422
    assert response.json()["errors"] == [{"field": field, "message": f"Flughafen '{code}' ist nicht erfasst."}]
    assert repository.flights == []


def test_create_flight_rejects_identical_airports_without_calling_airport_service(client, airport_client, valid_flight):
    """
    Sad Path: Abflug- und Ankunftsflughafen dürfen nicht identisch sein.

    Die Prüfung findet schon bei der Eingabevalidierung statt. Der
    Flughafenservice wird deshalb gar nicht angefragt.

    @param client         Testclient
    @param airport_client simulierter Flughafenservice, zählt Aufrufe
    @param valid_flight   gültige Eingabedaten als Basis
    @expected HTTP 422 mit Hinweis "verschieden", 0 Aufrufe des Flughafenservice
    """
    response = client.post("/flights", json={**valid_flight, "arrival_airport": "zrh"})

    assert response.status_code == 422
    assert "verschieden" in response.json()["errors"][0]["message"]
    assert airport_client.calls == 0


@pytest.mark.parametrize(
    "arrival_time",
    ["2026-12-01T08:30:00Z", "2026-12-01T07:00:00Z"],
    ids=["landung-gleich-start", "landung-vor-start"],
)
def test_create_flight_rejects_arrival_not_after_departure(client, valid_flight, arrival_time):
    """
    Sad Path: Die Landung muss nach dem Start liegen (Grenzfall: gleiche Zeit).

    @param client       Testclient
    @param valid_flight gültige Eingabedaten, Start 08:30 UTC
    @param arrival_time Landezeit gleich oder vor dem Start
    @expected HTTP 422 mit Meldung zum Landezeitpunkt
    """
    response = client.post("/flights", json={**valid_flight, "arrival_time": arrival_time})

    assert response.status_code == 422
    assert response.json()["errors"][0]["message"] == "Der Landezeitpunkt muss nach dem Startzeitpunkt liegen."


@pytest.mark.parametrize(
    ("departure_time", "expected_start"),
    [
        ("01.12.2026 08:30", "Ungültiges Datumsformat"),
        ("2026-13-01T08:30:00Z", "Ungültiges Datumsformat"),
        ("2026-12-01T08:30:00", "Zeitangabe ohne Zeitzone"),
        ("2026-12-01T09:30:00+01:00", "Zeitangabe muss in UTC sein"),
    ],
    ids=["schweizer-format", "monat-13", "ohne-zeitzone", "nicht-utc"],
)
def test_create_flight_rejects_invalid_time_formats(client, valid_flight, departure_time, expected_start):
    """
    Sad Path: Ungültige Datums- und Zeitformate führen zu einer klaren Meldung.

    @param client         Testclient
    @param valid_flight   gültige Eingabedaten als Basis
    @param departure_time ungültige Startzeit
    @param expected_start erwarteter Anfang der Fehlermeldung
    @expected HTTP 422, Fehler beim Feld departure_time
    """
    response = client.post("/flights", json={**valid_flight, "departure_time": departure_time})

    assert response.status_code == 422
    error = response.json()["errors"][0]
    assert error["field"] == "departure_time"
    assert error["message"].startswith(expected_start)


def test_create_flight_returns_503_when_airport_service_is_down(client, repository, airport_client, valid_flight):
    """
    Sad Path: Ist der Flughafenservice nicht erreichbar, wird kein Flug ungeprüft gespeichert.

    @param client         Testclient
    @param repository     In-Memory-Repository, muss leer bleiben
    @param airport_client simulierter Flughafenservice, auf "nicht erreichbar" gesetzt
    @param valid_flight   gültige Eingabedaten
    @expected HTTP 503 und kein gespeicherter Flug
    """
    airport_client.available = False

    response = client.post("/flights", json=valid_flight)

    assert response.status_code == 503
    assert "Flughafenservice" in response.json()["detail"]
    assert repository.flights == []
