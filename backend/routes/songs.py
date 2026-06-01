from __future__ import annotations

from flask import Blueprint, abort, request
from sqlalchemy import func, select
from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from model import Rating, Song


def create_songs_blueprint(engine):
    songs_bp = Blueprint("songs", __name__, url_prefix="/api")

    def responseSongs(rows):
        response = []
        for song, rating in rows:
            response.append(
                {
                    "index": song.index,
                    "id": song.id,
                    "title": song.title,
                    "danceability": song.danceability,
                    "acousticness": song.acousticness,
                    "energy": song.energy,
                    "mode": song.mode,
                    "tempo": song.tempo,
                    "duration_ms": song.duration_ms,
                    "num_sections": song.num_sections,
                    "num_segments": song.num_segments,
                    "rating": int(rating or 0),
                }
            )
        return response
       

    @songs_bp.get("/health")
    def health():
        return {"ok": True}


    @songs_bp.get("/songs/all")
    def all_songs():
        with Session(engine) as session:
            statement = (
                select(Song, Rating.rating)
                .outerjoin(Rating, Rating.song_id == Song.id)
                .order_by(Song.index)
            )
            results = session.execute(statement).all()

        
        return {"total": len(results), "items": responseSongs(results)}

    @songs_bp.get("/songs/search")
    def search_songs():
        title = (request.args.get("title") or "").strip()
        if not title:
            abort(400, description="title query param not provided")

        with Session(engine) as session:
            statement = (
                select(Song, Rating.rating)
                .outerjoin(Rating, Rating.song_id == Song.id)
                .where(func.lower(Song.title).like(f"%{title.lower()}%"))
                .order_by(Song.index)
            )
            results = session.execute(statement).all()
        
        return {"total": len(results), "items": responseSongs(results)}


   
    @songs_bp.put("/songs/<song_id>/rating")
    def rate_song(song_id):
        body = request.get_json(silent=True) or {}
        try:
            rating = int(body.get("rating"))
        except (TypeError, ValueError):
            abort(400, description="rating not provided")

        if rating < 0 or rating > 5:
            abort(400, description="rating must be between 0 and 5")

        with Session(engine) as session:
            check_if_exists = session.execute(select(Song.id).where(Song.id == song_id)).scalar_one_or_none()
            if not check_if_exists:
                abort(404, description="song not found")

            statement = insert(Rating).values(song_id=song_id, rating=rating)
            session.execute(
                statement.on_conflict_do_update(
                    index_elements=[Rating.song_id],
                    set_={"rating": rating},
                )
            )
            session.commit()

        return {"id": song_id, "rating": rating}

    @songs_bp.get("/songs")
    def list_songs():
        try:
            page = int(request.args.get("page", 1))
            page_size = int(request.args.get("page_size", 10))
        except ValueError:
            abort(400, description="page/page_size must be integers")

        if page < 1 or page_size < 1:
            abort(400, description="page and page_size more than 0")
            
        page_size = min(page_size, 500)
        start = (page - 1) * page_size

        with Session(engine) as session:
            total = session.execute(select(func.count()).select_from(Song)).scalar_one()
            statement = (
                select(Song, Rating.rating)
                .outerjoin(Rating, Rating.song_id == Song.id)
                .order_by(Song.index)
                .offset(start)
                .limit(page_size)
            )
            results = session.execute(statement).all()

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": responseSongs(results),
        }

    return songs_bp
