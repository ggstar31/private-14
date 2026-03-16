"""
seed_cafes.py — Populate the SQLite database with real Kasol cafe data.
Run from project root: python scripts/seed_cafes.py
"""

import sqlite3
import json
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'backend', 'data', 'cafes.db')

CAFES = [
    {
        "name": "Moon Dance Cafe & German Bakery",
        "lat": 32.0102,
        "lon": 77.3147,
        "open_time": "10:45",
        "close_time": "23:30",
        "wifi": False,
        "phone": None,
        "tags": ["bakery", "river-view", "israeli-menu", "live-music", "bar", "budget", "non-veg"],
    },
    {
        "name": "The Evergreen Cafe",
        "lat": 32.0110,
        "lon": 77.3158,
        "open_time": "08:00",
        "close_time": "22:30",
        "wifi": False,
        "phone": None,
        "tags": ["israeli-menu", "non-veg", "trout", "multicuisine", "outdoor-seating", "budget"],
    },
    {
        "name": "Stone Garden Cafe",
        "lat": 32.0096,
        "lon": 77.3142,
        "open_time": "08:00",
        "close_time": "00:00",
        "wifi": False,
        "phone": None,
        "tags": ["israeli-menu", "live-music", "river-view", "outdoor-seating", "non-veg", "bonfire"],
    },
    {
        "name": "Little Italy Inn",
        "lat": 32.0098,
        "lon": 77.3150,
        "open_time": "08:00",
        "close_time": "22:00",
        "wifi": True,
        "phone": None,
        "tags": ["israeli-menu", "bakery", "bar", "rooftop", "non-veg", "trout", "multicuisine"],
    },
    {
        "name": "Bhoj Cafe",
        "lat": 32.0101,
        "lon": 77.3145,
        "open_time": "12:00",
        "close_time": "01:00",
        "wifi": False,
        "phone": None,
        "tags": ["israeli-menu", "non-veg", "bar", "live-music", "late-night", "budget"],
    },
    {
        "name": "Jim Morrison Cafe",
        "lat": 32.0118,
        "lon": 77.3160,
        "open_time": "09:00",
        "close_time": "22:30",
        "wifi": False,
        "phone": None,
        "tags": ["veg", "no-egg", "floor-seating", "filter-coffee", "bakery", "rooftop", "budget"],
    },
    {
        "name": "Offlimits Coffee",
        "lat": 32.0095,
        "lon": 77.3138,
        "open_time": "08:00",
        "close_time": "23:00",
        "wifi": True,
        "phone": None,
        "tags": ["specialty-coffee", "river-view", "israeli-menu", "veg", "non-veg", "budget"],
    },
    {
        "name": "Rudraksh Cafe",
        "lat": 32.0115,
        "lon": 77.3162,
        "open_time": "09:30",
        "close_time": "23:00",
        "wifi": False,
        "phone": "+919910153916",
        "tags": ["multicuisine", "israeli-menu", "non-veg", "veg", "fireplace", "budget", "cozy"],
    },
    {
        "name": "Panjtara Bar & Grill",
        "lat": 32.0097,
        "lon": 77.3141,
        "open_time": "11:00",
        "close_time": "23:30",
        "wifi": False,
        "phone": None,
        "tags": ["live-music", "bar", "veg", "vegan", "gluten-free", "bakery", "bonfire", "outdoor-seating"],
    },
    {
        "name": "Cafe 4:20",
        "lat": 32.0085,
        "lon": 77.3078,
        "open_time": "00:00",
        "close_time": "23:59",
        "wifi": True,
        "phone": None,
        "tags": ["riverside", "camping", "bar", "bonfire", "non-veg", "veg", "budget", "hookah"],
    },
    {
        "name": "Shanti Cafe & Hostels",
        "lat": 32.0119,
        "lon": 77.3048,
        "open_time": "00:00",
        "close_time": "23:59",
        "wifi": True,
        "phone": "+918310266737",
        "tags": ["river-view", "live-music", "bonfire", "veg", "vegan", "israeli-menu", "hostel", "dj-nights"],
    },
    {
        "name": "Cafe 9 Chalal",
        "lat": 32.0124,
        "lon": 77.3036,
        "open_time": "09:00",
        "close_time": "23:00",
        "wifi": False,
        "phone": "+918627025205",
        "tags": ["river-view", "fireplace", "trance-music", "camping", "live-music", "bonfire", "veg", "cozy"],
    },
    {
        "name": "Freedom Cafe",
        "lat": 32.0130,
        "lon": 77.3022,
        "open_time": "09:00",
        "close_time": "04:00",
        "wifi": False,
        "phone": None,
        "tags": ["riverside", "trance-music", "bonfire", "live-music", "non-veg", "veg", "late-night", "budget"],
    },
    {
        "name": "Sunshine Cafe",
        "lat": 32.0088,
        "lon": 77.3130,
        "open_time": "08:00",
        "close_time": "23:00",
        "wifi": False,
        "phone": None,
        "tags": ["river-view", "non-veg", "trout", "israeli-menu", "budget", "outdoor-seating"],
    },
    {
        "name": "Rider's Cafe",
        "lat": 32.0103,
        "lon": 77.3148,
        "open_time": "10:00",
        "close_time": "02:30",
        "wifi": False,
        "phone": None,
        "tags": ["multicuisine", "israeli-menu", "mexican", "hookah", "live-music", "late-night", "non-veg", "veg"],
    },
    {
        "name": "German Bakery Kasol",
        "lat": 32.0100,
        "lon": 77.3151,
        "open_time": "12:00",
        "close_time": "23:30",
        "wifi": False,
        "phone": None,
        "tags": ["bakery", "falafel", "pastry", "budget", "veg", "israeli-menu", "takeaway"],
    },
]


def init_db(conn):
    conn.execute("""
        CREATE TABLE IF NOT EXISTS cafes (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            name        TEXT    NOT NULL,
            lat         REAL    NOT NULL,
            lon         REAL    NOT NULL,
            open_time   TEXT    NOT NULL,
            close_time  TEXT    NOT NULL,
            wifi        INTEGER NOT NULL DEFAULT 0,
            phone       TEXT,
            tags        TEXT    NOT NULL DEFAULT '[]'
        )
    """)
    conn.commit()


def seed(conn):
    conn.execute("DELETE FROM cafes")
    for cafe in CAFES:
        conn.execute(
            """
            INSERT INTO cafes (name, lat, lon, open_time, close_time, wifi, phone, tags)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                cafe["name"],
                cafe["lat"],
                cafe["lon"],
                cafe["open_time"],
                cafe["close_time"],
                1 if cafe["wifi"] else 0,
                cafe["phone"],
                json.dumps(cafe["tags"]),
            ),
        )
    conn.commit()
    print(f"Seeded {len(CAFES)} cafes into {DB_PATH}")


if __name__ == "__main__":
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        init_db(conn)
        seed(conn)
