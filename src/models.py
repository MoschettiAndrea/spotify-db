from sqlalchemy import (
    BigInteger,
    Boolean,
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
)
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True)
    username = Column(String(100), nullable=False)


class Artist(Base):
    __tablename__ = "artists"

    artist_id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)


class Album(Base):
    __tablename__ = "albums"

    album_id = Column(Integer, primary_key=True)
    artist_id = Column(
        Integer,
        ForeignKey("artists.artist_id"),
        nullable=False,
    )
    name = Column(String(255), nullable=False)


class Song(Base):
    __tablename__ = "songs"

    song_id = Column(Integer, primary_key=True)
    album_id = Column(
        Integer,
        ForeignKey("albums.album_id"),
        nullable=False,
    )
    name = Column(String(255), nullable=False)
    spotify_track_uri = Column(String(100), nullable=False)


class Platform(Base):
    __tablename__ = "platforms"

    platform_id = Column(Integer, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey("users.user_id"),
        nullable=False,
    )
    platform = Column(String(255), nullable=False)


class Listen(Base):
    __tablename__ = "listens"

    listen_id = Column(Integer, primary_key=True)
    song_id = Column(
        Integer,
        ForeignKey("songs.song_id"),
        nullable=False,
    )
    platform_id = Column(
        Integer,
        ForeignKey("platforms.platform_id"),
        nullable=False,
    )

    ts = Column(DateTime, nullable=False)
    ms_played = Column(Integer)
    conn_country = Column(String(2))
    ip_addr = Column(String(45))
    reason_start = Column(String(50))
    reason_end = Column(String(50))
    shuffle = Column(Boolean)
    skipped = Column(Boolean)
    offline = Column(Boolean)
    offline_timestamp = Column(BigInteger)
    incognito_mode = Column(Boolean)