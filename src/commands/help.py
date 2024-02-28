from utils.constants import SERVERS
from bot import bot


@bot.slash_command(
    name="help",
    description="Get some advice on Blowbot and how to best utilize it",
    guild_ids=SERVERS,
)
async def help(ctx):
    await ctx.respond(
        """
# Blowbot
The official Purdue Blows Discord Bot, built by Purdue Jazz for Purdue Jazz!
## Commands
- /help: Get some advice on Blowbot and how to best utilize it
- /add_to_playlist (link): Adds a link to the Purdue Blows playlist
- /get_playlist: Returns a link to the Purdue Blows playlist
- /get_current_song: Get the song that Blowbot is currently playing
- /play_song (link): Add a song to the queue 
- /view_queue: View the current queue
- /remove_from_queue (index): Remove a song that you added to the queue (or a song in general if you are an admin)
- /remove_from_playlist (index): Remove from playlist; you can only remove a song that you added, unless you are an admin
- /jazzle: Determine the jazz standard based on a number of hints. How many tries can you get it in?
- /jazz_trivia: Get a jazz trivia question
- /profile: Get information about your current user profile, from your current roles, badges, jazz trivia and jazzle scores, and more
""",
        ephemeral=True,
    )
