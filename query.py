"""Running queries against the flight database."""

import math
import re
from datetime import datetime


def run_query(db: list[dict], query: dict) -> dict:
    """Return one response entry for one query object.

    Valid query:   {"query": query, "matches": [...]}
    Invalid query: {"query": query, "error": "INVALID_QUERY", "matches": []}
    """
    if not isinstance(query, dict):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}

    allowed_keys = {
        "flight_id", "origin", "destination",
        "departure_datetime", "arrival_datetime",
        "price", "min_price", "sort_by", "order", "limit"
    }

    if not set(query).issubset(allowed_keys):
        return {"query": query, "error": "INVALID_QUERY", "matches": []}

    for key in ("flight_id", "origin", "destination"):
        if key in query and not isinstance(query[key], str):
            return {"query": query, "error": "INVALID_QUERY", "matches": []}

    date_format = r"[0-9]{4}-[0-9]{2}-[0-9]{2} [0-9]{2}:[0-9]{2}"

    for key in ("departure_datetime", "arrival_datetime"):
        if key in query:
            value = query[key]

            if not isinstance(value, str) or not re.fullmatch(date_format, value):
                return {"query": query, "error": "INVALID_QUERY", "matches": []}

            try:
                datetime.strptime(value, "%Y-%m-%d %H:%M")
            except ValueError:
                return {"query": query, "error": "INVALID_QUERY", "matches": []}

    for key in ("price", "min_price"):
        if key in query:
            value = query[key]

            if isinstance(value, bool) or not isinstance(value, (int, float)):
                return {"query": query, "error": "INVALID_QUERY", "matches": []}

    record_keys = {
        "flight_id", "origin", "destination",
        "departure_datetime", "arrival_datetime", "price"
    }

    if "sort_by" in query:
        if not isinstance(query["sort_by"], str) or query["sort_by"] not in record_keys:
            return {"query": query, "error": "INVALID_QUERY", "matches": []}

    if "order" in query:
        if "sort_by" not in query or query["order"] not in ("asc", "desc"):
            return {"query": query, "error": "INVALID_QUERY", "matches": []}

    if "limit" in query:
        if isinstance(query["limit"], bool) or not isinstance(query["limit"], int) or query["limit"] < 0:
            return {"query": query, "error": "INVALID_QUERY", "matches": []}

    matches = []

    for flight in db:
        if any(flight[key] != query[key] for key in ("flight_id", "origin", "destination") if key in query):
            continue

        if "departure_datetime" in query:
            if flight["departure_datetime"] < query["departure_datetime"]:
                continue

        if "arrival_datetime" in query:
            if flight["arrival_datetime"] > query["arrival_datetime"]:
                continue

        if "price" in query and flight["price"] > query["price"]:
            continue

        if "min_price" in query and flight["price"] < query["min_price"]:
            continue

        matches.append(flight)

    if "sort_by" in query:
        matches = sorted(
            matches,
            key=lambda flight: flight[query["sort_by"]],
            reverse=query.get("order", "asc") == "desc"
        )

    if "limit" in query:
        matches = matches[:query["limit"]]

    return {"query": query, "matches": matches}


def run_queries(db: list[dict], queries: dict | list) -> list[dict]:
    """Accept one query object or a list of them; always return a list."""
    if isinstance(queries, list):
        return [run_query(db, query) for query in queries]

    return [run_query(db, queries)]
