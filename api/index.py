"""
api/index.py — Vercel serverless FastAPI handler.
Cafe data is embedded directly (no SQLite needed on Vercel).
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from mangum import Mangum
import math

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

# ── Embedded cafe data (seeded from real Kasol sources) ───────────────────────
CAFES = [
    {"id": 1,  "name": "Moon Dance Cafe & German Bakery", "lat": 32.0102, "lon": 77.3147, "open_time": "10:45", "close_time": "23:30", "wifi": False, "phone": None,              "tags": ["bakery", "river-view", "israeli-menu", "live-music", "bar", "budget", "non-veg"]},
    {"id": 2,  "name": "The Evergreen Cafe",               "lat": 32.0110, "lon": 77.3158, "open_time": "08:00", "close_time": "22:30", "wifi": False, "phone": None,              "tags": ["israeli-menu", "non-veg", "trout", "multicuisine", "outdoor-seating", "budget"]},
    {"id": 3,  "name": "Stone Garden Cafe",                "lat": 32.0096, "lon": 77.3142, "open_time": "08:00", "close_time": "00:00", "wifi": False, "phone": None,              "tags": ["israeli-menu", "live-music", "river-view", "outdoor-seating", "non-veg", "bonfire"]},
    {"id": 4,  "name": "Little Italy Inn",                 "lat": 32.0098, "lon": 77.3150, "open_time": "08:00", "close_time": "22:00", "wifi": True,  "phone": None,              "tags": ["israeli-menu", "bakery", "bar", "rooftop", "non-veg", "trout", "multicuisine"]},
    {"id": 5,  "name": "Bhoj Cafe",                        "lat": 32.0101, "lon": 77.3145, "open_time": "12:00", "close_time": "01:00", "wifi": False, "phone": None,              "tags": ["israeli-menu", "non-veg", "bar", "live-music", "late-night", "budget"]},
    {"id": 6,  "name": "Jim Morrison Cafe",                "lat": 32.0118, "lon": 77.3160, "open_time": "09:00", "close_time": "22:30", "wifi": False, "phone": None,              "tags": ["veg", "no-egg", "floor-seating", "filter-coffee", "bakery", "rooftop", "budget"]},
    {"id": 7,  "name": "Offlimits Coffee",                 "lat": 32.0095, "lon": 77.3138, "open_time": "08:00", "close_time": "23:00", "wifi": True,  "phone": None,              "tags": ["specialty-coffee", "river-view", "israeli-menu", "veg", "non-veg", "budget"]},
    {"id": 8,  "name": "Rudraksh Cafe",                    "lat": 32.0115, "lon": 77.3162, "open_time": "09:30", "close_time": "23:00", "wifi": False, "phone": "+919910153916",   "tags": ["multicuisine", "israeli-menu", "non-veg", "veg", "fireplace", "budget", "cozy"]},
    {"id": 9,  "name": "Panjtara Bar & Grill",             "lat": 32.0097, "lon": 77.3141, "open_time": "11:00", "close_time": "23:30", "wifi": False, "phone": None,              "tags": ["live-music", "bar", "veg", "vegan", "gluten-free", "bakery", "bonfire", "outdoor-seating"]},
    {"id": 10, "name": "Cafe 4:20",                        "lat": 32.0085, "lon": 77.3078, "open_time": "00:00", "close_time": "23:59", "wifi": True,  "phone": None,              "tags": ["riverside", "camping", "bar", "bonfire", "non-veg", "veg", "budget", "hookah"]},
    {"id": 11, "name": "Shanti Cafe & Hostels",            "lat": 32.0119, "lon": 77.3048, "open_time": "00:00", "close_time": "23:59", "wifi": True,  "phone": "+918310266737",   "tags": ["river-view", "live-music", "bonfire", "veg", "vegan", "israeli-menu", "hostel", "dj-nights"]},
    {"id": 12, "name": "Cafe 9 Chalal",                    "lat": 32.0124, "lon": 77.3036, "open_time": "09:00", "close_time": "23:00", "wifi": False, "phone": "+918627025205",   "tags": ["river-view", "fireplace", "trance-music", "camping", "live-music", "bonfire", "veg", "cozy"]},
    {"id": 13, "name": "Freedom Cafe",                     "lat": 32.0130, "lon": 77.3022, "open_time": "09:00", "close_time": "04:00", "wifi": False, "phone": None,              "tags": ["riverside", "trance-music", "bonfire", "live-music", "non-veg", "veg", "late-night", "budget"]},
    {"id": 14, "name": "Sunshine Cafe",                    "lat": 32.0088, "lon": 77.3130, "open_time": "08:00", "close_time": "23:00", "wifi": False, "phone": None,              "tags": ["river-view", "non-veg", "trout", "israeli-menu", "budget", "outdoor-seating"]},
    {"id": 15, "name": "Rider's Cafe",                     "lat": 32.0103, "lon": 77.3148, "open_time": "10:00", "close_time": "02:30", "wifi": False, "phone": None,              "tags": ["multicuisine", "israeli-menu", "mexican", "hookah", "live-music", "late-night", "non-veg", "veg"]},
    {"id": 16, "name": "German Bakery Kasol",              "lat": 32.0100, "lon": 77.3151, "open_time": "12:00", "close_time": "23:30", "wifi": False, "phone": None,              "tags": ["bakery", "falafel", "pastry", "budget", "veg", "israeli-menu", "takeaway"]},
]


def _haversine(lat1, lon1, lat2, lon2):
    R = 6371
    d_lat = math.radians(lat2 - lat1)
    d_lon = math.radians(lon2 - lon1)
    a = (math.sin(d_lat / 2) ** 2
         + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2))
         * math.sin(d_lon / 2) ** 2)
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


# ── Routes ────────────────────────────────────────────────────────────────────

@app.get("/api/v1/cafes/nearby")
def cafes_nearby(
    lat: float = Query(...),
    lon: float = Query(...),
    radius: float = Query(5.0, ge=0.1, le=50),
):
    result = []
    for cafe in CAFES:
        dist = _haversine(lat, lon, cafe["lat"], cafe["lon"])
        if dist <= radius:
            result.append({**cafe, "distance": round(dist, 3)})
    result.sort(key=lambda c: c["distance"])
    return result


@app.get("/api/v1/cafes/search")
def cafes_search(q: str = Query(..., min_length=1)):
    q_lower = q.lower()
    return [
        c for c in CAFES
        if q_lower in c["name"].lower() or any(q_lower in t for t in c["tags"])
    ]


@app.get("/api/v1/cafes/{cafe_id}")
def cafe_detail(cafe_id: int):
    for cafe in CAFES:
        if cafe["id"] == cafe_id:
            return cafe
    raise HTTPException(status_code=404, detail="Cafe not found")


@app.get("/api/v1/cafes")
def cafes_list():
    return CAFES


@app.get("/health")
def health():
    return {"status": "ok"}

handler = Mangum(app)
