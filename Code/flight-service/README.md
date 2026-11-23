# Flugservice (Mikroservice 2)

REST-API zur Erfassung von Flügen. Version `0.1.0`.

| Methode | Pfad | Story | Erfolg | Fehler |
|---|---|---|---|---|
| `POST` | `/flights` | US-03 [#3](https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/3) | 201 | 422 ungültige Eingabe oder unbekannter Flughafen, 503 Flughafenservice oder DB nicht erreichbar |
| `GET` | `/health` | Betrieb | 200 | – |

Beispiel:

```json
{
  "departure_airport": "ZRH",
  "arrival_airport": "GVA",
  "departure_time": "2026-12-01T08:30:00Z",
  "arrival_time": "2026-12-01T09:25:00Z",
  "aircraft_type": "Boeing 727"
}
```

## Ablauf und Fehlerfälle

```mermaid
sequenceDiagram
    participant A as Administrator
    participant F as Flugservice
    participant H as Flughafenservice
    participant DB as Flug-DB
    A->>F: POST /flights
    F->>F: Format, UTC, Flughäfen verschieden, Landung nach Start
    alt Eingabe ungültig
        F-->>A: 422 mit Feld und Meldung
    else Eingabe gültig
        F->>H: GET /airports
        alt nicht erreichbar
            F-->>A: 503
        else Kürzel unbekannt
            F-->>A: 422 "Flughafen 'XXX' ist nicht erfasst."
        else beide bekannt
            F->>DB: INSERT flights
            F-->>A: 201 mit ID und created_at
        end
    end
```

Der Flugservice liest **nie** die Datenbank des Flughafenservice, sondern nur dessen API (`app/airport_client.py`).

## Lokal ausführen

```powershell
cd Code/flight-service
py -3.11 -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements-dev.txt
pytest -v
```

Die Unit Tests brauchen weder Datenbank noch Flughafenservice: `FakeAirportClient` in `tests/conftest.py`
simuliert den Flughafenservice.

Dienst starten: `uvicorn app.main:app --reload --port 8002`. Umgebungsvariablen:
`DATABASE_URL` (Standard `postgresql+psycopg://flight:flight@localhost:5434/flights`) und
`AIRPORT_SERVICE_URL` (Standard `http://localhost:8001`).
