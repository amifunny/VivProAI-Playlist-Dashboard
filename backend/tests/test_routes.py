def test_health(client):
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["ok"] is True

def test_songs_pagination(client):
    response = client.get("/api/songs")
    assert response.status_code == 200
    data = response.get_json()
    assert data["total"] == 100
    assert data["page"] == 1
    assert data["page_size"] == 10
    assert len(data["items"]) == 10

    item = data["items"][0]
    for key in ("id", "title", "danceability", "energy", "tempo", "duration_ms", "rating"):
        assert key in item

def test_songs_pagination_bad_request(client):
    response = client.get("/api/songs?page=0")
    assert response.status_code == 400

def test_all_songs(client):
    response = client.get("/api/songs/all")
    data = response.get_json()
    assert data["total"] == 100
    assert len(data["items"]) == 100

def test_search_title_exact(client):
    response = client.get("/api/songs/search?title=3AM")
    assert response.status_code == 200
    assert response.get_json()["items"][0]["title"] == "3AM"


def test_search_title_missing(client):
    response = client.get("/api/songs/search?title=not-available")
    assert response.status_code == 200
    data = response.get_json()
    assert len(data["items"]) == 0

def test_search_title_param_bad_request(client):
    response = client.get("/api/songs/search")
    assert response.status_code == 400


def test_song_rating_update(client):
    songs = client.get("/api/songs/all").get_json()["items"]
    song_id = songs[0]["id"]

    response = client.put(f"/api/songs/{song_id}/rating", json={"rating": 4})
    assert response.status_code == 200
    assert response.get_json() == {"id": song_id, "rating": 4}

    response_again = client.get("/api/songs").get_json()
    match = next(s for s in response_again["items"] if s["id"] == song_id)
    assert match["rating"] == 4


def test_song_rating_bad_request(client):
    songs = client.get("/api/songs/all").get_json()["items"]
    song_id = songs[0]["id"]
    assert client.put(f"/api/songs/{song_id}/rating", json={"rating": 6}).status_code == 400
    assert client.put(f"/api/songs/{song_id}/rating", json={"rating": -1}).status_code == 400

