import pandas as pd
from sqlalchemy import create_engine, text, Boolean
from .models import Base
from .config import DB_USER, DB_PASSWORD, DB_HOST, DB_NAME


def _connection_url(database=None):
    base = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/"
    return f"{base}{database}" if database else base

def create_engine_connection(database=DB_NAME):
    return create_engine(_connection_url(database))

def create_database(database=DB_NAME):
    engine = create_engine(_connection_url())
    with engine.connect() as connection:
        connection.execute(text(f"CREATE DATABASE IF NOT EXISTS {database}"))

def create_tables(engine):
    """Create all database tables."""

    Base.metadata.create_all(engine)

def read_table(engine, table_name):
    df = pd.read_sql_table(table_name, engine)

    table = Base.metadata.tables[table_name]
    bool_cols = [c.name for c in table.columns if isinstance(c.type, Boolean)]
    for col in bool_cols:
        df[col] = df[col].astype(bool)

    return df

# src/database.py
def insert_new_rows(
    engine,
    users,
    artists,
    albums,
    songs,
    platforms,
    listens,
):
    """Insert only the new rows for each table, skipping empty frames."""
    tables = {
        "users": users,
        "artists": artists,
        "albums": albums,
        "songs": songs,
        "platforms": platforms,
        "listens": listens,
    }
    for name, frame in tables.items():
        if frame.empty:
            continue
        frame.to_sql(name, engine, if_exists="append", index=False)


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