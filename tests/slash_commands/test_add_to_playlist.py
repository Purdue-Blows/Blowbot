from unittest import IsolatedAsyncioTestCase
from unittest.mock import AsyncMock, MagicMock, patch
from discord.ext import commands
from models.songs import Song
from models.users import User
from tests.constants import ALBUM, ARTIST, NAME, PLAYLIST, RELEASE_DATE, SONG, URL, USER
from slash_commands.add_to_playlist import (
    ARTIST_ERROR_MESSAGE,
    NAME_AND_ARTIST_ERROR_MESSAGE,
    NAME_ERROR_MESSAGE,
    SONG_ADD_ERROR_MESSAGE,
    SONG_EXISTS_ERROR_MESSAGE,
    SUCCESS_MESSAGE,
    URL_ERROR_MESSAGE,
    USER_ADD_ERROR_MESSAGE,
    USER_RETRIEVAL_ERROR_MESSAGE,
    add_to_playlist,
)


# NOTE: I shouldn't generate other tests until I get one test working
# AND then fix the command; generate one test at a time
class TestAddToPlaylist(IsolatedAsyncioTestCase):
    @patch("services.youtube.get_song_metadata_from_youtube")
    @patch("services.spotify.get_song_metadata_from_spotify")
    @patch("models.songs.Song.add")
    @patch("models.users.User.retrieve_one")
    @patch("models.users.User.add")
    @patch("models.playlist.Playlist.add")
    def setUpModule(
        self,
        mock_get_song_metadata_from_youtube,
        mock_get_song_metadata_from_spotify,
        mock_add_song,
        mock_retrieve_user,
        mock_add_user,
        mock_add_playlist,
    ):
        self.ctx = AsyncMock(commands.Context)
        self.url = URL
        self.name = NAME
        self.artist = ARTIST
        self.album = ALBUM
        self.release_date = RELEASE_DATE
        self.song = SONG
        self.mock_get_song_metadata_from_youtube: MagicMock = (
            mock_get_song_metadata_from_youtube
        )
        self.mock_get_song_metadata_from_spotify: MagicMock = (
            mock_get_song_metadata_from_spotify
        )
        self.mock_add_song: MagicMock = mock_add_song
        self.mock_retrieve_user: MagicMock = mock_retrieve_user
        self.mock_add_user: MagicMock = mock_add_user
        self.mock_add_playlist: MagicMock = mock_add_playlist

    async def test_invalid_url(self):
        # Adapt any necessary objects and methods
        # None necessary in this case because invalid url should be the first thing checked in the function
        # Call method
        await add_to_playlist(
            ctx=self.ctx,
            url="invalid_url",
            name=self.name,
            artist=self.artist,
            album=self.album,
            release_date=self.release_date,
        )
        # Make assertions using the mocked classes
        self.ctx.respond.called_once_with(URL_ERROR_MESSAGE, ephemeral=True)
        self.mock_get_song_metadata_from_youtube.assert_not_called()
        self.mock_get_song_metadata_from_spotify.assert_not_called()
        self.mock_add_song.assert_not_called()
        self.mock_retrieve_user.assert_not_called()
        self.mock_add_user.assert_not_called()
        self.mock_add_playlist.assert_not_called()

    async def test_no_song_name(self):
        # Adapt any necessary objects and methods
        # In this case, the song object should be created with just a valid url
        self.mock_get_song_metadata_from_youtube.return_value = Song(
            url=self.url, artist=self.artist
        )
        self.mock_get_song_metadata_from_spotify.return_value = Song(
            url=self.url, artist=self.artist
        )
        # Call method
        await add_to_playlist(ctx=self.ctx, url=self.url)
        # Mocks
        self.ctx.respond.called_once_with(NAME_ERROR_MESSAGE, ephemeral=True)
        self.mock_get_song_metadata_from_youtube.assert_called_once()
        self.mock_get_song_metadata_from_spotify.assert_called_once()
        self.mock_add_song.assert_not_called()
        self.mock_retrieve_user.assert_not_called()
        self.mock_add_user.assert_not_called()
        self.mock_add_playlist.assert_not_called()

    async def test_no_song_artist(self):
        # Adapt any necessary objects and methods
        # In this case, the song object should be created with just a valid url
        self.mock_get_song_metadata_from_youtube.return_value = Song(
            url=self.url, name=self.name
        )
        self.mock_get_song_metadata_from_spotify.return_value = Song(
            url=self.url, name=self.name
        )
        # Call method
        await add_to_playlist(ctx=self.ctx, url=self.url)
        # Mocks
        self.ctx.respond.called_once_with(ARTIST_ERROR_MESSAGE, ephemeral=True)
        self.mock_get_song_metadata_from_youtube.assert_called_once()
        self.mock_get_song_metadata_from_spotify.assert_called_once()
        self.mock_add_song.assert_not_called()
        self.mock_retrieve_user.assert_not_called()
        self.mock_add_user.assert_not_called()
        self.mock_add_playlist.assert_not_called()

    async def test_no_song_info(self):
        # Adapt any necessary objects and methods
        # In this case, the song object should be created with just a valid url
        song = Song(url=self.url)
        # Adapt any necessary objects and methods
        # In this case, the song object should be created with just a valid url
        self.mock_get_song_metadata_from_youtube.return_value = Song(url=self.url)
        self.mock_get_song_metadata_from_spotify.return_value = Song(url=self.url)
        # Call method
        await add_to_playlist(ctx=self.ctx, url=self.url)
        # Mocks
        self.ctx.respond.called_once_with(NAME_AND_ARTIST_ERROR_MESSAGE, ephemeral=True)
        self.mock_get_song_metadata_from_youtube.assert_called_once()
        self.mock_get_song_metadata_from_spotify.assert_called_once()
        self.mock_add_song.assert_not_called()
        self.mock_retrieve_user.assert_not_called()
        self.mock_add_user.assert_not_called()
        self.mock_add_playlist.assert_not_called()

    async def test_failed_to_add_song(self):
        # Adapt any necessary objects and methods
        # In this case, the song object should be created with all the necessary information
        self.mock_get_song_metadata_from_youtube.return_value = self.song
        self.mock_get_song_metadata_from_spotify.return_value = self.song
        self.mock_add_song.side_effect = Exception()
        # Call method
        await add_to_playlist(
            ctx=self.ctx,
            url=self.url,
        )
        # Mocks
        self.ctx.respond.called_once_with(SONG_EXISTS_ERROR_MESSAGE, ephemeral=True)
        self.mock_get_song_metadata_from_youtube.assert_called_once()
        self.mock_get_song_metadata_from_spotify.assert_called_once()
        self.mock_add_song.assert_called_once()
        self.mock_retrieve_user.assert_not_called()
        self.mock_add_user.assert_not_called()
        self.mock_add_playlist.assert_not_called()

    async def test_failed_to_retrieve_user(self):
        # Adapt any necessary objects and methods
        # In this case, the song object should be created with all the necessary information
        self.mock_get_song_metadata_from_youtube.return_value = self.song
        self.mock_get_song_metadata_from_spotify.return_value = self.song
        self.mock_retrieve_user.side_effect = Exception()
        # Call method
        await add_to_playlist(
            ctx=self.ctx,
            url=self.url,
        )
        # Mocks
        self.ctx.respond.called_once_with(USER_RETRIEVAL_ERROR_MESSAGE, ephemeral=True)
        self.mock_get_song_metadata_from_youtube.assert_called_once()
        self.mock_get_song_metadata_from_spotify.assert_called_once()
        self.mock_add_song.assert_called_once()
        self.mock_retrieve_user.assert_called_once()
        self.mock_add_user.assert_not_called()
        self.mock_add_playlist.assert_not_called()

    async def test_failed_to_add_user(self):
        # Adapt any necessary objects and methods
        # In this case, the song object should be created with all the necessary information
        self.mock_get_song_metadata_from_youtube.return_value = self.song
        self.mock_get_song_metadata_from_spotify.return_value = self.song
        self.mock_retrieve_user.return_value = None
        self.mock_add_user.side_effect = Exception()
        # Call method
        await add_to_playlist(
            ctx=self.ctx,
            url=self.url,
        )
        # Mocks
        self.ctx.respond.called_once_with(USER_ADD_ERROR_MESSAGE, ephemeral=True)
        self.mock_get_song_metadata_from_youtube.assert_called_once()
        self.mock_get_song_metadata_from_spotify.assert_called_once()
        self.mock_add_song.assert_called_once()
        self.mock_retrieve_user.assert_called_once()
        self.mock_add_user.assert_called_once()
        self.mock_add_playlist.assert_not_called()

    async def test_add_to_playlist_failed(self):
        # Adapt any necessary objects and methods
        # In this case, the song object should be created with all the necessary information
        self.mock_get_song_metadata_from_youtube.return_value = self.song
        self.mock_get_song_metadata_from_spotify.return_value = self.song
        self.mock_retrieve_user.return_value = USER
        self.mock_add_user.side_effect = Exception()
        # Call method
        await add_to_playlist(
            ctx=self.ctx,
            url=self.url,
        )
        # Mocks
        self.ctx.respond.called_once_with(SONG_ADD_ERROR_MESSAGE, ephemeral=True)
        self.mock_get_song_metadata_from_youtube.assert_called_once()
        self.mock_get_song_metadata_from_spotify.assert_called_once()
        self.mock_add_song.assert_called_once()
        self.mock_retrieve_user.assert_called_once()
        self.mock_add_user.assert_called_once()
        self.mock_add_playlist.assert_not_called()

    async def test_successful_add_to_playlist(self):
        # Adapt any necessary objects and methods
        # In this case, the song object should be created with all the necessary information
        self.mock_get_song_metadata_from_youtube.return_value = self.song
        self.mock_get_song_metadata_from_spotify.return_value = self.song
        self.mock_retrieve_user.return_value = USER
        self.mock_add_playlist.return_value = PLAYLIST
        # Call method
        await add_to_playlist(
            ctx=self.ctx,
            url=self.url,
        )
        # Mocks
        self.ctx.respond.called_once_with(
            SUCCESS_MESSAGE.format(author_name=USER.name, song_name=self.song.name)
        )
        self.mock_get_song_metadata_from_youtube.assert_called_once()
        self.mock_get_song_metadata_from_spotify.assert_called_once()
        self.mock_add_song.assert_called_once()
        self.mock_retrieve_user.assert_called_once()
        self.mock_add_user.assert_not_called()
        self.mock_add_playlist.assert_called_once()
