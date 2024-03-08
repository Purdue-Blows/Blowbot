from typing import Optional
from models.model_fields import PlaybackFields

from utils.constants import CurrentlyPlaying, PlaylistNames


class Playback:
    def __init__(
        self,
        current_playlist: PlaylistNames,
        current_playlist_index: int,
        currently_playing: CurrentlyPlaying,
        id: Optional[int] = None,
    ) -> None:
        self.current_playlist = current_playlist
        self.current_playlist_index = current_playlist_index
        self.currently_playing = currently_playing
        self.id = id

    @staticmethod
    async def get_currently_playing(db) -> CurrentlyPlaying:
        playback = await db.playback.find_one({})
        return playback[PlaybackFields.CURRENTLY_PLAYING.name]

    @staticmethod
    async def get_current_playlist(db) -> PlaylistNames:
        playback = await db.playback.find_one({})
        return playback[PlaybackFields.CURRENT_PLAYLIST.name]

    @staticmethod
    async def get_current_playlist_index(db) -> int:
        playback = await db.playback.find_one({})
        return playback[PlaybackFields.CURRENT_PLAYLIST_INDEX.name]

    @staticmethod
    async def update(db, playback: "Playback") -> bool:
        update = await db.playback.update_one(
            {},
            {
                "$set": {
                    PlaybackFields.CURRENT_PLAYLIST.name: playback.current_playlist,
                    PlaybackFields.CURRENT_PLAYLIST_INDEX.name: playback.current_playlist_index,
                    PlaybackFields.CURRENTLY_PLAYING.name: playback.currently_playing,
                }
            },
        )
        if update:
            return True
        return False
