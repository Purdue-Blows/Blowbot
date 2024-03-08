from enum import Enum
from typing import Optional, List, Union
from models.model_fields import SongFields

from utils.constants import DB_CLIENT


class Song:
    def __init__(
        self,
        url: str,
        name: Optional[str] = None,
        audio: Optional[bytes] = None,
        artist: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
        id: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.artist = artist
        self.url = url
        self.album = album
        self.release_date = release_date
        self.audio = audio

    @staticmethod
    def log_doc(song: dict) -> None:
        print("SONG DOC")
        print(f"Id: {song[SongFields.ID.name]}")
        print(f"Name: {song[SongFields.NAME.name]}")
        print(f"Artist: {song[SongFields.ARTIST.name]}")
        print(f"Audio: {str(song[SongFields.AUDIO.name])[0:20]}")
        print(f"URL: {song[SongFields.URL.name]}")
        print(f"Album: {song[SongFields.ALBUM.name]}")
        print(f"Release Date: {song[SongFields.RELEASE_DATE.name]}")

    @staticmethod
    def from_map(map: dict) -> "Song":
        return Song(
            map[SongFields.ID.name],
            map[SongFields.NAME.name],
            map[SongFields.ARTIST.name],
            map[SongFields.URL.name],
            map[SongFields.ALBUM.name],
            map[SongFields.RELEASE_DATE.name],
            map[SongFields.AUDIO.name],
        )

    # Add the song to the database
    @staticmethod
    async def add(song: "Song") -> Optional["Song"]:
        collection = DB_CLIENT.songs.songs
        result = await collection.insert_one(
            {
                SongFields.NAME.name: song.name,
                SongFields.ARTIST.name: song.artist,
                SongFields.URL.name: song.url,
                SongFields.AUDIO.name: song.audio,
                SongFields.ALBUM.name: song.album,
                SongFields.RELEASE_DATE.name: song.release_date,
            }
        )
        song.id = result.inserted_id
        return song

    @staticmethod
    async def retrieve_many(
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> List["Song"]:
        try:
            collection = DB_CLIENT.songs.songs
            query = {}

            if name is not None:
                query[SongFields.NAME.name] = name
            if artist is not None:
                query[SongFields.ARTIST.name] = artist
            if url is not None:
                query[SongFields.URL.name] = url
            if album is not None:
                query[SongFields.ALBUM.name] = album
            if release_date is not None:
                query[SongFields.RELEASE_DATE.name] = release_date

            results = await collection.find(query).to_list(length=None)

            return [Song.from_map(result) for result in results]
        except Exception as e:
            print(f"Error occurred while retrieving songs: {e}")
            return []

    @staticmethod
    async def retrieve_one(
        id: Optional[int] = None,
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> Optional["Song"]:
        collection = DB_CLIENT.songs.songs
        query = {}

        if id:
            query[SongFields.ID.name] = id
        if name:
            query[SongFields.NAME.name] = name
        if artist:
            query[SongFields.ARTIST.name] = artist
        if url:
            query[SongFields.URL.name] = url
        if album:
            query[SongFields.ALBUM.name] = album
        if release_date:
            query[SongFields.RELEASE_DATE.name] = release_date

        result = await collection.find_one(query)

        return Song.from_map(result) if result else None

    @staticmethod
    async def update(song: "Song") -> Optional["Song"]:
        collection = DB_CLIENT.songs.songs
        await collection.update_one(
            {"id": song.id},
            {
                "$set": {
                    SongFields.NAME.name: song.name,
                    SongFields.ARTIST.name: song.artist,
                    SongFields.AUDIO.name: song.audio,
                    SongFields.URL.name: song.url,
                    SongFields.ALBUM.name: song.album,
                    SongFields.RELEASE_DATE.name: song.release_date,
                }
            },
        )
        return song

    @staticmethod
    def format_song(song: "Song") -> str:
        return f"Name: {song.name}\nArtist: {song.artist}\nURL: {song.url}\nAlbum: {song.album}\nRelease Date: {song.release_date}"

    def to_string(self) -> str:
        return f"SONG\nName: {self.name}\nArtist: {self.artist}\nURL: {self.url}\nAlbum: {self.album}\nRelease Date: {self.release_date}"
