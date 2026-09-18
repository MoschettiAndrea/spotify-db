from src.database import (
    create_database,
    create_engine_connection,
    create_tables,
    insert_tables,
)
from src.parser import (
    create_albums,
    create_artists,
    create_listens,
    create_platforms,
    create_songs,
    create_users,
    load_json_folder,
)
from src.config import validate, SPOTIFY_FOLDER_PATH, USERNAME


def main():
    validate()

    try:
        df = load_json_folder(SPOTIFY_FOLDER_PATH)
    except FileNotFoundError as e:
        raise SystemExit(str(e))

    users = create_users(USERNAME)
    artists = create_artists(df)
    albums = create_albums(df, artists)
    songs = create_songs(df, artists, albums)
    platforms = create_platforms(df)
    listens = create_listens(df, songs, platforms)

    create_database()

    engine = create_engine_connection()

    create_tables(engine)

    insert_tables(
        engine,
        users,
        artists,
        albums,
        songs,
        platforms,
        listens,
    )


if __name__ == "__main__":
    main()