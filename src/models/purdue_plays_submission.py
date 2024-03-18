import random

from psycopg import IntegrityError
from models.songs import Song
from models.users import User
from typing import Dict, Any, List, Optional, Union
from models.songs import Song
from models.users import User
from models.model_fields import PlaybackFields, PlaylistFields, QueueFields
from models.playback import Playback

from utils.constants import PURDUE_BLOWS_PLAYLISTS, Base, PlaylistNames
import random
from sqlalchemy.orm import Session
from sqlalchemy import (
    BigInteger,
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    desc,
    func,
)
from sqlalchemy.orm import relationship
from sqlalchemy.util import concurrency

SONG_NOT_FOUND = "Song not found"
COULD_NOT_GET_PLAYLIST_NUM = "Could not get playlist num"
PLAYBACK_ISSUE = "There was an issue with playback"


class PurduePlaysSubmission(Base):
    __tablename__ = "purdue_plays_submission"

    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    notes = Column(String)

    user = relationship("User")

    @staticmethod
    def from_map_sync(session: Session, map: Dict[str, Any]) -> "Playlist":
        song = Song.retrieve_one_sync(session, id=map[PlaylistFields.SONG_ID.value])
        try:
            user = User.retrieve_one_sync(
                session,
                guild_id=map[PlaylistFields.GUILD_ID.value],
                id=map[PlaylistFields.USER_ID.value],
            )
        except Exception as e:
            user = None
        if song is None:
            raise ValueError(SONG_NOT_FOUND)
        # User can be none in certain cases, such as admins adding via the yt api
        # if user is None:
        #     raise ValueError("User not found")
        return Playlist(
            id=map[PlaylistFields.ID.value],
            song=song,
            played=map[PlaylistFields.PLAYED.value],
            playlist_num=map[PlaylistFields.PLAYLIST_NUM.value],
            playlist_name=map[PlaylistFields.PLAYLIST_NAME.value],
            user=user,
            guild_id=map[PlaylistFields.GUILD_ID.value],
        )

    @staticmethod
    async def from_map(session: Session, map: Dict[str, Any]) -> "Playlist":
        return await concurrency.greenlet_spawn(Playlist.from_map_sync, session, map)

    @staticmethod
    def add_sync(session: Session, playlist: "Playlist") -> Union["Playlist", None]:
        print("add_sync")
        playlist_name = PlaylistNames.from_string(playlist.playlist_name)  # type: ignore
        try:
            # If the song isn't already in songs, add it
            song = Song.add_sync(session, playlist.song)

            if playlist.playlist_num is None:
                playlist.playlist_num = Playlist.get_next_playlist_num_sync(
                    session,
                    guild_id=playlist.guild_id,  # type: ignore
                    playlist_name=playlist_name,
                )

            if song:
                print("Song is: " + song.to_string())
                playlist_obj = Playlist(
                    song=song,
                    played=playlist.played,
                    playlist_num=playlist.playlist_num,
                    playlist_name=playlist_name.value,
                    user=playlist.user,
                    guild_id=playlist.guild_id,
                )
                session.add(playlist_obj)
                session.commit()
                return playlist_obj
            return None
        except IntegrityError:
            print("Duplicate key error; adding playlist")
            if playlist.song.id is None:
                song = Song.retrieve_one_sync(session, url=playlist.song.url)
            playlist_obj = Playlist(
                song=song,
                played=playlist.played,
                playlist_num=playlist.playlist_num,
                playlist_name=playlist_name.value,
                user=playlist.user,
                guild_id=playlist.guild_id,
            )
            session.add(playlist_obj)
            session.commit()
            return playlist_obj
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def add(session: Session, playlist: "Playlist") -> Union["Playlist", None]:
        return await concurrency.greenlet_spawn(Playlist.add_sync, session, playlist)

    @staticmethod
    def get_next_playlist_num_sync(
        session: Session, playlist_name: PlaylistNames, guild_id
    ) -> int:
        print("get_next_playlist_num_sync")
        try:
            largest_playlist_num = (
                session.query(Playlist)
                .filter_by(playlist_name=playlist_name.value, guild_id=guild_id)
                .order_by(desc(Playlist.playlist_num))
                .scalar()
                .first()
            )
            if largest_playlist_num:
                playlist_num = largest_playlist_num + 1
            else:
                raise Exception(COULD_NOT_GET_PLAYLIST_NUM)
            return playlist_num
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def get_next_playlist_num(
        session: Session,
        guild_id,
        playlist_name: PlaylistNames,
    ) -> int:
        return await concurrency.greenlet_spawn(
            Playlist.get_next_playlist_num_sync, session, playlist_name, guild_id
        )

    @staticmethod
    def get_current_song_sync(
        session: Session,
        guild_id,
        playlist_name: Optional[PlaylistNames] = None,
    ) -> Optional[Song]:
        print("get_current_song_sync")
        try:
            playlist_num = Playback.get_current_playlist_index_sync(session, guild_id)
            if not playlist_name:
                playlist_name = Playback.get_current_playlist_sync(session, guild_id)
            # print(playlist_name)
            # print(playlist_num)

            # Playlist should NOT be None here
            playlist = (
                session.query(Playlist)
                .filter(
                    Playlist.playlist_name == playlist_name.value,
                    Playlist.playlist_num == playlist_num,
                    Playlist.guild_id == guild_id,
                )
                .first()
            )
            # print(playlist)
            if playlist != None:
                song = Song.retrieve_one_sync(session, id=playlist.song.id)
                return song
            return None
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def get_current_song(
        session: Session,
        guild_id,
        playlist_name: Optional[PlaylistNames] = None,
    ) -> Optional[Song]:
        return await concurrency.greenlet_spawn(
            Playlist.get_current_song_sync, session, guild_id, playlist_name
        )

    @staticmethod
    def get_playlist_count_sync(
        session: Session, playlist_name: PlaylistNames, guild_id
    ) -> int:
        print("get_playlist_count_sync")
        try:
            count = (
                session.query(Playlist)
                .filter_by(playlist_name=playlist_name.value, guild_id=guild_id)
                .count()
            )
            return count
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def get_playlist_count(
        session: Session, playlist_name: PlaylistNames, guild_id
    ) -> int:
        return await concurrency.greenlet_spawn(
            Playlist.get_playlist_count_sync, session, playlist_name.value, guild_id
        )

    @staticmethod
    def retrieve_many_sync(
        session: Session,
        guild_id,
        song_ids: Optional[List[int]] = None,
        played: Optional[bool] = None,
        user_id: Optional[int] = None,
        playlist_name: Optional[PlaylistNames] = None,
        url: Optional[str] = None,
        name: Optional[str] = None,
        album: Optional[str] = None,
        artist: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> List["Playlist"]:
        print("retrieve_many_sync")
        try:
            query = session.query(Playlist).join(Song, Playlist.song_id == Song.id)
            query = query.filter_by(guild_id=guild_id)
            if (
                song_ids is None
                and played is None
                and user_id is None
                and url is None
                and name is None
                and playlist_name is None
                and album is None
                and artist is None
                and release_date is None
            ):
                playlists = query.all()
                return playlists
            if song_ids is None and (
                url is not None
                or name is not None
                or artist is not None
                or album is not None
                or release_date is not None
            ):
                try:
                    songs = Song.retrieve_many_sync(
                        session,
                        url=url,
                        name=name,
                        artist=artist,
                        album=album,
                        release_date=release_date,
                    )
                    if songs:
                        song_ids = [song.id for song in songs if song.id is not None]  # type: ignore
                except Exception as e:
                    pass
            if song_ids is not None:
                query = query.filter(Playlist.song_id.in_(song_ids))
            if played is not None:
                query = query.filter_by(played=played)
            if playlist_name is not None:
                query = query.filter_by(playlist_name=playlist_name.value)
            if user_id is not None:
                query = query.filter_by(user_id=user_id)

            playlists = query.all()
            return playlists
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def retrieve_many(
        session: Session,
        guild_id,
        song_ids: Optional[List[int]] = None,
        played: Optional[bool] = None,
        user_id: Optional[int] = None,
        playlist_name: Optional[PlaylistNames] = None,
        url: Optional[str] = None,
        name: Optional[str] = None,
        album: Optional[str] = None,
        artist: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> List["Playlist"]:
        return await concurrency.greenlet_spawn(
            Playlist.retrieve_many_sync,
            session,
            guild_id,
            song_ids,
            played,
            user_id,
            playlist_name,
            url,
            name,
            album,
            artist,
            release_date,
        )

    @staticmethod
    def retrieve_one_sync(
        session: Session,
        guild_id,
        id: Optional[int] = None,
        song_id: Optional[int] = None,
        played: Optional[bool] = None,
        playlist_name: Optional[PlaylistNames] = None,
        user_id: Optional[int] = None,
        url: Optional[str] = None,
        name: Optional[str] = None,
        album: Optional[str] = None,
        artist: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> Optional["Playlist"]:
        print("retrieve_one_sync")
        try:
            query = (
                session.query(Playlist)
                .join(Song, Playlist.song_id == Song.id)
                .filter(Playlist.guild_id == guild_id)
            )
            # if id is not None:
            #     query = query.filter(Playlist.id == id)
            # if song_id is not None:
            #     query = query.filter(Playlist.song_id == song_id)
            # if played is not None:
            #     query = query.filter(Playlist.played == played)
            # if playlist_name is not None:
            #     query = query.filter(Playlist.playlist_name == playlist_name)
            # if user_id is not None:
            #     query = query.filter(Playlist.user_id == user_id)

            # print("Query")
            # print(query)
            playlist = query.first()
            # print("Playlist")
            # print(playlist)
            if playlist != None:
                return playlist
            if song_id is None and (
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
                # print("Song")
                # print(song)
                if song:
                    song_id = song.id if song.id is not None else None  # type: ignore
                    query = session.query(Playlist).filter(Playlist.song_id == song_id)
                    if played is not None:
                        query = query.filter(Playlist.played == played)
                    if playlist_name is not None:
                        query = query.filter(
                            Playlist.playlist_name == playlist_name.value
                        )
                    if user_id is not None:
                        query = query.filter(Playlist.user_id == user_id)
                    playlist = query.first()
                    if playlist:
                        return playlist
            return None
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
        playlist_name: Optional[PlaylistNames] = None,
        user_id: Optional[int] = None,
        url: Optional[str] = None,
        name: Optional[str] = None,
        album: Optional[str] = None,
        artist: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> Optional["Playlist"]:
        return await concurrency.greenlet_spawn(
            Playlist.retrieve_one_sync,
            session,
            guild_id,
            id,
            song_id,
            played,
            playlist_name,
            user_id,
            url,
            name,
            album,
            artist,
            release_date,
        )

    # Shuffles the songs in the playlist that haven't been played yet
    @staticmethod
    def shuffle_sync(
        session: Session,
        guild_id,
        playlist_name: PlaylistNames,
    ) -> None:
        print("shuffle_sync")
        try:
            # print("Getting numbers")
            min_playlist_num = (
                session.query(func.min(Playlist.playlist_num))
                .filter_by(
                    played=False, playlist_name=playlist_name.value, guild_id=guild_id
                )
                .scalar()
            )
            max_playlist_num = (
                session.query(func.max(Playlist.playlist_num))
                .filter_by(
                    played=False, playlist_name=playlist_name.value, guild_id=guild_id
                )
                .scalar()
            )
        except Exception as e:
            session.rollback()
            raise e
        try:
            if playlist_name:
                print("Getting playlists")
                playlists = (
                    session.query(Playlist)
                    .filter(
                        Playlist.playlist_name == playlist_name.value,
                        Playlist.playlist_num <= max_playlist_num,
                        Playlist.playlist_num >= min_playlist_num,
                        Playlist.playlist_num < max_playlist_num,
                        Playlist.guild_id == guild_id,
                    )
                    .all()
                )
                print("Shuffling numbers")
                playlist_nums = list(range(min_playlist_num, max_playlist_num + 1))
                for playlist in playlists:
                    playlist.playlist_num = random.choice(playlist_nums)
                    playlist_nums.remove(playlist.playlist_num)
                session.commit()
            else:
                print("No playlist name")
                playback_doc = session.query(Playback).first()
                if playback_doc:
                    current_playlist_name = playback_doc.current_playlist
                    playlists = (
                        session.query(Playlist)
                        .filter(
                            Playlist.playlist_name == current_playlist_name,
                            Playlist.playlist_num <= max_playlist_num,
                            Playlist.playlist_num >= min_playlist_num,
                            Playlist.playlist_num < max_playlist_num,
                            Playlist.guild_id == guild_id,
                        )
                        .all()
                    )
                    playlist_nums = list(range(min_playlist_num, max_playlist_num + 1))
                    for playlist in playlists:
                        playlist.playlist_num = random.choice(playlist_nums)
                        playlist_nums.remove(playlist.playlist_num)
                    session.commit()
                else:
                    raise Exception()
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def shuffle(
        session: Session,
        guild_id,
        playlist_name: Optional[PlaylistNames] = None,
    ) -> None:
        return await concurrency.greenlet_spawn(
            Playlist.shuffle_sync,
            session,
            guild_id,
            playlist_name,
        )

    @staticmethod
    def switch_playlist_sync(
        session: Session, guild_id, new_playlist_name: PlaylistNames
    ) -> bool:
        print("switch_playlist_sync")
        try:
            # Mark all songs as having not been played
            session.query(Playlist).filter(
                Playlist.guild_id == guild_id,
            ).update(
                {
                    PlaylistFields.PLAYED.value: False,
                }
            )
            # Update the current playback playlist name and playlist index
            playback = session.query(Playback).first()
            if playback:
                playback.current_playlist_index = 0  # type: ignore
                playback.current_playlist = new_playlist_name.value  # type: ignore
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def switch_playlist(
        session: Session,
        guild_id,
        new_playlist_name: PlaylistNames,
    ) -> bool:
        return await concurrency.greenlet_spawn(
            Playlist.switch_playlist_sync, session, guild_id, new_playlist_name
        )

    @staticmethod
    def get_next_song_sync(session: Session, guild_id) -> Optional[Song]:
        print("get_next_song_sync")
        try:
            playback = session.query(Playback).first()
            if playback:
                current_playlist_name = playback.current_playlist
                current_playlist_index = playback.current_playlist_index
                current_playlist_index += 1
                next_playlist = (
                    session.query(Playlist)
                    .filter_by(
                        playlist_name=current_playlist_name,
                        playlist_num=current_playlist_index,
                        guild_id=guild_id,
                    )
                    .first()
                )
                if not next_playlist:
                    return None
                song = Song.retrieve_one_sync(session, id=next_playlist.song.id)
                return song
            return None
        except Exception as e:
            session.rollback()
            raise e

    @staticmethod
    async def get_next_song(session: Session, guild_id) -> Optional[Song]:
        return await concurrency.greenlet_spawn(
            Playlist.get_next_song_sync, session, guild_id
        )

    @staticmethod
    def get_previous_song_sync(
        session: Session,
        guild_id,
        current_playlist_name: PlaylistNames,
        current_playlist_index: int,
    ) -> Optional[Song]:
        print("get_previous_song_sync")
        try:
            previous_playlist = (
                session.query(Playlist)
                .filter_by(
                    playlist_name=current_playlist_name.value,
                    playlist_num=current_playlist_index - 1,
                    guild_id=guild_id,
                )
                .first()
            )
            if not previous_playlist:
                return None
            song = Song.retrieve_one_sync(session, id=previous_playlist.song.id)
            return song
        except Exception as e:
            session.rollback()
            print(f"Error retrieving previous song: {e}")
            raise e

    @staticmethod
    async def get_previous_song(
        session: Session,
        guild_id,
        current_playlist_name: PlaylistNames,
        current_playlist_index: int,
    ) -> Optional[Song]:
        return await concurrency.greenlet_spawn(
            Playlist.get_previous_song_sync,
            session,
            guild_id,
            current_playlist_name,
            current_playlist_index,
        )

    @staticmethod
    def reset_playlists_sync(session: Session, guild_id) -> bool:
        print("reset_playlists_sync")
        try:
            session.query(Playlist).filter_by(guild_id=guild_id).update(
                {PlaylistFields.PLAYED.value: False}
            )
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            print(f"Error resetting playlists: {e}")
            return False

    @staticmethod
    async def reset_playlists(session: Session, guild_id) -> bool:
        return await concurrency.greenlet_spawn(
            Playlist.reset_playlists_sync, session, guild_id
        )

    @staticmethod
    def reset_playlist_sync(
        session: Session,
        guild_id,
        playlist_name: PlaylistNames,
    ) -> bool:
        playlists = (
            session.query(Playlist)
            .filter_by(playlist_name=playlist_name.value, guild_id=guild_id)
            .update({PlaylistFields.PLAYED.value: False})
        )
        try:
            session.commit()
            return True
        except:
            session.rollback()
            return False

    @staticmethod
    async def reset_playlist(
        session: Session,
        guild_id,
        playlist_name: PlaylistNames,
    ) -> bool:
        return await concurrency.greenlet_spawn(
            Playlist.reset_playlist_sync, session, guild_id, playlist_name
        )

    @staticmethod
    def remove_song_sync(session: Session, playlist: "Playlist") -> bool:
        print("remove_song_sync")
        session.delete(playlist)
        try:
            session.commit()
            return True
        except Exception as e:
            print(f"Error removing song from playlist: {e}")
            session.rollback()
            return False

    @staticmethod
    async def remove_song(session: Session, playlist: "Playlist") -> bool:
        return await concurrency.greenlet_spawn(
            Playlist.remove_song_sync, session, playlist
        )

    @staticmethod
    def update_sync(session: Session, playlist: "Playlist") -> bool:
        print("update_sync")
        try:
            if playlist.id is not None:
                update = session.merge(
                    {
                        PlaylistFields.SONG_ID.value: playlist.song.id,
                        PlaylistFields.PLAYED.value: playlist.played,
                        PlaylistFields.PLAYLIST_NUM.value: playlist.playlist_num,
                        PlaylistFields.PLAYLIST_NAME.value: playlist.playlist_name,
                        PlaylistFields.USER_ID.value: (
                            playlist.user.id if playlist.user != None else None
                        ),
                        PlaylistFields.GUILD_ID.value: playlist.guild_id,
                    }
                )
                if update:
                    session.commit()
                    return True
        except Exception as e:
            session.rollback()
            raise e
        return False

    @staticmethod
    async def update(session: Session, playlist: "Playlist") -> bool:
        return await concurrency.greenlet_spawn(Playlist.update_sync, session, playlist)

    @staticmethod
    def log_map(playlist: dict) -> None:
        print("PLAYLIST")
        print(f"Id: {playlist[PlaylistFields.ID.value]}")
        print(f"Song Id: {playlist[PlaylistFields.SONG_ID.value]}")
        print(f"User Id: {playlist[PlaylistFields.USER_ID.value]}")
        print(f"Played: {playlist[PlaylistFields.PLAYED.value]}")
        print(f"Playlist Number: {playlist[PlaylistFields.PLAYLIST_NUM.value]}")
        print(f"Playlist Name: {playlist[PlaylistFields.PLAYLIST_NAME.value]}")
        print(f"Guild Id: {playlist[PlaylistFields.GUILD_ID.value]}")

    def to_string(self):
        return (
            "PLAYLIST\n"
            + "Id: "
            + str(self.id)
            + "\n Song: "
            + self.song.to_string()
            + "\n Played: "
            + str(self.played)
            + ("\n User:" + self.user.to_string() if self.user else "")
            + "\n Playlist Number: "
            + str(self.playlist_num)
            + "\n Playlist Name: "
            + str(self.playlist_name)
            + "\n Guild Id: "
            + str(self.guild_id)
        )
