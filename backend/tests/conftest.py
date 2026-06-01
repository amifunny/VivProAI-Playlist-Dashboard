import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.data_processing.data import connect_db, load_songs_from_file
import pytest
from app import create_app


@pytest.fixture
def client(tmp_path, monkeypatch):
    print("---- tmp_path", tmp_path)
    monkeypatch.setenv("DATABASE_URL", str(tmp_path / "storage.db"))

    engine = connect_db()
    load_songs_from_file(ROOT / "data_processing" / "test_data.json", engine=engine)
    
    app = create_app()
    app.config.update(TESTING=True)
    with app.test_client() as c:
        yield c
