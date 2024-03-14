from select import epoll
import traceback
from models.queue import Queue
from discord import VoiceClient
from discord.ext import commands
from models.model_fields import PlaylistFields, QueueFields, SongFields
from models.playlist import Playlist
from utils.constants import PURDUE_BLOWS_PLAYLISTS, SERVERS, Session, bot
from utils.messages import COULD_NOT_FIND_ERROR, GENERIC_ERROR, NO_GUILD_ERROR

# from utils.state import CURRENT_SONG
from models.songs import Song

CURRENT_SONG_MESSAGE = "Blowbot is not currently playing anything"
NO_GUILD_MESSAGE = "You must be in a guild to use blowbot"


@bot.slash_command(
    name="get_current_song",
    description="Get the song that Blowbot is currently playing",
    guild_ids=SERVERS,
)
async def get_current_song(ctx) -> None:
    if ctx.guild is None:
        raise Exception(NO_GUILD_ERROR)
    with Session() as session:
        # Check if there are any songs in the queue that haven't been played yet
        try:
            song = await Queue.get_current_song(session, ctx.guild.id)
            if song is not None:
                await ctx.respond(Song.format_song(song), ephemeral=True)
            else:
                song = await Playlist.get_current_song(session, ctx.guild.id)
                if song:
                    await ctx.respond(Song.format_song(song), ephemeral=True)
                else:
                    await ctx.respond(
                        COULD_NOT_FIND_ERROR.format("song"), ephemeral=True
                    )
                    return
        except Exception as e:
            await ctx.respond(GENERIC_ERROR.format("get_current_song"), ephemeral=True)
            traceback.print_exc()
