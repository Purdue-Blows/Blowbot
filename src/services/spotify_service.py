from models.songs import Song

# from utils.constants import spotify
from spotipy import Spotify

from utils.messages import COULD_NOT_FIND_ERROR


# Attempts to retrieve the song metadata from spotify given the parameters
# TODO: need to update the spotify api call to avoid the madeleine west and keanan field group thing
async def get_song_metadata_from_spotify(spotify: Spotify, song: Song) -> Song:
    # Check which values are present (not None)
    print("SPOTIFY")
    if song.name is not None:
        # Use the spotipy API to attempt to update the values
        query = f"{song.name}"
        if song.artist is not None:
            query += f" {song.artist}"
        # if song.release_date is not None:
        #     query += f" year:{song.release_date}"
        # if song.album is not None:
        #     query += f" album:{song.album}"

        #     print("Calling that one")
        #     print(song.name)
        #     results = spotify.search(
        #         q=f"{song.name} {song.artist}", type="track", market="US", limit=1
        #     )
        # else:
        #     print("Calling this one")
        #     print(song.name)
        # results = spotify.search(
        #     q=f"{song.name}", type="track", market="US", limit=1
        # )
        results = spotify.search(q=query, type="track", limit=1)
        print("spotify results")
        print(results)
        if results != None:
            if len(results["tracks"]["items"]) != 0:
                if results.get("tracks") != None:
                    if results["tracks"].get("items") != None:
                        if len(results["tracks"]["items"]) != 0:
                            track = results["tracks"]["items"][0]
                if track == None:
                    raise Exception(COULD_NOT_FIND_ERROR.format("song"))
                if track.get("name") != None:
                    song.name = track["name"]
                else:
                    raise Exception(COULD_NOT_FIND_ERROR.format("name"))

                if track.get("artists") != None:
                    artists = ""
                    for artist in track["artists"]:
                        if artist.get("name") != None:
                            artists += artist["name"] + ", "
                    artists = artists[:-2]
                    song.artist = artists  # type: ignore
                else:
                    raise Exception(COULD_NOT_FIND_ERROR.format("artist"))

                if track.get("album") != None:
                    if track["album"].get("name") != None:
                        song.album = track["album"]["name"]
                    if track["album"].get("release_date") != None:
                        song.release_date = track["album"]["release_date"]
        print(song.to_string())
    # Return the updated song
    return song
