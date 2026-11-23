"""
Integrationstests für das SQL-Repository des Flughafenservice.

Diese Tests prüfen das Zusammenspiel mit einer echten Datenbank.
Ist ``TEST_DATABASE_URL`` gesetzt (z. B. PostgreSQL in der CI, P3),
läuft der Test dort. Sonst verwendet er eine temporäre SQLite-Datei,
damit er auch ohne Docker lokal ausführbar bleibt.

@see <a href="https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/15">P3 #15</a>
@since 0.1.0
"""

import os
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import create_engine

from app.models import Airport
from app.repository import DuplicateAirportCodeError, SqlAlchemyAirportRepository, metadata

pytestmark = pytest.mark.integration


@pytest.fixture
def sql_repository(tmp_path):
    """
    Liefert ein Repository mit frisch angelegter, leerer Tabelle.

    @param tmp_path temporärer Ordner von pytest für die SQLite-Datei
    @return {@code SqlAlchemyAirportRepository} auf einer leeren Datenbank
    """
    url = os.getenv("TEST_DATABASE_URL", f"sqlite:///{tmp_path / 'airports.db'}")
    engine = create_engine(url)
    metadata.drop_all(engine)
    repository = SqlAlchemyAirportRepository(engine)
    repository.create_schema()
    yield repository
    metadata.drop_all(engine)
    engine.dispose()


def _airport(code: str) -> Airport:
    return Airport(id=uuid4(), name=f"Flughafen {code}", code=code, capacity=1000, created_at=datetime.now(UTC))


def test_unique_constraint_rejects_duplicate_code(sql_repository):
    """
    Der UNIQUE-Constraint der Datenbank verhindert doppelte Kürzel.

    Given ein gespeicherter Flughafen mit Kürzel ZRH
    When ein weiterer Flughafen mit demselben Kürzel gespeichert wird
    Then übersetzt das Repository den Datenbankfehler in DuplicateAirportCodeError.

    @param sql_repository Repository auf echter Datenbank
    @throws DuplicateAirportCodeError erwartet beim zweiten Speichern
    """
    sql_repository.add(_airport("ZRH"))

    with pytest.raises(DuplicateAirportCodeError):
        sql_repository.add(_airport("ZRH"))


def test_list_all_reads_saved_airports_sorted_by_code(sql_repository):
    """
    Gespeicherte Flughäfen werden vollständig und nach Kürzel sortiert gelesen.

    Given drei gespeicherte Flughäfen in zufälliger Reihenfolge
    When list_all aufgerufen wird
    Then kommen alle drei sortiert zurück, mit denselben Werten wie gespeichert.

    @param sql_repository Repository auf echter Datenbank
    @expected Kürzel BSL, GVA, ZRH in dieser Reihenfolge, Felder unverändert
    """
    saved = [sql_repository.add(_airport(code)) for code in ("ZRH", "BSL", "GVA")]

    loaded = sql_repository.list_all()

    assert [a.code for a in loaded] == ["BSL", "GVA", "ZRH"]
    by_code = {a.code: a for a in saved}
    for airport in loaded:
        assert airport.id == by_code[airport.code].id
        assert airport.capacity == by_code[airport.code].capacity
        # Regression: SQLite lieferte created_at ohne Zeitzone (gefunden im E2E-Lauf).
        assert airport.created_at == by_code[airport.code].created_at
        assert airport.created_at.tzinfo is not None
