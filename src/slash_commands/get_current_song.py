from src.models.queue import Queue
from discord import VoiceClient
from discord.ext import commands
from src.models.model_fields import PlaylistFields, QueueFields, SongFields
from src.models.playlist import Playlist
from src.slash_commands.back import COULD_NOT_FIND_SONG
from utils.constants import DB_CLIENT, PURDUE_BLOWS_PLAYLISTS, SERVERS, bot

# from utils.state import CURRENT_SONG
from models.songs import Song

CURRENT_SONG_MESSAGE = "Blowbot is not currently playing anything"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"
COULD_NOT_FIND_SONG = "Song not found"
GENERIC_ERROR = "There was an error trying to get the current song"


@bot.command(
    name="get_current_song",
    description="Get the song that Blowbot is currently playing",
    guild_ids=SERVERS,
)
async def get_current_song(ctx: commands.Context) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_MESSAGE)
    db = DB_CLIENT[str(ctx.guild.id)]
    # Check if there are any songs in the queue that haven't been played yet
    try:
        song = await Queue.get_current_song(db)
        if song is not None:
            await ctx.send(Song.format_song(song), ephemeral=True)
        else:
            song = await Playlist.get_current_song(db)
            if song:
                await ctx.send(Song.format_song(song), ephemeral=True)
            else:
                raise Exception(COULD_NOT_FIND_SONG)
    except Exception as e:
        await ctx.send(GENERIC_ERROR, ephemeral=True)
