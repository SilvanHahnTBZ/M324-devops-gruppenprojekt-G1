"""Fehlerbehandlung: übersetzt Validierungsfehler in verständliche Meldungen."""

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

_MESSAGES = {
    "missing": "Pflichtfeld fehlt.",
    "int_type": "Muss eine ganze Zahl sein.",
    "int_parsing": "Muss eine ganze Zahl sein.",
    "int_from_float": "Muss eine ganze Zahl sein.",
    "string_type": "Muss ein Text sein.",
    "extra_forbidden": "Dieses Feld ist nicht erlaubt.",
    "json_invalid": "Der Inhalt ist kein gültiges JSON.",
    "model_attributes_type": "Erwartet wird ein JSON-Objekt.",
    "dict_type": "Erwartet wird ein JSON-Objekt.",
}


def _translate(error: dict) -> str:
    """Liefert eine deutsche Meldung für einen einzelnen Pydantic-Fehler."""
    kind = error.get("type", "")
    ctx = error.get("ctx") or {}
    if kind == "value_error" and "error" in ctx:
        return str(ctx["error"])
    if kind == "greater_than":
        return f"Muss grösser als {ctx.get('gt')} sein."
    if kind == "less_than_equal":
        return f"Darf höchstens {ctx.get('le')} sein."
    if kind == "string_too_short":
        return f"Muss mindestens {ctx.get('min_length')} Zeichen lang sein."
    if kind == "string_too_long":
        return f"Darf höchstens {ctx.get('max_length')} Zeichen lang sein."
    return _MESSAGES.get(kind, error.get("msg", "Ungültiger Wert."))


def _field(loc: tuple) -> str | None:
    parts = [str(p) for p in loc if p != "body"]
    return ".".join(parts) or None


async def validation_exception_handler(_: Request, exc: RequestValidationError) -> JSONResponse:
    """Antwortet mit HTTP 422 und einer Liste ``{field, message}``."""
    errors = [{"field": _field(e["loc"]), "message": _translate(e)} for e in exc.errors()]
    return JSONResponse(
        status_code=422,
        content={"detail": "Die Eingabe ist ungültig. Bitte die markierten Felder korrigieren.", "errors": errors},
    )
