from sqlalchemy import create_engine, text

from .models import Base


def create_database(database="spotify_db"):
    """Create the MySQL database if it does not already exist."""

    engine = create_engine(
        "mysql+pymysql://root:root@localhost/"
    )

    with engine.connect() as connection:
        connection.execute(
            text(f"CREATE DATABASE IF NOT EXISTS {database}")
        )


def create_engine_connection(database="spotify_db"):
    """Create a SQLAlchemy engine for the Spotify database."""

    return create_engine(
        f"mysql+pymysql://root:root@localhost/{database}"
    )


def create_tables(engine):
    """Create all database tables."""

    Base.metadata.create_all(engine)


def insert_tables(
    engine,
    users,
    artists,
    albums,
    songs,
    platforms,
    listens,
):
    """Insert the prepared DataFrames into the database."""

    users.to_sql(
        "users",
        engine,
        if_exists="append",
        index=False,
    )

    artists.to_sql(
        "artists",
        engine,
        if_exists="append",
        index=False,
    )

    albums.to_sql(
        "albums",
        engine,
        if_exists="append",
        index=False,
    )

    songs.to_sql(
        "songs",
        engine,
        if_exists="append",
        index=False,
    )

    platforms.to_sql(
        "platforms",
        engine,
        if_exists="append",
        index=False,
    )

    listens.to_sql(
        "listens",
        engine,
        if_exists="append",
        index=False,
    )