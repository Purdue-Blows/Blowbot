import sqlite3
from typing import Optional, List


class Song:
    def __init__(
        self,
        name: Optional[str],
        artist: Optional[str],
        url: str,
        album: Optional[str],
        release_date: Optional[str],
    ):
        self.name = name
        self.artist = artist
        # TODO: If url already in database, throw a ValueError
        self.url = url
        self.album = album
        self.release_date = release_date
        pass

    @staticmethod
    def from_map(map: dict) -> "Song":
        return Song(
            map["name"], map["artist"], map["url"], map["album"], map["release_date"]
        )

    # Add the song to the database
    @staticmethod
    async def add(song: "Song") -> None:
        pass

    @staticmethod
    async def retrieve_many(
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> List["Song"]:
        # TODO: Retrieve the values that match the most specified params for the songs table, in order
        pass

    @staticmethod
    async def retrieve_one(
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> Optional["Song"]:
        # TODO: Retrieve the value that matches the most specified parameters for the songs table
        pass

    @staticmethod
    async def update(song: "Song") -> None:
        # TODO: updates the corresponding song instance in the database
        pass

    @staticmethod
    async def format_song(song: "Song") -> str:
        # TODO: format song information in a readable way given a song
        # and return the string
        pass
