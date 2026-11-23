"""
Unit Tests für US-02 – Alle Flughäfen auslesen (GET /airports).

Die Tests laufen isoliert mit einem In-Memory-Repository.

@see <a href="https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/2">US-02 #2</a>
@since 0.1.0
"""

from datetime import UTC, datetime
from uuid import uuid4

from app.models import Airport
from app.repository import RepositoryError

EXPECTED_FIELDS = {"id", "name", "code", "capacity", "created_at"}


def test_list_airports_returns_all_airports_with_complete_fields(client):
    """
    Happy Path: Mehrere erfasste Flughäfen werden vollständig geliefert.

    Given zwei über POST /airports erfasste Flughäfen
    When GET /airports aufgerufen wird
    Then enthält die Antwort beide Einträge mit allen fünf Feldern,
    sortiert nach Kürzel, und count == 2.

    @param client Testclient mit leerem In-Memory-Repository
    @expected HTTP 200, count 2, Felder id, name, code, capacity, created_at
    """
    client.post("/airports", json={"name": "Flughafen Zürich", "code": "ZRH", "capacity": 85000})
    client.post("/airports", json={"name": "EuroAirport Basel", "code": "BSL", "capacity": 25000})

    response = client.get("/airports")

    assert response.status_code == 200
    body = response.json()
    assert body["count"] == 2
    assert body["message"] is None
    assert [a["code"] for a in body["items"]] == ["BSL", "ZRH"]
    for airport in body["items"]:
        assert set(airport) == EXPECTED_FIELDS


def test_list_airports_returns_created_airport_unchanged(client):
    """
    Happy Path: Ein erfasster Flughafen erscheint unverändert in der Übersicht
    (Abnahmekriterium US-01 "danach in der Übersicht abrufbar").

    @param client Testclient mit leerem In-Memory-Repository
    @expected der Eintrag aus GET /airports ist identisch mit der Antwort von POST
    """
    created = client.post("/airports", json={"name": "Flughafen Genf", "code": "GVA", "capacity": 50000}).json()

    items = client.get("/airports").json()["items"]

    assert items == [created]


def test_list_airports_handles_many_entries(client, repository):
    """
    Happy Path mit grossem Datenbestand: 1000 Einträge werden vollständig
    und korrekt sortiert geliefert.

    Grenze: Der Test prüft die Korrektheit, nicht die Antwortzeit einer
    echten PostgreSQL-Datenbank. Diese gehört in einen Last- oder Integrationstest.

    @param client     Testclient
    @param repository In-Memory-Repository, direkt mit 1000 Flughäfen befüllt
    @expected count 1000, Kürzel aufsteigend sortiert
    """
    letters = "ABCDEFGHIJ"
    codes = [a + b + c for a in letters for b in letters for c in letters]
    for code in reversed(codes):
        repository.add(
            Airport(id=uuid4(), name=f"Flughafen {code}", code=code, capacity=1000, created_at=datetime.now(UTC))
        )

    body = client.get("/airports").json()

    assert body["count"] == 1000
    assert [a["code"] for a in body["items"]] == sorted(codes)


def test_list_airports_reports_empty_database_with_message(client):
    """
    Sad Path: Ohne erfasste Flughäfen gibt es eine verständliche Meldung.

    Entscheid: HTTP 200 mit leerer Liste statt 404, weil ein leerer Bestand
    ein gültiger Zustand ist. Der Flugservice kann so immer gleich auswerten.

    @param client Testclient mit leerem In-Memory-Repository
    @expected HTTP 200, count 0, items leer, message gesetzt
    """
    response = client.get("/airports")

    assert response.status_code == 200
    assert response.json() == {"count": 0, "items": [], "message": "Es sind noch keine Flughäfen erfasst."}


def test_list_airports_returns_503_when_query_fails(client, repository, monkeypatch):
    """
    Sad Path: Eine fehlgeschlagene Datenbankabfrage wird klar gemeldet.

    Given ein Repository, dessen Abfrage einen technischen Fehler wirft
    When GET /airports aufgerufen wird
    Then antwortet der Dienst mit 503 und ohne interne Fehlerdetails.

    @param client      Testclient
    @param repository  In-Memory-Repository, dessen list_all() simuliert fehlschlägt
    @param monkeypatch pytest-Hilfsmittel zum Ersetzen von list_all()
    @expected HTTP 503 mit deutscher Meldung
    """

    def failing_list_all():
        raise RepositoryError("timeout while reading airports")

    monkeypatch.setattr(repository, "list_all", failing_list_all)

    response = client.get("/airports")

    assert response.status_code == 503
    assert "konnten nicht geladen werden" in response.json()["detail"]
    assert "timeout" not in response.text
