import os

DB_USER = os.environ.get("SPOTIFY_DB_USER", "root")
DB_PASSWORD = os.environ.get("SPOTIFY_DB_PASSWORD")
DB_HOST = os.environ.get("SPOTIFY_DB_HOST", "localhost")
DB_NAME = os.environ.get("SPOTIFY_DB_NAME", "spotify_db")

SPOTIFY_FOLDER_PATH = os.environ.get("SPOTIFY_FOLDER_PATH")

USERNAME = os.environ.get("SPOTIFY_USERNAME", "Andrea")

def validate():
    """Raise if required configuration is missing."""
    missing = [
        name for name, value in [
            ("SPOTIFY_DB_PASSWORD", DB_PASSWORD),
            ("SPOTIFY_FOLDER_PATH", SPOTIFY_FOLDER_PATH),
        ] if not value
    ]
    if missing:
        raise SystemExit(f"Missing required environment variables: {', '.join(missing)}")