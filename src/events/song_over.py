import random
from models.playlist import Playlist
from services.discord import play_song
from utils.constants import con
from utils.state import CURRENT_SONG, QUEUE_NUM
from discord.ext import commands


async def on_song_over(ctx: commands.Context) -> None:
    global QUEUE_NUM
    global CURRENT_SONG
    cur = con.cursor()
    next_song = cur.execute("SELECT * FROM queue WHERE id = ?", (QUEUE_NUM,)).fetchone()
    if not next_song:
        unplayed_songs = cur.execute(
            "SELECT * FROM playlist WHERE played = ?", (False,)
        ).fetchmany()
        if len(unplayed_songs) == 0:
            await ctx.respond(
                ":confetti_ball: The entire playlist has been listened to! It will now repeat! :confetti_ball:"
            )
            await Playlist.reset_playlist()
            CURRENT_SONG = random.choice(unplayed_songs)
            return
    else:
        CURRENT_SONG = next_song
    await play_song()
    cur.close()
