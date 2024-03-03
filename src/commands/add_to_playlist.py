from models.songs import Song
from utils.constants import SERVERS, bot, cur
from services import youtube, spotify
from discord.ext import commands
from typing import Optional


# Add a song to the Purdue Blows playlist
@bot.slash_command(
    name="add_to_playlist",
    description="Adds a link to the Purdue Blows playlist",
    guild_ids=SERVERS,
)
async def add_to_playlist(
    ctx: commands.Context,
    url: str,
    name: Optional[str] = None,
    artist: Optional[str] = None,
    album: Optional[str] = None,
    release_date: Optional[str] = None,
) -> None:
    # validate that url is a youtube url
    if not youtube.validate_youtube_url(url):
        await ctx.respond("Url must be a valid YouTube url", ephemeral=True)
        return
    song = Song(
        name=name, artist=artist, url=url, album=album, release_date=release_date
    )
    # if a parameter is None, attempt to search the spotify api for it
    if name is None or artist is None or album is None or release_date is None:
        # Get any data possible from youtube
        if name is None or artist is None:
            song = await youtube.get_song_metadata_from_youtube(song.url)
        song = await spotify.get_song_metadata_from_spotify(song)
    # if the data isn't acquired, throw an error accordingly
    if song.name is None or song.artist is None:
        await ctx.respond(
            "Sorry, we couldn't find the song you were looking for", ephemeral=True
        )
        return
    # if the data is acquired, update the playlist table accordingly
    result = cur.execute(
        "INSERT INTO songs (name, artist, url, album, release_date) VALUES (?, ?, ?, ?, ?)",
        (song.name, song.artist, song.url, song.album, song.release_date),
    )
    if not result:
        await ctx.respond(
            "Sorry, that song's already in the playlist",
            ephemeral=True,
        )
    # Using the id of the song, add it to the playlist table
    cur.execute(
        "INSERT INTO playlist (song_id, song, played, user_id) VALUES (?, ?, ?)",
        (
            cur.lastrowid,
            await youtube.download_song_from_youtube(song.url),
            False,
            ctx.author.id,
        ),
    )
    # return a success message as confirmation
    await ctx.respond(
        f"{ctx.author.name} added {song.name} to the Purdue Blows playlist"
    )
    return
