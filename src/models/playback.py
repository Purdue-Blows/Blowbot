import traceback
from typing import Optional
from models.model_fields import PlaybackFields

from utils.constants import Base, CurrentlyPlaying, PlaylistNames, Session
from typing import Optional
from models.model_fields import PlaybackFields
from utils.constants import CurrentlyPlaying, PlaylistNames
from sqlalchemy import BigInteger, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.util import concurrency


class Playback(Base):
    __tablename__ = "playback"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    guild_id = Column(BigInteger, unique=True, nullable=False)
    current_playlist = Column(String)
    current_playlist_index = Column(Integer)
    currently_playing = Column(String)

    @staticmethod
    def add_sync(
        session, guild_id, current_playlist: str, currently_playing: CurrentlyPlaying
    ):
        try:
            playback = Playback(
                guild_id=guild_id,
                current_playlist=current_playlist,
                currently_playing=currently_playing,
                current_playlist_index=1,
            )
            session.add(playback)
            session.commit()
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            raise e

    @staticmethod
    def add(
        session, guild_id, current_playlist: str, currently_playing: CurrentlyPlaying
    ):
        return concurrency.greenlet_spawn(
            Playback.add_sync, session, guild_id, current_playlist, currently_playing
        )

    @staticmethod
    def retrieve_one_sync(session, guild_id) -> "Playback":
        playback = session.query(Playback).filter_by(guild_id=guild_id).first()
        return playback

    @staticmethod
    async def retrieve_one(session, guild_id) -> "Playback":
        return await concurrency.greenlet_spawn(
            Playback.retrieve_one_sync, session, guild_id
        )

    @staticmethod
    def get_currently_playing_sync(session, guild_id) -> CurrentlyPlaying:
        playback = session.query(Playback).filter_by(guild_id=guild_id).first()
        return CurrentlyPlaying.from_string(playback.currently_playing)

    @staticmethod
    async def get_currently_playing(session, guild_id) -> CurrentlyPlaying:
        return await concurrency.greenlet_spawn(
            Playback.get_currently_playing_sync, session, guild_id
        )

    @staticmethod
    def get_current_playlist_sync(session, guild_id) -> PlaylistNames:
        playback = session.query(Playback).filter_by(guild_id=guild_id).first()
        return PlaylistNames.from_string(playback.current_playlist)

    @staticmethod
    async def get_current_playlist(session, guild_id) -> PlaylistNames:
        return await concurrency.greenlet_spawn(
            Playback.get_current_playlist_sync, session, guild_id
        )

    @staticmethod
    def get_current_playlist_index_sync(session, guild_id) -> int:
        playback = session.query(Playback).filter_by(guild_id=guild_id).first()
        return playback.current_playlist_index

    @staticmethod
    async def get_current_playlist_index(session, guild_id) -> int:
        return await concurrency.greenlet_spawn(
            Playback.get_current_playlist_index_sync, session, guild_id
        )

    @staticmethod
    def update_sync(session, playback: "Playback", guild_id) -> bool:
        session.query(Playback).filter_by(guild_id=guild_id).update(
            {
                PlaybackFields.CURRENT_PLAYLIST.value: playback.current_playlist,
                PlaybackFields.CURRENT_PLAYLIST_INDEX.value: playback.current_playlist_index,
                PlaybackFields.CURRENTLY_PLAYING.value: playback.currently_playing,
            }
        )
        session.commit()
        return True

    @staticmethod
    async def update(session, playback: "Playback", guild_id) -> bool:
        return await concurrency.greenlet_spawn(
            Playback.update_sync, session, playback, guild_id
        )

    @staticmethod
    def delete_sync(session, guild_id) -> bool:
        try:
            session.query(Playback).filter_by(guild_id=guild_id).delete()
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            traceback.print_exc()
            raise e

    @staticmethod
    async def delete(session, guild_id) -> bool:
        return await concurrency.greenlet_spawn(Playback.delete_sync, session, guild_id)

    @staticmethod
    def log_map(playback: dict) -> None:
        print("PLAYLIST")
        print(f"Id: {playback[PlaybackFields.ID.value]}")
        print(f"Current Playlist: {playback[PlaybackFields.CURRENT_PLAYLIST.value]}")
        print(
            f"Current Playlist Index: {playback[PlaybackFields.CURRENT_PLAYLIST_INDEX.value]}"
        )
        print(f"Currently Playing: {playback[PlaybackFields.CURRENTLY_PLAYING.value]}")
        print(f"Guild Id: {playback[PlaybackFields.GUILD_ID.value]}")

    def to_string(self):
        return (
            "PLAYBACK\n"
            + "Id: "
            + str(self.id)
            + "\n Current Playlist: "
            + str(self.current_playlist)
            + "\n Current Playlist Index: "
            + str(self.current_playlist_index)
            + "\n Currently Playing: "
            + str(self.currently_playing)
            + "\n Guild Id: "
            + str(self.guild_id)
        )
