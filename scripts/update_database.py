from src.config import validate, SPOTIFY_FOLDER_PATH, USERNAME
from src.database import create_engine_connection
from src.parser import load_json_folder
from src.pipeline import sync_database


def main():
    validate()
    df = load_json_folder(SPOTIFY_FOLDER_PATH)
    engine = create_engine_connection()

    sync_database(engine, df, USERNAME)


if __name__ == "__main__":
    main()