from enum import Enum
from typing import Any, List, Dict, Union, Optional
from pymongo.errors import DuplicateKeyError

from models.songs import Song
from models.users import User
from models.model_fields import QueueFields
from models.playlist import Playlist


# A model for the queue table
# Note that the entire queue isn't loaded into memory because it's already in the database,
# This is just more of a utility model to ensure that the data
# flows smoothly and correctly
class Queue:
    def __init__(
        self,
        song: Song,
        user: User,
        queue_num: int,
        played: bool = False,
        id: Optional[int] = None,
    ) -> None:
        self.song = song
        self.user = user
        self.id = id
        self.queue_num = queue_num
        self.played = played

    # Asynchronous constructor
    @staticmethod
    async def create_queue(
        db, song: Song, audio: bytes, user: User, id: Optional[int] = None
    ) -> "Queue":
        queue_num = await Queue.get_queue_num(db)
        return Queue(
            song=song,
            user=user,
            id=id,
            queue_num=queue_num,
            played=False,
        )

    @staticmethod
    async def get_queue_num(db) -> int:
        highest_queue = await db.queue.find_one(sort=[(QueueFields.QUEUE_NUM.name, -1)])
        print(highest_queue)
        if highest_queue:
            queue_num = highest_queue[QueueFields.QUEUE_NUM.name]
            return queue_num + 1
        else:
            return 1

    @staticmethod
    def log_doc(queue: dict) -> None:
        print("QUEUE DOC")
        print(f"Id: {queue[QueueFields.ID.name]}")
        print(f"Song Id: {queue[QueueFields.SONG_ID.name]}")
        print(f"User Id: {queue[QueueFields.USER_ID.name]}")
        print(f"Queue Num: {queue[QueueFields.QUEUE_NUM.name]}")
        print(f"Played: {queue[QueueFields.PLAYED.name]}")

    @staticmethod
    async def from_map(db, map: Dict[str, Any]) -> "Queue":
        song = await Song.retrieve_one(id=map[QueueFields.SONG_ID.name])
        user = await User.retrieve_one(db, id=map[QueueFields.USER_ID.name])
        if song is None:
            raise ValueError("Song not found")
        if user is None:
            raise ValueError("User not found")
        return Queue(
            id=map[QueueFields.ID.name],
            song=song,
            user=user,
            queue_num=map[QueueFields.QUEUE_NUM.name],
            played=map[QueueFields.PLAYED.name],
        )

    # Adds a queue instance to the queue table
    @staticmethod
    async def add(db, queue: "Queue") -> Optional["Queue"]:
        # TODO: Check that song id and user id are in the database
        try:
            collection = db["queue"]
            # If the song isn't already in songs, add it
            song = await Song.add(queue.song)

            if song:
                result = await collection.insert_one(
                    {
                        QueueFields.SONG_ID.name: song.id,
                        QueueFields.USER_ID.name: queue.user.id,
                        QueueFields.QUEUE_NUM.name: queue.queue_num,
                        QueueFields.PLAYED.name: queue.played,
                    }
                )
                queue.id = result.inserted_id
            return queue
        except DuplicateKeyError:
            print("Duplicate key error; adding playlist")
            if queue.song.id is None:
                song = await Song.retrieve_one(url=queue.song.url)
                if song != None:
                    queue.song.id = song.id
            await collection.insert_one(
                {
                    QueueFields.SONG_ID.name: queue.song.id,
                    QueueFields.USER_ID.name: queue.user.id,
                    QueueFields.QUEUE_NUM.name: queue.queue_num,
                    QueueFields.PLAYED.name: queue.played,
                }
            )
            return queue

    @staticmethod
    async def retrieve_many(
        db,
        song_ids: Optional[List[int]] = None,
        played: Optional[bool] = None,
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> Optional[List["Queue"]]:
        if (
            song_ids is None
            and played is None
            and user_id is None
            and url is None
            and name is None
            and album is None
            and artist is None
            and release_date is None
        ):
            playlists = []
            async for document in db.playlist.find():
                playlist = Playlist.from_map(db, document)
                playlists.append(playlist)
            return playlists
        collection = db["queue"]
        query = {}
        if song_ids is not None:
            query[QueueFields.SONG_ID.name] = {"$in": song_ids}
        if played is not None:
            query[QueueFields.PLAYED.name] = played
        if user_id:
            query[QueueFields.USER_ID.name] = user_id

        queues = []
        async for document in collection.find(query):
            queues.append(await Queue.from_map(db, document))
        return queues

    @staticmethod
    async def retrieve_one(
        db,
        id: Optional[int] = None,
        song_id: Optional[int] = None,
        played: Optional[bool] = None,
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> Optional["Queue"]:
        if song_id is None and (
            url is not None
            or name is not None
            or artist is not None
            or album is not None
            or release_date is not None
            or song_id
        ):
            try:
                song = await Song.retrieve_one(
                    url=url,
                    name=name,
                    artist=artist,
                    album=album,
                    release_date=release_date,
                )
                if song:
                    song_id = song.id if song.id is not None else None
            except Exception as e:
                pass
        collection = db["queue"]
        query = {}
        if id:
            query[QueueFields.ID.name] = id
        if song_id:
            query[QueueFields.SONG_ID.name] = song_id
        if played is not None:
            query[QueueFields.PLAYED.name] = played
        if user_id:
            query[QueueFields.USER_ID.name] = user_id
        queue_doc = await collection.find_one(query)
        if queue_doc:
            queue = await Queue.from_map(db, queue_doc)
        return queue

    @staticmethod
    async def clear_queue(db) -> None:
        collection = db["queue"]
        await collection.delete_many({})

    @staticmethod
    async def remove_song(db, queue: "Queue") -> None:
        collection = db["queue"]
        await collection.delete_one({QueueFields.ID.name: queue.id})

    @staticmethod
    async def update(db, queue: "Queue") -> Optional["Queue"]:
        collection = db["queue"]
        await Song.update(queue.song)
        await collection.update_one(
            {"_id": queue.id},
            {
                "$set": {
                    QueueFields.SONG_ID.name: queue.song.id,
                    QueueFields.USER_ID.name: queue.user.id,
                    QueueFields.QUEUE_NUM.name: queue.queue_num,
                    QueueFields.PLAYED.name: queue.played,
                }
            },
        )
        return queue

    def to_string(self):
        return (
            "QUEUE\n"
            + QueueFields.ID.name
            + str(self.id)
            + "\n Song: "
            + self.song.to_string()
            + "\n User:"
            + self.user.to_string()
            + "\n Queue Num: "
            + str(self.queue_num)
            + "\n Played: "
            + str(self.played)
        )
