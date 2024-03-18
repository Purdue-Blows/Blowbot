from enum import Enum


class SongFields(Enum):
    ID = "_id"
    AUDIO = "audio"
    NAME = "name"
    ARTIST = "artist"
    URL = "url"
    ALBUM = "album"
    RELEASE_DATE = "release_date"

    @classmethod
    def from_string(cls, value):
        for field in cls:
            if str(field.value) == str(value):
                return field
        raise ValueError(f"No matching field found for value: {value}")


class PlaylistFields(Enum):
    ID = "_id"
    SONG_ID = "song_id"
    PLAYED = "played"
    USER_ID = "user_id"
    PLAYLIST_NUM = "playlist_num"
    PLAYLIST_NAME = "playlist_name"
    GUILD_ID = "guild_id"

    @classmethod
    def from_string(cls, value):
        for field in cls:
            if str(field.value) == str(value):
                return field
        raise ValueError(f"No matching field found for value: {value}")


class QueueFields(Enum):
    ID = "_id"
    SONG_ID = "song_id"
    USER_ID = "user_id"
    QUEUE_NUM = "queue_num"
    PLAYED = "played"
    GUILD_ID = "guild_id"

    @classmethod
    def from_string(cls, value):
        for field in cls:
            if str(field.value) == str(value):
                return field
        raise ValueError(f"No matching field found for value: {value}")


class UserFields(Enum):
    ID = "_id"
    NAME = "name"
    JAZZLE_STREAK = "jazzle_streak"
    JAZZ_TRIVIA_CORRECT = "jazz_trivia_correct"
    JAZZ_TRIVIA_INCORRECT = "jazz_trivia_incorrect"
    JAZZ_TRIVIA_PERCENTAGE = "jazz_trivia_percentage"
    GUILD_ID = "guild_id"

    @classmethod
    def from_string(cls, value):
        for field in cls:
            if str(field.value) == (value):
                return field
        raise ValueError(f"No matching field found for value: {value}")


class PlaybackFields(Enum):
    ID = "_id"
    CURRENT_PLAYLIST = "current_playlist"
    CURRENT_PLAYLIST_INDEX = "current_playlist_index"
    CURRENTLY_PLAYING = "currently_playing"
    GUILD_ID = "guild_id"

    @classmethod
    def from_string(cls, value):
        for field in cls:
            if str(field.value) == str(value):
                return field
        raise ValueError(f"No matching field found for value: {value}")


class PurduePlaysChallengeFields(Enum):
    ID = "_id"
    NAME = "name"
    DESCRIPTION = "description"
    PLAYLIST_URL = "url"
    COMPLETED = "completed"  # Whether or not the challenge is over
    DATE = "date"
    EDITORS = "editors"

    @classmethod
    def from_string(cls, value):
        for field in cls:
            if str(field.value) == str(value):
                return field
        raise ValueError(f"No matching field found for value: {value}")


class PurduePlaysSubmissionFields(Enum):
    ID = "_id"
    USER_ID = "user_id"
    NOTES = "notes"  # Optional user-specified notes about the performance

    @classmethod
    def from_string(cls, value):
        for field in cls:
            if str(field.value) == str(value):
                return field
        raise ValueError(f"No matching field found for value: {value}")


class AlbumFields(Enum):
    ID = "_id"
    NAME = "name"
    DESCRIPTION = "description"
    TRACKS = "tracks"  # The tracks in the album
    COMPLETED = "completed"
    VIDEO_URL = "video_url"
    EDITORS = "editors"

    @classmethod
    def from_string(cls, value):
        for field in cls:
            if str(field.value) == str(value):
                return field
        raise ValueError(f"No matching field found for value: {value}")


class TrackFields(Enum):
    ID = "_id"
    NAME = "name"
    DESCRIPTION = "description"
    SCORE = "score"  # A zip of all the necessary files
    PLAYLIST_URL = (
        "playlist_url"  # Each track gets it's own playlist to handle multiple shots
    )
    STEP = "step"  # what part of the process the track is currently on; i.e. arrangement, performing, editing, etc
    ROLES = "roles"  # required roles
    PERFORMERS = "performers"
    ARRANGERS = "arrangers"
    EDITORS = "editors"

    @classmethod
    def from_string(cls, value):
        for field in cls:
            if str(field.value) == str(value):
                return field
        raise ValueError(f"No matching field found for value: {value}")
