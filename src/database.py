import pandas as pd
from sqlalchemy import create_engine, text, Boolean, DateTime, Integer, BigInteger
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

def align_dtypes(df, table_name):
    """Normalize a DataFrame's dtypes to a single schema-driven policy, so
    dtype-based comparisons in sync.reconcile are meaningful regardless of
    whether the data came from parsing JSON or reading the DB back."""
    df = df.copy()
    table = Base.metadata.tables[table_name]

    for column in table.columns:
        if column.name not in df.columns:
            continue
        if isinstance(column.type, Boolean):
            df[column.name] = df[column.name].astype(bool)
        elif isinstance(column.type, DateTime):
            df[column.name] = (
                pd.to_datetime(df[column.name], utc=True)
                .dt.tz_localize(None)
                .astype("datetime64[us]")
            )
        elif isinstance(column.type, (Integer, BigInteger)) and column.nullable:
            df[column.name] = df[column.name].astype("float64")

    return df


def read_table(engine, table_name):
    df = pd.read_sql_table(table_name, engine)
    return align_dtypes(df, table_name)

def insert_new_rows(engine, users, artists, albums, songs, platforms, listens):
    """Insert only the new rows for each table, skipping empty frames.
    All inserts happen in a single transaction: a failure partway through
    rolls back everything, rather than leaving the DB partially updated."""
    tables = {
        "users": users,
        "artists": artists,
        "albums": albums,
        "songs": songs,
        "platforms": platforms,
        "listens": listens,
    }
    with engine.begin() as connection:
        for name, frame in tables.items():
            if frame.empty:
                continue
            frame.to_sql(name, connection, if_exists="append", index=False)


def insert_tables(engine, users, artists, albums, songs, platforms, listens):
    """Insert the prepared DataFrames into the database, as one transaction."""
    tables = {
        "users": users,
        "artists": artists,
        "albums": albums,
        "songs": songs,
        "platforms": platforms,
        "listens": listens,
    }
    with engine.begin() as connection:
        for name, frame in tables.items():
            frame.to_sql(name, connection, if_exists="append", index=False)