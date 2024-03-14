# Attempts to download the song at url from youtube
import os
from yt_dlp import YoutubeDL
from utils.to_mp3_file import to_mp3_file
from utils.escape_special_characters import escape_special_characters

YOUTUBE_DOWNLOAD_ERROR = "Could not download the information from youtube"


async def download_song_from_youtube(ydl: YoutubeDL, url: str) -> bytes:
    # Use the yt-dlp library to download the song
    info_dict = ydl.extract_info(url, download=True)
    if info_dict is None:
        raise ValueError(YOUTUBE_DOWNLOAD_ERROR)
    # filepath = "%(title)s.%(ext)s"
    # title = info_dict.get("title")
    # if title != None:
    #     title = escape_special_characters(title)
    # ext = info_dict.get("ext")
    # if ext != None:
    #     ext = to_mp3_file(ext)
    # downloaded_file_path = filepath % {"title": title, "ext": ext}
    downloaded_file_path = "temp.mp3"
    # Rename file
    os.rename(
        os.path.join(os.getcwd(), "temp.mp3"),
        os.path.join(os.getcwd(), downloaded_file_path),
    )
    # Open file
    with open(os.path.join(os.getcwd(), downloaded_file_path), "rb") as file:
        audio = file.read()
    # Remove file
    os.remove(os.path.join(os.getcwd(), downloaded_file_path))
    return audio
