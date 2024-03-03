# Attempts to retrieve a song from youtube
from models.songs import Song


async def get_song_metadata_from_youtube(url: str) -> Song:
    pass


# Validates that a url is a youtube url
async def validate_youtube_url(url):
    if url.contains("https://www.youtube.com"):
        return True
    return False


# Parses song information into a youtube search
# ideal for finding the correct song
async def create_youtube_search(song):
    pass


# Attempts to download the song at url from youtube
async def download_song_from_youtube(url):
    pass


# Check if song exists in the playlist
async def check_song_in_playlist(song):
    pass


# A general utility method to ensure that the YouTube playlist and db are synced
async def sync_playlist():
    pass
