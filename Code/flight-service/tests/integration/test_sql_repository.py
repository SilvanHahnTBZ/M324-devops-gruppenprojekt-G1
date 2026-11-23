"""
Integrationstest für das SQL-Repository des Flugservice.

Mit ``TEST_DATABASE_URL`` gegen PostgreSQL (CI, P3), sonst gegen eine
temporäre SQLite-Datei.

@see <a href="https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/15">P3 #15</a>
@since 0.1.0
"""

import os
from datetime import UTC, datetime
from uuid import uuid4

import pytest
from sqlalchemy import create_engine, func, select

from app.models import Flight
from app.repository import SqlAlchemyFlightRepository, flights_table, metadata

pytestmark = pytest.mark.integration


@pytest.fixture
def engine(tmp_path):
    """
    Liefert eine Datenbankverbindung mit leerer Tabelle ``flights``.

    @param tmp_path temporärer Ordner für die SQLite-Datei
    @return SQLAlchemy-Engine
    """
    engine = create_engine(os.getenv("TEST_DATABASE_URL", f"sqlite:///{tmp_path / 'flights.db'}"))
    metadata.drop_all(engine)
    metadata.create_all(engine)
    yield engine
    metadata.drop_all(engine)
    engine.dispose()


def test_add_persists_flight(engine):
    """
    Ein gespeicherter Flug landet als Zeile in der Tabelle ``flights``.

    @param engine Verbindung zur Testdatenbank
    @expected genau eine Zeile mit derselben ID und Strecke
    """
    flight = Flight(
        id=uuid4(),
        departure_airport="ZRH",
        arrival_airport="GVA",
        departure_time=datetime(2026, 12, 1, 8, 30, tzinfo=UTC),
        arrival_time=datetime(2026, 12, 1, 9, 25, tzinfo=UTC),
        aircraft_type="Boeing 727",
        created_at=datetime.now(UTC),
    )

    SqlAlchemyFlightRepository(engine).add(flight)

    with engine.connect() as conn:
        assert conn.execute(select(func.count()).select_from(flights_table)).scalar_one() == 1
        row = conn.execute(select(flights_table)).mappings().one()
    assert row["id"] == flight.id
    assert (row["departure_airport"], row["arrival_airport"]) == ("ZRH", "GVA")
