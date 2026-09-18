import pandas as pd
from src.config import validate, SPOTIFY_FOLDER_PATH, USERNAME
from src.database import create_engine_connection, read_table, insert_new_rows
from src.parser import (
    load_json_folder, create_users, create_artists, create_albums,
    create_songs, create_platforms, create_listens,
)
from src.sync import reconcile


def main():
    validate()
    df = load_json_folder(SPOTIFY_FOLDER_PATH)
    engine = create_engine_connection()

    # --- users ---
    existing_users = read_table(engine, "users")
    user_id_map, users_new = reconcile(
        create_users(USERNAME), existing_users, ["username"], "user_id"
    )
    users_full = pd.concat([existing_users, users_new], ignore_index=True)

    # --- artists ---
    existing_artists = read_table(engine, "artists")
    artist_id_map, artists_new = reconcile(
        create_artists(df), existing_artists, ["name"], "artist_id"
    )
    artists_full = pd.concat([existing_artists, artists_new], ignore_index=True)

    # --- albums (built against the FULL artist reference, not the fresh one) ---
    existing_albums = read_table(engine, "albums")
    album_id_map, albums_new = reconcile(
        create_albums(df, artists_full), existing_albums, ["artist_id", "name"], "album_id"
    )
    albums_full = pd.concat([existing_albums, albums_new], ignore_index=True)

    # --- songs ---
    existing_songs = read_table(engine, "songs")
    song_id_map, songs_new = reconcile(
        create_songs(df, artists_full, albums_full), existing_songs,
        ["spotify_track_uri"], "song_id",
    )
    songs_full = pd.concat([existing_songs, songs_new], ignore_index=True)

    # --- platforms ---
    user_id = user_id_map.loc[USERNAME]

    existing_platforms = read_table(engine, "platforms")
    platform_id_map, platforms_new = reconcile(
        create_platforms(df, user_id=user_id), existing_platforms,
        ["user_id", "platform"], "platform_id",
    )
    platforms_full = pd.concat([existing_platforms, platforms_new], ignore_index=True)

    # --- listens (key = everything except listen_id) ---
    existing_listens = read_table(engine, "listens")
    listens_candidate = create_listens(df, songs_full, platforms_full)
    key_cols = [c for c in listens_candidate.columns if c != "listen_id"]
    _, listens_new = reconcile(listens_candidate, existing_listens, key_cols, "listen_id")

    insert_new_rows(engine, users_new, artists_new, albums_new, songs_new, platforms_new, listens_new)


if __name__ == "__main__":
    main()