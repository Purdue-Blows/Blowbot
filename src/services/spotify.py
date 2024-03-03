from models.songs import Song
from utils.constants import spotify


# Attempts to retrieve the song metadata from spotify given the parameters
async def get_song_metadata_from_spotify(song: Song) -> Song:
    # Check which values are present (not None)
    if song.name is not None and song.artist is not None:
        # Use the spotipy API to attempt to update the values
        results = spotify.search(
            q=f"track:{song.name} artist:{song.artist}", type="track", limit=1
        )
        if results["tracks"]["items"]:
            track = results["tracks"]["items"][0]
            song.name = track["name"]
            song.artist = track["artists"][0]["name"]
            song.album = track["album"]["name"]
            song.release_date = track["album"]["release_date"]
    # Return the updated song
    return song
