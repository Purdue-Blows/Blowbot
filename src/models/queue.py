import sqlite3
from typing import Any, List, Dict

from models.songs import Song
from models.users import User


# A model for the queue table
# Note that the entire queue isn't loaded into memory because it's already in the database,
# This is just more of a utility model to ensure that the data
# flows smoothly and correctly
class Queue:
    def __init__(self, song: Song, audio: bytes, user: User) -> None:
        self.song = song
        self.audio = audio
        self.user = user

    @staticmethod
    def from_map(map: Dict[str, Any]) -> "Queue":
        return Queue(song=map["song"], audio=map["audio"], user=map["user"])

    # Adds a queue instance to the queue table
    @staticmethod
    async def add(queue: "Queue") -> None:
        pass

    @staticmethod
    async def retrieve_many() -> List["Queue"]:
        # TODO: Retrieve the values that match the most specified params for the queue table, in order
        pass

    @staticmethod
    async def retrieve_one(
        index: int, played: bool = False, random: bool = True
    ) -> "Queue":
        # TODO: Retrieve the next song in the queue (the song with the smallest id)
        pass

    @staticmethod
    async def clear_queue() -> None:
        # TODO: Clear the queue table
        pass

    # Removes a song from the queue table (shifting all the songs up 1)
    @staticmethod
    async def remove_song() -> None:
        # TODO: Removes a song from the queue table (shifting all the songs up 1)
        # TODO: you can only remove a song from the queue if you added it or you are an admin
        # TODO:
        pass

    @staticmethod
    async def update(queue: "Queue") -> None:
        # TODO: updates the corresponding queue instance in the database
        pass
