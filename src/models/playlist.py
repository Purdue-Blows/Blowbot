from enum import Enum
import random
from models.songs import Song
from models.users import User
from typing import Dict, Any, List, Optional, Union
from models.songs import Song
from models.users import User
from pymongo.errors import DuplicateKeyError
from src.models.model_fields import PlaylistFields, QueueFields

from utils.constants import PlaylistName
import random


class Playlist:
    def __init__(
        self,
        song: Song,
        played: bool,
        playlist_num: int,
        playlist_name: PlaylistName,
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
            raise ValueError("Song not found")
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
        # TODO: Check that song id and user id are in the database
        try:
            print("Playlist.add was called")
            # If the song isn't already in songs, add it
            song = await Song.add(playlist.song)

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
    async def retrieve_many(
        db,
        song_ids: Optional[List[int]] = None,
        played: Optional[bool] = None,
        user_id: Optional[int] = None,
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
    async def shuffle(db) -> None:
        query = {PlaylistFields.PLAYED.name: False}
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
    async def reset_playlists(db) -> None:
        await db.playlist.delete_many({})

    @staticmethod
    async def reset_playlist(db, playlist_name: PlaylistName) -> None:
        await db.playlist.delete_many(
            {PlaylistFields.PLAYLIST_NAME.name: playlist_name.name}
        )

    @staticmethod
    async def remove_song(db, playlist: "Playlist") -> None:
        await db.playlist.delete_one({PlaylistFields.ID.name: playlist.id})

    @staticmethod
    async def update(db, playlist: "Playlist") -> Optional["Playlist"]:
        await db.playlist.update_one(
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
        return playlist

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
