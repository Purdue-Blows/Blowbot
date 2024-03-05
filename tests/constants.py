from models.users import User
from models.users import User
from models.playlist import Playlist
from models.queue import Queue
from models.songs import Song
import os

# Test data
URL = "https://www.youtube.com/watch?v=dnK6OHPQZbA"
NAME = "Joy Spring"
ARTIST = "Clifford Brown"
ALBUM = "Clifford Brown & Max Roach"
RELEASE_DATE = "December 1st, 1954"
SONG = Song(
    name=NAME, artist=ARTIST, url=URL, album=ALBUM, release_date=RELEASE_DATE, id=1
)
USER = User(
    name="Clifford Brown",
    jazzle_streak=0,
    jazz_trivia_correct=0,
    jazz_trivia_incorrect=0,
    jazz_trivia_percentage=0,
    id=1,
)
# Get the path to the audio file
audio_path = os.path.join(os.path.dirname(__file__), "joy_spring.mp3")

with open(audio_path, "rb") as f:
    audio_content = f.read()

PLAYLIST = Playlist(song=SONG, audio=audio_content, played=True, user=USER, id=1)
QUEUE = Queue(song=SONG, audio=audio_content, user=USER, id=1)
