from pathlib import Path

from flask import Flask, jsonify
from flask_cors import CORS

from data_processing.data import connect_db, load_songs_from_file
from routes.songs import create_songs_blueprint

def create_app():
    app = Flask(__name__)
    CORS(app)

    engine = connect_db()
    app.register_blueprint(create_songs_blueprint(engine))

    @app.errorhandler(400)
    @app.errorhandler(404)
    def _error_handler(e):
        return jsonify(error=e.description), e.code

    return app


if __name__ == "__main__":
    create_app().run(host="127.0.0.1", port=5001, debug=True)
