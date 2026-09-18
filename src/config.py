import os

DB_USER = os.environ.get("SPOTIFY_DB_USER", "root")
DB_PASSWORD = os.environ.get("SPOTIFY_DB_PASSWORD")
DB_HOST = os.environ.get("SPOTIFY_DB_HOST", "localhost")
DB_NAME = os.environ.get("SPOTIFY_DB_NAME", "spotify_db")

JSON_PATH = os.environ.get("SPOTIFY_JSON_PATH")

USERNAME = os.environ.get("SPOTIFY_USERNAME", "Andrea")