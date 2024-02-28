from utils.constants import SERVERS
from bot import bot


@bot.slash_command(
    name="play_song", description="Add a song to Blowbot's queue", guild_ids=SERVERS
)
async def play_song(ctx, arg):
    return
