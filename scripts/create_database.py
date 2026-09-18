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
    load_json,
)


from src.config import DB_PASSWORD, JSON_PATH, USERNAME


def main():
    if not DB_PASSWORD:
        raise SystemExit(
            "Set SPOTIFY_DB_PASSWORD before running this script."
        )

    if not JSON_PATH:
        raise SystemExit(
            "Set SPOTIFY_JSON_PATH before running this script."
        )
    df = load_json(JSON_PATH)

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