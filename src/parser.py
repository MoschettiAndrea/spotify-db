import json
import pandas as pd


def load_json(path):
    """Load a Spotify Extended Streaming History JSON file."""
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)

    return pd.DataFrame(data)


def create_artists(df):
    """Create the artists table from Spotify streaming history."""

    artists = (
        df[["master_metadata_album_artist_name"]]
        .dropna()
        .drop_duplicates()
        .reset_index(drop=True)
        .rename(columns={
            "master_metadata_album_artist_name": "name"
        })
    )

    artists.insert(0, "artist_id", range(1, len(artists) + 1))

    return artists


def create_albums(df, artists):
    """Create the albums table from Spotify streaming history."""

    artist_id_map = artists.set_index("name")["artist_id"]

    albums = (
        df[
            [
                "master_metadata_album_artist_name",
                "master_metadata_album_album_name",
            ]
        ]
        .dropna()
        .drop_duplicates()
        .rename(columns={
            "master_metadata_album_artist_name": "artist_name",
            "master_metadata_album_album_name": "name",
        })
    )

    albums["artist_id"] = albums["artist_name"].map(artist_id_map)

    albums = albums[
        ["artist_id", "name"]
    ].reset_index(drop=True)

    albums.insert(0, "album_id", range(1, len(albums) + 1))

    return albums


def create_songs(df, artists, albums):
    """Create the songs table from Spotify streaming history."""

    album_id_map = (
        albums
        .set_index(["artist_id", "name"])["album_id"]
    )

    songs = (
        df[
            [
                "spotify_track_uri",
                "master_metadata_track_name",
                "master_metadata_album_album_name",
                "master_metadata_album_artist_name",
            ]
        ]
        .dropna(subset=["spotify_track_uri"])
        .drop_duplicates("spotify_track_uri")
        .rename(columns={
            "master_metadata_track_name": "name",
            "master_metadata_album_album_name": "album_name",
            "master_metadata_album_artist_name": "artist_name",
        })
    )

    artist_id_map = artists.set_index("name")["artist_id"]

    songs["artist_id"] = songs["artist_name"].map(artist_id_map)

    songs["album_id"] = songs.set_index(
        ["artist_id", "album_name"]
    ).index.map(album_id_map)

    songs = songs[
        [
            "name",
            "album_id",
            "spotify_track_uri",
        ]
    ].reset_index(drop=True)

    songs.insert(0, "song_id", range(1, len(songs) + 1))

    return songs


def create_users():
    """Create the users table."""

    return pd.DataFrame({
        "user_id": [1],
        "username": ["Andrea"],
    })


def create_platforms(df):
    """Create the platforms table."""

    platforms = (
        df[["platform"]]
        .dropna()
        .drop_duplicates()
        .reset_index(drop=True)
    )

    platforms.insert(
        0,
        "platform_id",
        range(1, len(platforms) + 1),
    )

    platforms.insert(1, "user_id", 1)

    return platforms


def create_listens(df, songs, platforms):
    """Create the listens table."""

    listens = df[
        [
            "ts",
            "platform",
            "spotify_track_uri",
            "ms_played",
            "conn_country",
            "ip_addr",
            "reason_start",
            "reason_end",
            "shuffle",
            "skipped",
            "offline",
            "offline_timestamp",
            "incognito_mode",
        ]
    ].copy()

    platform_id_map = (
        platforms
        .set_index("platform")["platform_id"]
    )

    song_id_map = (
        songs
        .set_index("spotify_track_uri")["song_id"]
    )

    listens["platform_id"] = listens["platform"].map(
        platform_id_map
    )

    listens["song_id"] = listens["spotify_track_uri"].map(
        song_id_map
    )

    listens = listens[
        [
            "song_id",
            "platform_id",
            "ts",
            "ms_played",
            "conn_country",
            "ip_addr",
            "reason_start",
            "reason_end",
            "shuffle",
            "skipped",
            "offline",
            "offline_timestamp",
            "incognito_mode",
        ]
    ].reset_index(drop=True)

    listens.insert(
        0,
        "listen_id",
        range(1, len(listens) + 1),
    )

    listens["ts"] = pd.to_datetime(
        listens["ts"],
        utc=True,
    )

    return listens