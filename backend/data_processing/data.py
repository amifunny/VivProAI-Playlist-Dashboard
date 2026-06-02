from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path
from sqlalchemy import create_engine, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.exc import OperationalError
from sqlalchemy.orm import Session

BASE_DIR = Path(__file__).parent
BACKEND_DIR = BASE_DIR.parent
DATABASE = BACKEND_DIR / "storage.db"
DEFAULT_DB = DATABASE

sys.path.append(str(BASE_DIR.parent))
from model import Base,  Song

def db_path():
    return Path(os.environ.get("DATABASE_URL", DEFAULT_DB))

def connect_db():
    engine = create_engine(f"sqlite:///{db_path()}")
    try:
        Base.metadata.create_all(engine)
    except OperationalError as exc:
        if "already exists" not in str(exc):
            raise
    return engine

def _to_float(value, default=0.0):
        try:
            if value is None:
                return default
            return float(value)
        except (TypeError, ValueError):
            return default

def normalize_json(json_filename):
    path = json_filename
    
    try:
        with open(path) as f:
            raw_json = json.load(f)
    except ValueError as exc:
        raise ValueError(str(exc)) 


    if "id" not in raw_json:
        raise ValueError("playlist JSON is missing the 'id' column")

    columns = dict()
    for key, value in raw_json.items():
        if isinstance(value, dict):
            columns[key] = value
    
    indices = sorted(columns["id"].keys(), key=int)
    
    rows = []
    for index in indices:
        row = {
            "index": int(index),
            "id": columns["id"].get(index, ""),
            "title": columns.get("title", {}).get(index, ""),
        }

        for field, mapping in columns.items():
            if field in {"id", "title"}:
                continue
            row[field] = _to_float(mapping.get(index))

        rows.append(row)

    return rows

def insert_data_to_db(engine, rows):
    with Session(engine) as session:
        for row in rows:
            statement = insert(Song).values(
                id=row.get("id", ""),
                title=row.get("title", ""),
                index=row.get("index", 0),
                danceability=row.get("danceability", 0.0),
                acousticness=row.get("acousticness", 0.0),
                energy=row.get("energy", 0.0),
                mode=row.get("mode", 0.0),
                tempo=row.get("tempo", 0.0),
                duration_ms=row.get("duration_ms", 0.0),
                num_sections=row.get("num_sections", 0.0),
                num_segments=row.get("num_segments", 0.0),
            )
            session.execute(
                statement.on_conflict_do_update(
                    index_elements=[Song.id],
                    set_={
                        "title": row.get("title", ""),
                        "index": row.get("index", 0),
                        "danceability": row.get("danceability", 0.0),
                        "acousticness": row.get("acousticness", 0.0),
                        "energy": row.get("energy", 0.0),
                        "mode": row.get("mode", 0.0),
                        "tempo": row.get("tempo", 0.0),
                        "duration_ms": row.get("duration_ms", 0.0),
                        "num_sections": row.get("num_sections", 0.0),
                        "num_segments": row.get("num_segments", 0.0),
                    },
                )
            )
        session.commit()

def load_songs_from_file(json_filename, engine=None):
    rows = normalize_json(json_filename)
    if engine is None:
        engine = connect_db()
    insert_data_to_db(engine, rows)
    return len(rows)


def main():
    parser = argparse.ArgumentParser(
        description="Load a playlist JSON file into database"
    )
    parser.add_argument(
        "json_file",
        help="JSON file path to load",
    )
    args = parser.parse_args()

    totalLoaded = load_songs_from_file(args.json_file)
    print(f"Loaded {totalLoaded} songs into {db_path()}")


if __name__ == "__main__":
    main()
