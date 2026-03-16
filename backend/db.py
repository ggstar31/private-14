"""
db.py — SQLite connection and cafe queries.
"""

import sqlite3
import json
import math
import os
from typing import Optional

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'cafes.db')


def get_conn() -> sqlite3.Connection:
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def _haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """Returns distance in kilometers."""
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(d_lon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


def _row_to_dict(row: sqlite3.Row, distance: Optional[float] = None) -> dict:
    d = dict(row)
    d["tags"] = json.loads(d["tags"])
    d["wifi"] = bool(d["wifi"])
    if distance is not None:
        d["distance"] = round(distance, 3)
    return d


def get_cafes_nearby(lat: float, lon: float, radius_km: float = 5.0) -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM cafes").fetchall()
    result = []
    for row in rows:
        dist = _haversine(lat, lon, row["lat"], row["lon"])
        if dist <= radius_km:
            result.append(_row_to_dict(row, dist))
    result.sort(key=lambda c: c["distance"])
    return result


def get_all_cafes() -> list[dict]:
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM cafes ORDER BY name").fetchall()
    return [_row_to_dict(r) for r in rows]


def get_cafe_by_id(cafe_id: int) -> Optional[dict]:
    with get_conn() as conn:
        row = conn.execute("SELECT * FROM cafes WHERE id = ?", (cafe_id,)).fetchone()
    return _row_to_dict(row) if row else None


def search_cafes(query: str) -> list[dict]:
    like = f"%{query}%"
    with get_conn() as conn:
        rows = conn.execute(
            "SELECT * FROM cafes WHERE name LIKE ? ORDER BY name",
            (like,),
        ).fetchall()
    return [_row_to_dict(r) for r in rows]
