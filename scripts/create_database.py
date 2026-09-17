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


JSON_PATH = (
    "C:/Users/Andrea/Desktop/Spotify Data/"
    "Spotify Extended Streaming History/"
    "Streaming_History_Audio_2015-2016_0.json"
)


def main():
    df = load_json(JSON_PATH)

    users = create_users()
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