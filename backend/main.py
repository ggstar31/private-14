"""
main.py — CafeKasol FastAPI application.
Run: uvicorn main:app --reload --port 8000
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
import db

app = FastAPI(title="CafeKasol API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/api/v1/cafes/nearby")
def cafes_nearby(
    lat: float = Query(..., description="User latitude"),
    lon: float = Query(..., description="User longitude"),
    radius: float = Query(5.0, description="Search radius in km", ge=0.1, le=50),
):
    cafes = db.get_cafes_nearby(lat, lon, radius)
    return cafes


@app.get("/api/v1/cafes/search")
def cafes_search(q: str = Query(..., min_length=1, description="Search query")):
    return db.search_cafes(q)


@app.get("/api/v1/cafes/{cafe_id}")
def cafe_detail(cafe_id: int):
    cafe = db.get_cafe_by_id(cafe_id)
    if not cafe:
        raise HTTPException(status_code=404, detail="Cafe not found")
    return cafe


@app.get("/api/v1/cafes")
def cafes_list():
    return db.get_all_cafes()


@app.get("/health")
def health():
    return {"status": "ok"}
