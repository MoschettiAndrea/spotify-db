from src.config import validate, SPOTIFY_FOLDER_PATH, USERNAME
from src.database import create_database, create_engine_connection, create_tables
from src.parser import load_json_folder
from src.pipeline import sync_database


def main():
    validate()
    try:
        df = load_json_folder(SPOTIFY_FOLDER_PATH)
    except FileNotFoundError as e:
        raise SystemExit(str(e))

    create_database()
    engine = create_engine_connection()
    create_tables(engine)

    sync_database(engine, df, USERNAME)


if __name__ == "__main__":
    main()