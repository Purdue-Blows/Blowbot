from utils.constants import SERVERS
from bot import bot


@bot.slash_command(
    name="remove_from_playlist",
    description="Remove from playlist; you can only remove a song that you added, unless you are an admin",
    guild_ids=SERVERS,
)
async def remove_from_playlist(ctx, arg):
    return
