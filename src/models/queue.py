from calendar import c
from enum import Enum
from typing import Any, List, Dict, Union, Optional
from psycopg import IntegrityError

from models.songs import Song
from models.users import User
from models.model_fields import QueueFields
from models.playlist import Playlist
from sqlalchemy import BigInteger, Column, Integer, Boolean, ForeignKey
from sqlalchemy.orm import relationship, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.util import concurrency

from utils.constants import Base

SONG_NOT_FOUND = "Song not found"

# A model for the queue table
# Note that the entire queue isn't loaded into memory because it's already in the database,
# This is just more of a utility model to ensure that the data
# flows smoothly and correctly


class Queue(Base):
    __tablename__ = "queues"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    song_id = Column(Integer, ForeignKey("songs.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    guild_id = Column(BigInteger, nullable=False)
    queue_num = Column(Integer, nullable=False)
    played = Column(Boolean, nullable=False)

    song = relationship("Song")
    user = relationship("User")

    # Asynchronous constructor
    @staticmethod
    def get_next_queue_num_sync(session: Session, guild_id) -> int:
        try:
            highest_queue = (
                session.query(Queue)
                .order_by(Queue.queue_num.desc())
                .filter(Queue.guild_id == guild_id)
                .first()
            )
            if highest_queue:
                queue_num = highest_queue.queue_num
                return queue_num + 1  # type: ignore
            else:
                return 1
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def get_next_queue_num(session: Session, guild_id) -> int:
        return await concurrency.greenlet_spawn(
            Queue.get_next_queue_num_sync, session, guild_id
        )

    @staticmethod
    def get_next_song_sync(session: Session, guild_id) -> Optional[Song]:
        try:
            next_queue = (
                session.query(Queue)
                .filter(Queue.played == False, Queue.guild_id == guild_id)
                .order_by(Queue.queue_num.asc())
                .first()
            )
            if next_queue is not None:
                next_song = Song.retrieve_one_sync(session, id=next_queue.song.id)
                return next_song
            raise Exception(SONG_NOT_FOUND)
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def get_next_song(session: Session, guild_id) -> Optional[Song]:
        return await concurrency.greenlet_spawn(
            Queue.get_next_song_sync, session, guild_id
        )

    @staticmethod
    def get_previous_song_sync(session: Session, guild_id) -> Optional[Song]:
        try:
            previous_queue = (
                session.query(Queue)
                .filter(Queue.played == True, Queue.guild_id == guild_id)
                .order_by(Queue.queue_num.desc())
                .all()
            )[-2]
            if not previous_queue:
                raise Exception(SONG_NOT_FOUND)
            previous_song = Song.retrieve_one_sync(session, id=previous_queue.song.id)
            return previous_song
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def get_previous_song(session: Session, guild_id) -> Optional[Song]:
        return await concurrency.greenlet_spawn(
            Queue.get_previous_song_sync, session, guild_id
        )

    @staticmethod
    def get_current_song_sync(session: Session, guild_id) -> Optional[Song]:
        try:
            current_queue = (
                session.query(Queue)
                .filter(Queue.played == True, Queue.guild_id == guild_id)
                .order_by(Queue.queue_num.desc())
                .first()
            )
            if not current_queue:
                raise Exception(SONG_NOT_FOUND)
            current_song = Song.retrieve_one_sync(session, id=current_queue.song.id)
            return current_song
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def get_current_song(session: Session, guild_id) -> Optional[Song]:
        return await concurrency.greenlet_spawn(
            Queue.get_current_song_sync, session, guild_id
        )

    @staticmethod
    def from_map_sync(session: Session, map: Dict[str, Any]) -> "Queue":
        try:
            song = Song.retrieve_one_sync(session, id=map[QueueFields.SONG_ID.value])
            user = User.retrieve_one_sync(
                session,
                guild_id=map[QueueFields.GUILD_ID.value],
                id=map[QueueFields.USER_ID.value],
            )
            if song is None:
                raise ValueError("Song not found")
            if user is None:
                raise ValueError("User not found")
            return Queue(
                id=map[QueueFields.ID.value],
                song=song,
                user=user,
                queue_num=map[QueueFields.QUEUE_NUM.value],
                played=map[QueueFields.PLAYED.value],
                guild_id=map[QueueFields.GUILD_ID.value],
            )
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def from_map(session: Session, map: Dict[str, Any]) -> "Queue":
        return await concurrency.greenlet_spawn(Queue.from_map_sync, session, map)

    @staticmethod
    def add_sync(session: Session, queue: "Queue") -> Optional["Queue"]:
        try:
            song = Song.add_sync(session, queue.song)
            if queue.queue_num is None:
                queue.queue_num = Queue.get_next_queue_num_sync(session, queue.guild_id)  # type: ignore
            if song:
                queue.song_id = song.id
                session.add(queue)
                session.commit()
            return queue
        except IntegrityError:
            print("Duplicate key error; adding queue")
            if queue.song.id is None:
                song = Song.retrieve_one_sync(session, url=queue.song.url)
            queue_obj = Queue(
                song=song,
                played=queue.played,
                queue_num=queue.queue_num,
                user=queue.user,
                guild_id=queue.guild_id,
            )
            session.add(queue_obj)
            session.commit()
            return queue_obj
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def add(session: Session, queue: "Queue") -> Optional["Queue"]:
        return await concurrency.greenlet_spawn(Queue.add_sync, session, queue)

    @staticmethod
    def retrieve_many_sync(
        session: Session,
        guild_id,
        song_ids: Optional[List[int]] = None,
        played: Optional[bool] = None,
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> Optional[List["Queue"]]:
        try:
            query = (
                session.query(Queue)
                .join(Song, Queue.song_id == Song.id)
                .filter(Queue.guild_id == guild_id)
            )
            if song_ids is not None:
                query = query.filter(Queue.song_id.in_(song_ids))
            if played is not None:
                query = query.filter(Queue.played == played)
            if user_id:
                query = query.filter(Queue.user_id == user_id)
            if (
                url is not None
                or name is not None
                or artist is not None
                or album is not None
                or release_date is not None
            ):
                song = Song.retrieve_one_sync(
                    session,
                    url=url,
                    name=name,
                    artist=artist,
                    album=album,
                    release_date=release_date,
                )
                if song:
                    query = query.filter(Queue.song_id == song.id)
            return query.all()
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def retrieve_many(
        session: Session,
        guild_id,
        song_ids: Optional[List[int]] = None,
        played: Optional[bool] = None,
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> Optional[List["Queue"]]:
        return await concurrency.greenlet_spawn(
            Queue.retrieve_many_sync,
            session,
            guild_id,
            song_ids,
            played,
            name,
            artist,
            url,
            album,
            release_date,
            user_id,
        )

    @staticmethod
    def retrieve_one_sync(
        session: Session,
        guild_id,
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
        try:
            query = session.query(Queue).join(Song, Queue.song_id == Song.id)
            query = query.filter(Queue.guild_id == guild_id)
            if id:
                query = query.filter(Queue.id == id)
            if song_id:
                query = query.filter(Queue.song_id == song_id)
            if played is not None:
                query = query.filter(Queue.played == played)
            if user_id:
                query = query.filter(Queue.user_id == user_id)
            if (
                url is not None
                or name is not None
                or artist is not None
                or album is not None
                or release_date is not None
            ):
                song = Song.retrieve_one_sync(
                    session,
                    url=url,
                    name=name,
                    artist=artist,
                    album=album,
                    release_date=release_date,
                )
                if song:
                    query = query.filter(Queue.song_id == song.id)
            return query.first()
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def retrieve_one(
        session: Session,
        guild_id,
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
        return await concurrency.greenlet_spawn(
            Queue.retrieve_one_sync,
            session,
            guild_id,
            id,
            song_id,
            played,
            name,
            artist,
            url,
            album,
            release_date,
            user_id,
        )

    @staticmethod
    def clear_queue_sync(session: Session, guild_id) -> bool:
        try:
            session.query(Queue).filter(Queue.guild_id == guild_id).delete()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def clear_queue(session: Session, guild_id):
        return await concurrency.greenlet_spawn(
            Queue.clear_queue_sync, session, guild_id
        )

    @staticmethod
    def remove_queue_sync(session: Session, queue: "Queue") -> bool:
        try:
            session.query(Queue).filter(
                Queue.guild_id == queue.guild_id, Queue.id == queue.id
            ).delete()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def remove_queue(session: Session, queue: "Queue") -> bool:
        return await concurrency.greenlet_spawn(Queue.remove_queue_sync, session, queue)

    @staticmethod
    def update_sync(session: Session, queue: "Queue") -> bool:
        try:
            update = session.merge(queue)
            if update:
                session.commit()
                return True
            session.rollback()
            return False
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def update(session: Session, queue: "Queue") -> bool:
        return await concurrency.greenlet_spawn(Queue.update_sync, session, queue)

    @staticmethod
    def log_map(queue: dict) -> None:
        print("QUEUE")
        print(f"Id: {queue[QueueFields.ID.value]}")
        print(f"Song Id: {queue[QueueFields.SONG_ID.value]}")
        print(f"User Id: {queue[QueueFields.USER_ID.value]}")
        print(f"Queue Num: {queue[QueueFields.QUEUE_NUM.value]}")
        print(f"Played: {queue[QueueFields.PLAYED.value]}")
        print(f"Guild Id: {queue[QueueFields.GUILD_ID.value]}")

    def to_string(self):
        return (
            "QUEUE\n"
            + QueueFields.ID.value
            + str(self.id)
            + "\n Song: "
            + self.song.to_string()
            + "\n User:"
            + self.user.to_string()
            + "\n Queue Num: "
            + str(self.queue_num)
            + "\n Played: "
            + str(self.played)
            + "\n Guild Id: "
            + str(self.guild_id)
        )
