"""
Unit Tests für US-01 – Flughafen erfassen (POST /airports).

Die Tests laufen isoliert mit einem In-Memory-Repository.

@see <a href="https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/1">US-01 #1</a>
@since 0.1.0
"""

from datetime import UTC, datetime
from uuid import UUID

import pytest

from app.repository import InMemoryAirportRepository, RepositoryError
from app.schemas import AirportCreate
from app.service import AirportService


def test_create_airport_returns_201_with_generated_id_and_date(client, valid_airport):
    """
    Happy Path: Ein gültiger Flughafen wird erfasst.

    Given eine gültige Eingabe (Name, Kürzel ZRH, Kapazität 85000)
    When POST /airports aufgerufen wird
    Then antwortet der Dienst mit 201, gibt die Eingabe zurück und ergänzt
    eine gültige UUID sowie ein Erstellungsdatum mit Zeitzone.

    @param client      Testclient mit leerem In-Memory-Repository
    @param valid_airport gültige Eingabedaten
    @expected HTTP 201, Felder id und created_at sind gesetzt
    """
    response = client.post("/airports", json=valid_airport)

    assert response.status_code == 201
    body = response.json()
    assert body["name"] == "Flughafen Zürich"
    assert body["code"] == "ZRH"
    assert body["capacity"] == 85000
    UUID(body["id"])  # wirft ValueError, falls keine gültige UUID
    assert datetime.fromisoformat(body["created_at"]).tzinfo is not None


def test_create_airport_normalizes_code_to_uppercase(client):
    """
    Happy Path: Kleingeschriebene Kürzel werden vereinheitlicht.

    Given das Kürzel " bsl " mit Leerzeichen und Kleinbuchstaben
    When POST /airports aufgerufen wird
    Then wird es als "BSL" gespeichert. So erkennt die Duplikatprüfung
    auch "bsl" und "BSL" als dasselbe Kürzel.

    @param client Testclient mit leerem In-Memory-Repository
    @expected HTTP 201 und code == "BSL"
    """
    response = client.post("/airports", json={"name": "EuroAirport Basel", "code": " bsl ", "capacity": 25000})

    assert response.status_code == 201
    assert response.json()["code"] == "BSL"


def test_create_airport_rejects_duplicate_code_with_409(client, valid_airport):
    """
    Sad Path: Ein Kürzel darf nur einmal vorkommen.

    Given ein bereits erfasster Flughafen mit Kürzel ZRH
    When ein zweiter Flughafen mit Kürzel "zrh" erfasst wird
    Then antwortet der Dienst mit 409 und nennt das doppelte Kürzel.

    @param client        Testclient mit leerem In-Memory-Repository
    @param valid_airport gültige Eingabedaten
    @expected HTTP 409, Fehlermeldung enthält "ZRH"
    """
    client.post("/airports", json=valid_airport)

    response = client.post("/airports", json={**valid_airport, "name": "Zürich Kopie", "code": "zrh"})

    assert response.status_code == 409
    assert "ZRH" in response.json()["detail"]
    assert response.json()["errors"][0]["field"] == "code"


@pytest.mark.parametrize(
    ("capacity", "expected_message"),
    [
        (0, "Muss grösser als 0 sein."),
        (-5, "Muss grösser als 0 sein."),
        (1_000_001, "Darf höchstens 1000000 sein."),
        ("viel", "Muss eine ganze Zahl sein."),
        (12.5, "Muss eine ganze Zahl sein."),
        (True, "Muss eine ganze Zahl sein."),
    ],
)
def test_create_airport_rejects_invalid_capacity_with_422(client, valid_airport, capacity, expected_message):
    """
    Sad Path: Ungültige Kapazitätswerte werden abgewiesen.

    Given eine sonst gültige Eingabe mit ungültiger Kapazität
    (0, negativ, über der Plausibilitätsgrenze, Text, Kommazahl, Boolean)
    When POST /airports aufgerufen wird
    Then antwortet der Dienst mit 422 und einer deutschen Meldung beim Feld capacity.

    @param client           Testclient mit leerem In-Memory-Repository
    @param valid_airport    gültige Eingabedaten als Basis
    @param capacity         ungültiger Kapazitätswert
    @param expected_message erwartete Fehlermeldung
    @expected HTTP 422, errors enthält {field: capacity, message: expected_message}
    """
    response = client.post("/airports", json={**valid_airport, "capacity": capacity})

    assert response.status_code == 422
    assert {"field": "capacity", "message": expected_message} in response.json()["errors"]


@pytest.mark.parametrize("code", ["ZR", "ZRHX", "Z1H", ""])
def test_create_airport_rejects_invalid_code_with_422(client, valid_airport, code):
    """
    Sad Path: Das Kürzel muss aus genau drei Buchstaben bestehen.

    @param client        Testclient mit leerem In-Memory-Repository
    @param valid_airport gültige Eingabedaten als Basis
    @param code          ungültiges Kürzel
    @expected HTTP 422 mit Fehler beim Feld code
    """
    response = client.post("/airports", json={**valid_airport, "code": code})

    assert response.status_code == 422
    assert response.json()["errors"][0]["field"] == "code"


def test_create_airport_rejects_missing_fields_with_422(client):
    """
    Sad Path: Fehlende Pflichtfelder werden einzeln gemeldet.

    Given ein leeres JSON-Objekt
    When POST /airports aufgerufen wird
    Then meldet der Dienst name, code und capacity als fehlende Pflichtfelder.

    @param client Testclient mit leerem In-Memory-Repository
    @expected HTTP 422 mit drei Fehlern "Pflichtfeld fehlt."
    """
    response = client.post("/airports", json={})

    assert response.status_code == 422
    fields = {e["field"] for e in response.json()["errors"] if e["message"] == "Pflichtfeld fehlt."}
    assert fields == {"name", "code", "capacity"}


def test_create_airport_returns_503_when_database_fails(client, repository, valid_airport, monkeypatch):
    """
    Sad Path: Ein Datenbankfehler wird verständlich gemeldet, ohne Interna preiszugeben.

    Given ein Repository, das beim Speichern einen technischen Fehler wirft
    When POST /airports aufgerufen wird
    Then antwortet der Dienst mit 503 und einer allgemeinen Meldung.

    @param client        Testclient
    @param repository    In-Memory-Repository, dessen add() simuliert fehlschlägt
    @param valid_airport gültige Eingabedaten
    @param monkeypatch   pytest-Hilfsmittel zum Ersetzen von add()
    @expected HTTP 503, keine SQL-Details in der Antwort
    """

    def failing_add(_airport):
        raise RepositoryError("connection refused")

    monkeypatch.setattr(repository, "add", failing_add)

    response = client.post("/airports", json=valid_airport)

    assert response.status_code == 503
    assert "connection refused" not in response.text


def test_service_sets_id_and_creation_date_from_injected_factories():
    """
    Unit Test der Geschäftslogik ohne HTTP: ID und Datum stammen vom Service.

    Given ein Service mit fester Uhr und fester ID
    When create_airport aufgerufen wird
    Then übernimmt der gespeicherte Flughafen genau diese Werte.

    @expected id und created_at entsprechen den injizierten Werten
    """
    fixed_id = UUID("00000000-0000-0000-0000-000000000001")
    fixed_time = datetime(2026, 11, 23, 8, 0, tzinfo=UTC)
    service = AirportService(InMemoryAirportRepository(), clock=lambda: fixed_time, id_factory=lambda: fixed_id)

    airport = service.create_airport(AirportCreate(name="Flughafen Genf", code="GVA", capacity=50000))

    assert airport.id == fixed_id
    assert airport.created_at == fixed_time
