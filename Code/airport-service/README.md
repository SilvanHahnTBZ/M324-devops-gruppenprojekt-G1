# Flughafenservice (Mikroservice 1)

REST-API zur Verwaltung von Flughäfen. Version `0.1.0`.

| Methode | Pfad | Story | Erfolg | Fehler |
|---|---|---|---|---|
| `POST` | `/airports` | US-01 [#1](https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/1) | 201 | 409 Kürzel doppelt, 422 ungültige Eingabe, 503 DB-Fehler |
| `GET` | `/health` | Betrieb | 200 | – |

Die interaktive API-Doku liegt nach dem Start unter <http://localhost:8001/docs>.

## Aufbau

```
app/
  main.py        REST-Endpoints, Statuscodes, Abhängigkeiten (create_app)
  schemas.py     Eingabe-/Ausgabeschemas und Validierung (Pydantic)
  service.py     Geschäftslogik (ID und Erstellungsdatum)
  repository.py  Datenzugriff: Schnittstelle, PostgreSQL- und In-Memory-Umsetzung
  errors.py      deutsche Fehlermeldungen für Validierungsfehler
tests/
  unit/          isolierte Tests ohne Datenbank (In-Memory-Repository)
  integration/   Tests gegen eine echte Datenbank
```

## Lokal ausführen

```powershell
cd Code/airport-service
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
```

Tests (ohne Datenbank, ohne Docker):

```powershell
pytest -v
```

Integrationstests gegen PostgreSQL statt SQLite:

```powershell
$env:TEST_DATABASE_URL = "postgresql+psycopg://airport:airport@localhost:5433/airports"; pytest -m integration -v
```

Dienst starten (PostgreSQL muss laufen, siehe `Code/docker-compose.yml`):

```powershell
uvicorn app.main:app --reload --port 8001
```

Die Datenbank-URL kommt aus der Umgebungsvariablen `DATABASE_URL`. Ohne Angabe gilt der lokale Standard
`postgresql+psycopg://airport:airport@localhost:5433/airports` (nur für die Entwicklung).
