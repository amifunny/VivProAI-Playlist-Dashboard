# Playlist Dashboard

Full-stack playlist dashboard built with Flask (API) and Nuxt 4 (UI). Also includes unit testing.

It supports:

- paginated song listing

- title-based search

- rating songs (persisted in SQLite)

- chart visualizations for key audio features

## Tech Stack

- `backend/`: Flask + SQLAlchemy + SQLite + pytest

- `frontend/`: Nuxt 4 + Vue 3 + Nuxt UI + Tailwind CSS + Chart.js

## API Endpoints

All backend routes are under `/api`.

| Method | Path | Description |

| ------ | ------------------------- | ------------------------------------- |

| `GET` | `/health` | Health check (`{"ok": true}`) |

| `GET` | `/songs` | Paginated songs (`page`, `page_size`) |

| `GET` | `/songs/all` | Full songs list |

| `GET` | `/songs/search?title=...` | Case-insensitive partial title search |

| `PUT` | `/songs/<song_id>/rating` | Update rating (`0 - 5`) |

## Local Setup

### 1) Backend

Python 3.9+ recommended.

```bash

cd  backend

python3  -m  venv  .venv

source  .venv/bin/activate

pip  install  -r  requirements.txt

```

Seed the database (required before using the app):

```bash

python  data_processing/data.py  data_processing/test_data.json

```

Run the API:

```bash

python  app.py  # http://127.0.0.1:5001

```

### 2) Frontend

Node 18+ recommended.

```bash

cd  frontend

npm  install

npm  run  dev  # http://localhost:3000

```

The frontend uses `http://127.0.0.1:5001` by default.

Override with:

```bash

BACKEND_URL=http://127.0.0.1:5001  npm  run  dev

```

## Running Tests

Backend tests:

```bash

cd  backend

source  .venv/bin/activate

pytest  -q

```
