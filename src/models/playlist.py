from enum import Enum
from optparse import Option
import random
from turtle import update
from models.songs import Song
from models.users import User
from typing import Dict, Any, List, Optional, Union
from models.songs import Song
from models.users import User
from pymongo.errors import DuplicateKeyError
from src.models.model_fields import PlaybackFields, PlaylistFields, QueueFields

from utils.constants import PURDUE_BLOWS_PLAYLISTS, PlaylistNames
import random

SONG_NOT_FOUND = "Song not found"
COULD_NOT_GET_PLAYLIST_NUM = "Could not get playlist num"


class Playlist:
    def __init__(
        self,
        song: Song,
        played: bool,
        playlist_name: str,
        playlist_num: Optional[int] = None,
        user: Optional[User] = None,
        id: Optional[int] = None,
    ) -> None:
        self.song = song
        self.played = played
        self.playlist_num = playlist_num
        self.playlist_name = playlist_name
        self.user = user
        self.id = id

    @staticmethod
    def log_doc(playlist: dict) -> None:
        print("PLAYLIST DOC")
        print(f"Id: {playlist[PlaylistFields.ID.name]}")
        print(f"Song Id: {playlist[PlaylistFields.SONG_ID.name]}")
        print(f"User Id: {playlist[PlaylistFields.USER_ID.name]}")
        print(f"Played: {playlist[PlaylistFields.PLAYED.name]}")
        print(f"Playlist Number: {playlist[PlaylistFields.PLAYLIST_NUM.name]}")
        print(f"Playlist Name: {playlist[PlaylistFields.PLAYLIST_NAME.name]}")

    @staticmethod
    async def from_map(db, map: Dict[str, Any]) -> "Playlist":
        song = await Song.retrieve_one(id=map[PlaylistFields.SONG_ID.name])
        try:
            user = await User.retrieve_one(db, id=map[PlaylistFields.USER_ID.name])
        except Exception as e:
            user = None
        if song is None:
            raise ValueError(SONG_NOT_FOUND)
        # User can be none in certain cases, such as admins adding via the yt api
        # if user is None:
        #     raise ValueError("User not found")
        return Playlist(
            id=map[PlaylistFields.ID.name],
            song=song,
            played=map[PlaylistFields.PLAYED.name],
            playlist_num=map[PlaylistFields.PLAYLIST_NUM.name],
            playlist_name=map[PlaylistFields.PLAYLIST_NAME.name],
            user=user,
        )

    @staticmethod
    async def add(db, playlist: "Playlist") -> Union["Playlist", None]:
        try:
            print("Playlist.add was called")
            # If the song isn't already in songs, add it
            song = await Song.add(playlist.song)

            if playlist.playlist_num is None:
                playlist.playlist_num = await Playlist.get_next_playlist_num(
                    db, playlist.playlist_name
                )

            if song:
                print("Song is: " + song.to_string())
                result = await db.playlist.insert_one(
                    {
                        PlaylistFields.SONG_ID.name: song.id,
                        PlaylistFields.PLAYED.name: playlist.played,
                        PlaylistFields.PLAYLIST_NUM.name: playlist.playlist_num,
                        PlaylistFields.PLAYLIST_NAME.name: playlist.playlist_name,
                        PlaylistFields.USER_ID.name: (
                            playlist.user.id if playlist.user else None
                        ),
                    }
                )
                playlist.id = result.inserted_id
                return playlist
            return None
        except DuplicateKeyError:
            print("Duplicate key error; adding playlist")
            if playlist.song.id is None:
                song = await Song.retrieve_one(url=playlist.song.url)
            await db.playlist.insert_one(
                {
                    PlaylistFields.SONG_ID.name: playlist.song.id,
                    PlaylistFields.PLAYED.name: playlist.played,
                    PlaylistFields.USER_ID.name: (
                        playlist.user.id if playlist.user else None
                    ),
                    PlaylistFields.PLAYLIST_NUM.name: playlist.playlist_num,
                    PlaylistFields.PLAYLIST_NAME.name: playlist.playlist_name,
                }
            )
            return playlist

    @staticmethod
    async def get_next_playlist_num(db, playlist_name: str) -> int:
        largest_playlist_num = await db.playlist.find_one(
            {PlaylistFields.PLAYLIST_NAME.name: playlist_name},
            sort=[(PlaylistFields.PLAYLIST_NUM.name, -1)],
            projection={PlaylistFields.PLAYLIST_NUM.name: 1},
        )
        if largest_playlist_num:
            playlist_num = largest_playlist_num[PlaylistFields.PLAYLIST_NUM.name] + 1
        else:
            raise Exception(COULD_NOT_GET_PLAYLIST_NUM)
        return playlist_num

    @staticmethod
    async def get_current_song(
        db, playlist_name: Optional[str] = None
    ) -> Optional[Song]:
        if playlist_name is None:
            for name in PURDUE_BLOWS_PLAYLISTS:
                playlists = await db.playlists.find(
                    {
                        PlaylistFields.PLAYLIST_NAME.name: name,
                        PlaylistFields.PLAYED.name: True,
                    }
                ).to_list(length=None)
                if len(playlists) > 0:
                    break
        if playlists is None:
            raise Exception(SONG_NOT_FOUND)
        current_playlist = max(playlists, key=lambda playlist: playlist.playlist_num)
        song = await Song.retrieve_one(id=current_playlist[PlaylistFields.SONG_ID.name])
        return song

    @staticmethod
    async def get_playlist_count(db, playlist_name: str) -> int:
        count = await db.playlist.count_documents(
            {PlaylistFields.PLAYLIST_NAME.name: playlist_name}
        )
        return count

    @staticmethod
    async def retrieve_many(
        db,
        song_ids: Optional[List[int]] = None,
        played: Optional[bool] = None,
        user_id: Optional[int] = None,
        playlist_name: Optional[str] = None,
        url: Optional[str] = None,
        name: Optional[str] = None,
        album: Optional[str] = None,
        artist: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> List["Playlist"]:
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
            playlists = []
            async for document in db.playlist.find():
                playlist = Playlist.from_map(db, document)
                playlists.append(playlist)
            return playlists
        query = {}
        if song_ids is None and (
            url is not None
            or name is not None
            or artist is not None
            or album is not None
            or release_date is not None
        ):
            try:
                songs = await Song.retrieve_many(
                    url=url,
                    name=name,
                    artist=artist,
                    album=album,
                    release_date=release_date,
                )
                if songs:
                    song_ids = [song.id for song in songs if song.id is not None]
            except Exception as e:
                pass
        if song_ids is not None:
            query[PlaylistFields.SONG_ID.name] = {"$in": song_ids}
        if played is not None:
            query[PlaylistFields.PLAYED.name] = played
        if playlist_name is not None:
            query[PlaylistFields.PLAYLIST_NAME.name] = playlist_name
        if user_id is not None:
            query[PlaylistFields.USER_ID.name] = user_id

        playlists = []
        async for document in db.playlist.find(query):
            playlist = await Playlist.from_map(db, document)
            playlists.append(playlist)
        return playlists

    @staticmethod
    async def retrieve_one(
        db,
        id: Optional[int] = None,
        song_id: Optional[int] = None,
        played: Optional[bool] = None,
        playlist_name: Optional[str] = None,
        user_id: Optional[int] = None,
        url: Optional[str] = None,
        name: Optional[str] = None,
        album: Optional[str] = None,
        artist: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> Optional["Playlist"]:
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
        query = {}
        if id is not None:
            query[PlaylistFields.ID.name] = id
        if song_id is not None:
            query[PlaylistFields.SONG_ID.name] = song_id
        if playlist_name is not None:
            query[PlaylistFields.PLAYLIST_NAME.name] = playlist_name
        if played is not None:
            query[PlaylistFields.PLAYED.name] = played
        if user_id is not None:
            query[PlaylistFields.USER_ID.name] = user_id
        print(query)
        print("Finding playlist")
        playlist_doc = await db.playlist.find_one(query)
        if playlist_doc:
            Playlist.log_doc(playlist_doc)
            print("Converting playlist to map")
            playlist_doc = await Playlist.from_map(db, playlist_doc)
            print("Returning playlist")
        return playlist_doc

    # Shuffles the songs in the playlist that haven't been played yet
    @staticmethod
    async def shuffle(db, playlist_name: Optional[PlaylistNames] = None) -> None:
        query: dict[str, Any] = {PlaylistFields.PLAYED.name: False}
        if playlist_name:
            query[PlaylistFields.PLAYLIST_NAME.name] = playlist_name.name
        else:
            playback_doc = await db.playback.find_one({})
            current_playlist_name = playback_doc[PlaybackFields.CURRENT_PLAYLIST.name]
            query[PlaylistFields.PLAYLIST_NAME.name] = current_playlist_name

        playlists = await db.playlist.find(query).to_list(length=None)
        if playlists:
            for playlist in playlists:
                # Find the smallest and largest playlist_num values
                smallest_num = int("inf")
                largest_num = int("-inf")
                for playlist in playlists:
                    if playlist.playlist_num < smallest_num:
                        smallest_num = playlist.playlist_num
                    if playlist.playlist_num > largest_num:
                        largest_num = playlist.playlist_num

                # Generate a random playlist_num within the range
                playlist[PlaylistFields.PLAYLIST_NUM.name] = random.randint(
                    smallest_num, largest_num
                )
                await db.playlist.update_one(
                    {PlaylistFields.ID.name: playlist[PlaylistFields.ID.name]},
                    {
                        "$set": {
                            PlaylistFields.PLAYLIST_NUM.name: playlist[
                                PlaylistFields.PLAYLIST_NUM.name
                            ]
                        }
                    },
                )
        return None

    @staticmethod
    async def switch_playlist(db, new_playlist_name: PlaylistNames) -> bool:
        # Mark all songs as having not been played
        update_playlists = await db.playlist.update_many(
            {}, {"$set": {PlaylistFields.PLAYED.name: False}}
        )
        if not update_playlists:
            return False
        # Update the current playback playlist name and playlist index
        update_playback = await db.playback.update_one(
            {},
            {
                "$set": {
                    PlaybackFields.CURRENT_PLAYLIST_INDEX.name: 0,
                    PlaybackFields.CURRENT_PLAYLIST.name: new_playlist_name,
                }
            },
        )
        if not update_playback:
            return False
        return True

    @staticmethod
    async def get_next_song(db) -> Optional[Song]:
        # Returns the next song in the currently playing playlist
        playback_doc = await db.playback.find_one({})
        current_playlist_name = playback_doc[PlaybackFields.CURRENT_PLAYLIST.name]
        current_playlist_index = playback_doc[
            PlaybackFields.CURRENT_PLAYLIST_INDEX.name
        ]
        current_playlist_index += 1
        next_playlist = await Playlist.retrieve_one(
            db, current_playlist_name, current_playlist_index
        )
        if not next_playlist:
            return None
        song = await Song.retrieve_one(id=next_playlist.song.id)
        return song

    @staticmethod
    async def get_previous_song(db) -> Optional[Song]:
        # Returns the next song in the currently playing playlist
        playback_doc = await db.playback.find_one({})
        current_playlist_name = playback_doc[PlaybackFields.CURRENT_PLAYLIST.name]
        current_playlist_index = playback_doc[
            PlaybackFields.CURRENT_PLAYLIST_INDEX.name
        ]
        current_playlist_index += 1
        next_playlist = await Playlist.retrieve_one(
            db, current_playlist_name, current_playlist_index
        )
        if not next_playlist:
            return None
        song = await Song.retrieve_one(id=next_playlist.song.id)
        return song

    @staticmethod
    async def reset_playlists(db) -> bool:
        reset = await db.playlist.update_many(
            {}, {"$set": {PlaylistFields.PLAYED.name: False}}
        )
        if reset:
            return True
        return False

    @staticmethod
    async def reset_playlist(db, playlist_name: PlaylistNames) -> bool:
        reset = await db.playlist.update_many(
            {PlaylistFields.PLAYLIST_NAME.name: playlist_name.name},
            {"$set": {PlaylistFields.PLAYED.name: False}},
        )
        if reset:
            return True
        return False

    @staticmethod
    async def remove_song(db, playlist: "Playlist") -> bool:
        delete = await db.playlist.delete_one({PlaylistFields.ID.name: playlist.id})
        if delete:
            return True
        return False

    @staticmethod
    async def update(db, playlist: "Playlist") -> bool:
        update = await db.playlist.update_one(
            {PlaylistFields.ID.name: playlist.id},
            {
                "$set": {
                    PlaylistFields.SONG_ID.name: playlist.song.id,
                    PlaylistFields.PLAYED.name: playlist.played,
                    PlaylistFields.PLAYLIST_NUM.name: playlist.playlist_num,
                    PlaylistFields.PLAYLIST_NAME.name: playlist.playlist_name,
                    PlaylistFields.USER_ID.name: (
                        playlist.user.id if playlist.user != None else None
                    ),
                }
            },
        )
        if update:
            return True
        return False

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
        )
