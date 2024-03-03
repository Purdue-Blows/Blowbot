import sqlite3
from typing import Dict, Any, List, Union


from models.songs import Song
from models.users import User


class Playlist:
    def __init__(self, song: Song, audio: bytes, played: bool, user: User) -> None:
        self.song = song
        self.audio = audio
        self.played = played
        self.user = user

    @staticmethod
    def from_map(map: Dict[str, Any]) -> "Playlist":
        return Playlist(
            song=map["song"], audio=map["audio"], played=map["played"], user=map["user"]
        )

    @staticmethod
    async def add(playlist: "Playlist") -> None:
        pass

    @staticmethod
    async def retrieve_many() -> List["Playlist"]:
        pass

    @staticmethod
    async def retrieve_one(played: bool = False, random: bool = True) -> "Playlist":
        pass

    @staticmethod
    async def reset_playlist() -> None:
        pass

    @staticmethod
    async def remove_song() -> None:
        pass

    @staticmethod
    async def update(playlist: "Playlist") -> None:
        pass
