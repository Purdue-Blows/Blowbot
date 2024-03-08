from enum import Enum


class SongFields(Enum):
    ID = "_id"
    AUDIO = "audio"
    NAME = "name"
    ARTIST = "artist"
    URL = "url"
    ALBUM = "album"
    RELEASE_DATE = "release_date"


class PlaylistFields(Enum):
    ID = "_id"
    SONG_ID = "song_id"
    PLAYED = "played"
    USER_ID = "user_id"
    PLAYLIST_NUM = "playlist_num"
    PLAYLIST_NAME = "playlist_name"


class QueueFields(Enum):
    ID = "_id"
    SONG_ID = "song_id"
    USER_ID = "user_id"
    QUEUE_NUM = "queue_num"
    PLAYED = "played"


class UserFields(Enum):
    ID = "_id"
    NAME = "name"
    JAZZLE_STREAK = "jazzle_streak"
    JAZZ_TRIVIA_CORRECT = "jazz_trivia_correct"
    JAZZ_TRIVIA_INCORRECT = "jazz_trivia_incorrect"
    JAZZ_TRIVIA_PERCENTAGE = "jazz_trivia_percentage"
