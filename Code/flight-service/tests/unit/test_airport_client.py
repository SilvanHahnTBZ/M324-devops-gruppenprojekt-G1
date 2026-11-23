"""
Unit Tests für den HTTP-Client zum Flughafenservice.

Statt eines echten Netzwerks liefert {@code httpx.MockTransport} vorbereitete
Antworten. So wird geprüft, dass der Client die Antwort von GET /airports
(US-02) richtig liest und Fehler einheitlich meldet.

@see <a href="https://github.com/SilvanHahnTBZ/M324-devops-gruppenprojekt-G1/issues/3">US-03 #3</a>
@since 0.1.0
"""

import httpx
import pytest

from app.airport_client import AirportServiceUnavailableError, HttpAirportClient


def _client(handler) -> HttpAirportClient:
    http = httpx.Client(base_url="http://airport-service", transport=httpx.MockTransport(handler))
    return HttpAirportClient("http://airport-service", http_client=http)


def test_get_airport_codes_reads_codes_from_list_endpoint():
    """
    Happy Path: Der Client ruft GET /airports auf und liest die Kürzel aus items.

    @expected Pfad /airports, Ergebnis {"ZRH", "GVA"}
    """
    requested_paths = []

    def handler(request: httpx.Request) -> httpx.Response:
        requested_paths.append(request.url.path)
        return httpx.Response(200, json={"count": 2, "items": [{"code": "ZRH"}, {"code": "GVA"}], "message": None})

    assert _client(handler).get_airport_codes() == {"ZRH", "GVA"}
    assert requested_paths == ["/airports"]


def test_get_airport_codes_returns_empty_set_for_empty_airport_list():
    """
    Happy Path: Ein leerer Bestand ist kein Fehler, sondern eine leere Menge.

    @expected leere Menge, keine Exception
    """
    empty = {"count": 0, "items": [], "message": "Es sind noch keine Flughäfen erfasst."}

    assert _client(lambda _: httpx.Response(200, json=empty)).get_airport_codes() == set()


@pytest.mark.parametrize(
    "handler",
    [
        lambda _: httpx.Response(503, json={"detail": "DB down"}),
        lambda _: httpx.Response(200, text="kein json"),
        lambda _: httpx.Response(200, json={"unerwartet": []}),
    ],
    ids=["status-503", "kein-json", "falsches-format"],
)
def test_get_airport_codes_raises_on_bad_response(handler):
    """
    Sad Path: Fehlerstatus oder unerwartete Antworten führen zu AirportServiceUnavailableError.

    @param handler simulierte fehlerhafte Antwort des Flughafenservice
    @throws AirportServiceUnavailableError erwartet
    """
    with pytest.raises(AirportServiceUnavailableError):
        _client(handler).get_airport_codes()


def test_get_airport_codes_raises_when_service_unreachable():
    """
    Sad Path: Ein Netzwerkfehler (z. B. Dienst nicht gestartet) wird übersetzt.

    @throws AirportServiceUnavailableError erwartet statt httpx.ConnectError
    """

    def handler(request: httpx.Request) -> httpx.Response:
        raise httpx.ConnectError("Connection refused", request=request)

    with pytest.raises(AirportServiceUnavailableError):
        _client(handler).get_airport_codes()
