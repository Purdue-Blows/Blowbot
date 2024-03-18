import re
from src.utils.messages import GENERIC_ERROR
from utils.constants import yt
from youtube_service import validate_youtube_url


def get_video_id_from_url(url: str) -> str:
    video_id = ""
    try:
        # Regular expression pattern to match YouTube video URLs
        pattern = r"(?<=v=|v\/|vi=|vi\/|youtu.be\/|embed\/|\/v\/|\/e\/|watch\?v=|youtube.com\/user\/[^#]*#([^\/]*?\/)*)[^#&?]*"
        match = re.search(pattern, url)
        if match:
            video_id = match.group(0)
    except Exception as e:
        print(str(e))
    return video_id


def get_playlist_id_from_url(url: str) -> str:
    playlist_id = ""
    try:
        # Regular expression pattern to match YouTube playlist URLs
        pattern = r"(?<=list=)[^#\&\?]*"
        match = re.search(pattern, url)
        if match:
            playlist_id = match.group(0)
    except Exception as e:
        print(str(e))
    return playlist_id


def refresh_access_token() -> bool:
    if yt.refresh_token:
        yt.refresh_access_token(refresh_token=yt.refresh_token)
        return True
    return False

def get_new_refresh_token() -> bool:
    


# Create playlist using YouTube Data API
async def create_playlist(
    new_playlist_name: str, new_playlist_description: str
) -> bool:
    try:
        request = yt.playlists.insert(
            body={
                "snippet": {
                    "title": new_playlist_name,
                    "description": new_playlist_description,
                }
            },
        )
        if request is None:
            raise ValueError(GENERIC_ERROR)
        return True
    except Exception as e:
        print(str(e))
        return False


# Add video at url to playlist using YT
# TODO: this prob doesn't work
async def add_to_playlist(url: str, playlist_name: str) -> bool:
    try:
        if not await validate_youtube_url(url):
            raise ValueError("Invalid URL")
        video_id = get_video_id_from_url(url)
        playlists = yt.playlists.list(mine=True, pageToken=None)

        playlist_names = [
            playlist["snippet"]["title"]  # type: ignore
            for playlist in playlists  # type: ignore
        ]
        request = None
        for name in playlist_names:
            if playlist_name == name:
                # Add to playlist
                if type(playlists) is dict:
                    playlist_id = playlists.get(playlist_names.index(name)).get("id")  # type: ignore

                request = yt.playlistItems.insert(
                    body={
                        "snippet": {
                            "playlistId": playlist_id,
                            "resourceId": {
                                "kind": "youtube#video",
                                "videoId": video_id,
                            },
                        }
                    }
                )
                break

        if request is None:
            raise ValueError(GENERIC_ERROR)

        return True
    except Exception as e:
        print(str(e))
        return False


# Remove from playlist using YT
async def remove_from_playlist(url: str, playlist_name: str):
    pass
