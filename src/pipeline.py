import pandas as pd
from .database import read_table, insert_new_rows, align_dtypes
from .parser import (
    create_users, create_artists, create_albums, create_songs,
    create_platforms, create_listens,
)
from .sync import reconcile


def sync_database(engine, df, username):
    """Reconcile parsed data against whatever's already in the DB (which
    may be nothing, on a fresh DB) and insert only what's new."""

    existing_users = read_table(engine, "users")
    user_id_map, users_new = reconcile(
        create_users(username), existing_users, ["username"], "user_id"
    )
    user_id = user_id_map.loc[username]

    existing_artists = read_table(engine, "artists")
    artist_id_map, artists_new = reconcile(
        create_artists(df), existing_artists, ["name"], "artist_id"
    )
    artists_full = pd.concat([existing_artists, artists_new], ignore_index=True)

    existing_albums = read_table(engine, "albums")
    album_id_map, albums_new = reconcile(
        create_albums(df, artists_full), existing_albums, ["artist_id", "name"], "album_id"
    )
    albums_full = pd.concat([existing_albums, albums_new], ignore_index=True)

    existing_songs = read_table(engine, "songs")
    song_id_map, songs_new = reconcile(
        create_songs(df, artists_full, albums_full), existing_songs,
        ["spotify_track_uri"], "song_id",
    )
    songs_full = pd.concat([existing_songs, songs_new], ignore_index=True)

    existing_platforms = read_table(engine, "platforms")
    platform_id_map, platforms_new = reconcile(
        create_platforms(df, user_id=user_id), existing_platforms,
        ["user_id", "platform"], "platform_id",
    )
    platforms_full = pd.concat([existing_platforms, platforms_new], ignore_index=True)

    existing_listens = read_table(engine, "listens")
    listens_candidate = align_dtypes(create_listens(df, songs_full, platforms_full), "listens")
    key_cols = [c for c in listens_candidate.columns if c != "listen_id"]
    _, listens_new = reconcile(listens_candidate, existing_listens, key_cols, "listen_id")

    insert_new_rows(engine, users_new, artists_new, albums_new, songs_new, platforms_new, listens_new)