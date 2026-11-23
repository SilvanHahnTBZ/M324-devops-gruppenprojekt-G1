"""Zugriff auf den Flughafenservice über dessen REST-API (US-02, GET /airports).

Der Flugservice liest die Datenbank des Flughafenservice nie direkt.
``AirportClient`` ist die Schnittstelle; in Unit Tests ersetzt ein
simulierter Client (Fake) den echten HTTP-Aufruf.
"""

from typing import Protocol

import httpx


class AirportServiceUnavailableError(Exception):
    """Der Flughafenservice ist nicht erreichbar oder antwortet fehlerhaft."""


class AirportClient(Protocol):
    """Liefert die Kürzel aller erfassten Flughäfen."""

    def get_airport_codes(self) -> set[str]:
        """Raises:
        AirportServiceUnavailableError: bei Netzwerkfehler, Status != 200 oder ungültiger Antwort.
        """
        ...


class HttpAirportClient:
    """Ruft ``GET {base_url}/airports`` des Flughafenservice auf."""

    def __init__(self, base_url: str, timeout: float = 3.0, http_client: httpx.Client | None = None) -> None:
        self._http = http_client or httpx.Client(base_url=base_url, timeout=timeout)

    def get_airport_codes(self) -> set[str]:
        try:
            response = self._http.get("/airports")
        except httpx.HTTPError as exc:
            raise AirportServiceUnavailableError(f"Flughafenservice nicht erreichbar: {exc}") from exc
        if response.status_code != 200:
            raise AirportServiceUnavailableError(f"Flughafenservice antwortet mit HTTP {response.status_code}")
        try:
            return {item["code"] for item in response.json()["items"]}
        except (ValueError, KeyError, TypeError) as exc:
            raise AirportServiceUnavailableError("Antwort des Flughafenservice hat ein unerwartetes Format") from exc

    def close(self) -> None:
        self._http.close()
