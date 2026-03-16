# CLAUDE.md

## Project Overview

**private-14** is a proximity-based cafe discovery tool that uses real-time geolocation to find and display nearby cafes. Designed specifically for **low-connectivity hill station conditions**, the app prioritizes offline-first operation, minimal data usage, and fast local lookups.

## Language & Stack

**Language: Python (backend) + JavaScript (frontend)**

| Layer | Technology | Reason |
|-------|-----------|--------|
| Backend API | **Python 3.11+ / FastAPI** | Lightweight, async, easy local deployment |
| Frontend | **Vanilla JavaScript PWA** | Offline-capable via service workers; no app store; runs in any browser |
| Database | **SQLite (via Python sqlite3)** | Embedded, zero-config, works fully offline |
| Geolocation | **Browser Geolocation API** | Native, no third-party dependency |
| Maps (optional) | **Leaflet.js + OpenStreetMap tiles** | Open-source, tiles can be cached offline |

## Repository Structure

```
/
├── CLAUDE.md                  # This file
├── README.md                  # Project description
├── backend/
│   ├── main.py                # FastAPI app entry point
│   ├── db.py                  # SQLite setup and queries
│   ├── models.py              # Pydantic data models
│   ├── routes/
│   │   ├── cafes.py           # /cafes endpoints (nearby, search, detail)
│   │   └── sync.py            # Optional sync endpoint for bulk data refresh
│   ├── data/
│   │   └── cafes.db           # SQLite database (gitignored)
│   └── requirements.txt       # Python dependencies
├── frontend/
│   ├── index.html             # App shell
│   ├── app.js                 # Main JS logic
│   ├── geo.js                 # Geolocation utilities
│   ├── ui.js                  # DOM rendering helpers
│   ├── sw.js                  # Service worker for offline caching
│   ├── manifest.json          # PWA manifest
│   └── style.css              # Styles
└── scripts/
    └── seed_cafes.py          # Script to populate DB with cafe data
```

## Current State

- Branch `claude/cafe-discovery-geolocation-WdwEx` is active
- CLAUDE.md updated with project direction
- No source code written yet — greenfield

## Low-Connectivity Design Principles

- **Offline-first**: Service worker caches the app shell and last-fetched cafe data
- **Local-first queries**: Haversine distance calculations run in the Python backend against the local SQLite DB — no external API calls required for core functionality
- **Minimal payload**: API responses return only essential fields (name, distance, lat/lon, open status)
- **Progressive enhancement**: Map tiles load only when connectivity is available; list view always works
- **Bulk sync over spot queries**: A single `/sync` endpoint refreshes all cafe data at once when connectivity is good, avoiding repeated small requests

## Development Workflow

```
# Backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Seed database
python scripts/seed_cafes.py

# Frontend (serve locally)
cd frontend
python -m http.server 3000
```

- **Build:** No build step — vanilla JS, no bundler
- **Test:** `pytest backend/tests/` (to be set up)
- **Lint:** `ruff check backend/` and `eslint frontend/`
- **Format:** `ruff format backend/`

## Conventions

- **Python**: PEP 8, type hints on all function signatures, Pydantic models for request/response validation
- **JavaScript**: ES2020+, no framework, modules via `<script type="module">`
- **Naming**: `snake_case` for Python, `camelCase` for JS, `kebab-case` for HTML/CSS
- **API routes**: REST, versioned under `/api/v1/`
- **Distance**: Haversine formula, results in kilometers
- **Commit messages**: `type(scope): description` — e.g., `feat(geo): add haversine distance filter`

## Key API Endpoints (planned)

| Method | Path | Description |
|--------|------|-------------|
| GET | `/api/v1/cafes/nearby` | Cafes within `radius` km of `lat,lon` |
| GET | `/api/v1/cafes/{id}` | Single cafe detail |
| GET | `/api/v1/cafes/search` | Text search by name |
| POST | `/api/v1/sync` | Bulk refresh cafe data from upstream source |

## Environment Setup

```bash
# Python 3.11+
python -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn pydantic sqlite3
```

No external API keys required for offline operation. If online map tiles (OpenStreetMap) are desired, no key is needed. Optional: a one-time data import from Overpass API (OpenStreetMap) to seed cafe locations.

## Notes for AI Assistants

- This is a **low-connectivity-first** project — never introduce dependencies that require constant internet
- All core functionality (geolocation + nearby search) must work fully offline after first load
- Keep the frontend dependency-free (no npm, no bundler) unless there is a strong reason
- SQLite is the database — do not introduce PostgreSQL, MongoDB, or other servers
- Always read this file at the start of a session as it will be updated as the project evolves
- When adding new infrastructure, update this file accordingly
