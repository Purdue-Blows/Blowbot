from enum import Enum
from typing import Optional, List, Union
from models.model_fields import SongFields

from utils.constants import Base, ydl
from services.download_song_from_youtube import download_song_from_youtube
from sqlalchemy.orm import Session
from sqlalchemy import Column, Integer, String, LargeBinary
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session
from sqlalchemy.util import concurrency


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    name = Column(String, nullable=False)
    artist = Column(String)
    url = Column(String, nullable=False, unique=True)
    album = Column(String)
    release_date = Column(String)
    audio = Column(LargeBinary, nullable=False)

    @staticmethod
    def from_map(map: dict) -> "Song":
        return Song(
            id=map[SongFields.ID.value],
            name=map[SongFields.NAME.value],
            artist=map[SongFields.ARTIST.value],
            url=map[SongFields.URL.value],
            album=map[SongFields.ALBUM.value],
            release_date=map[SongFields.RELEASE_DATE.value],
            audio=map[SongFields.AUDIO.value],
        )

    @staticmethod
    def add_sync(session: Session, song: "Song") -> "Song":
        try:
            session.add(song)
            session.commit()
            return song
        except Exception as e:
            session.rollback()
            print(f"Error occurred while adding song: {e}")
            raise e

    @staticmethod
    async def add(session: Session, song: "Song"):
        return await concurrency.greenlet_spawn(Song.add_sync, session, song)

    @staticmethod
    def retrieve_many_sync(
        session: Session,
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> List["Song"]:
        try:
            query = session.query(Song)

            if name is not None:
                query = query.filter(Song.name == name)
            if artist is not None:
                query = query.filter(Song.artist == artist)
            if url is not None:
                query = query.filter(Song.url == url)
            if album is not None:
                query = query.filter(Song.album == album)
            if release_date is not None:
                query = query.filter(Song.release_date == release_date)

            results = query.all()

            return results
        except Exception as e:
            session.rollback()
            print(f"Error occurred while retrieving songs: {e}")
            return []

    @staticmethod
    async def retrieve_many(
        session: Session,
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> List["Song"]:
        return await concurrency.greenlet_spawn(
            Song.retrieve_many_sync, session, name, artist, url, album, release_date
        )

    @staticmethod
    def retrieve_one_sync(
        session: Session,
        id: Optional[int] = None,
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> "Song":
        try:
            print("Before initial song query")
            query = session.query(Song)

            if id:
                query = query.filter(Song.id == id)
            if name:
                query = query.filter(Song.name == name)
            if artist:
                query = query.filter(Song.artist == artist)
            if url:
                query = query.filter(Song.url == url)
            if album:
                query = query.filter(Song.album == album)
            if release_date:
                query = query.filter(Song.release_date == release_date)

            print("Before song query retrieval")
            result = query.first()
            print("After song query retrieval")

            return result
        except Exception as e:
            session.rollback()
            print(f"Error occurred while retrieving song: {e}")
            raise e

    @staticmethod
    async def retrieve_one(
        session: Session,
        id: Optional[int] = None,
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> "Song":
        return await concurrency.greenlet_spawn(
            Song.retrieve_one_sync, session, id, name, artist, url, album, release_date
        )

    @staticmethod
    def update_sync(session: Session, song: "Song") -> bool:
        try:
            update = session.merge(song)
            if update:
                session.commit()
                return True
            session.rollback()
            return False
        except Exception as e:
            session.rollback()
            print(f"Error occurred while updating song: {e}")
            return False

    @staticmethod
    async def update(session: Session, song: "Song") -> bool:
        return await concurrency.greenlet_spawn(Song.update_sync, session, song)

    @staticmethod
    def log_map(song: dict) -> None:
        print("SONG")
        print(f"Id: {song[SongFields.ID.value]}")
        print(f"Name: {song[SongFields.NAME.value]}")
        print(f"Artist: {song[SongFields.ARTIST.value]}")
        print(f"Audio: {str(song[SongFields.AUDIO.value])[0:20]}")
        print(f"URL: {song[SongFields.URL.value]}")
        print(f"Album: {song[SongFields.ALBUM.value]}")
        print(f"Release Date: {song[SongFields.RELEASE_DATE.value]}")

    @staticmethod
    def format_song(song: "Song") -> str:
        audio_preview = song.audio[0:20] if song.audio is not None else None
        return f"Name: {song.name}\nArtist: {song.artist}\nURL: {song.url}\nAlbum: {song.album}\nRelease Date: {song.release_date}\nAudio: {audio_preview}"

    def to_string(self) -> str:
        audio_preview = self.audio[0:20] if self.audio is not None else None
        return f"SONG\nName: {self.name}\nArtist: {self.artist}\nURL: {self.url}\nAlbum: {self.album}\nRelease Date: {self.release_date}\nAudio: {audio_preview}"
