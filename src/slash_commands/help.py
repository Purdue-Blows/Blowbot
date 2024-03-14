# from typing import Any
# from discord.ext import commands
# from utils.constants import SERVERS, bot
# from utils.messages import NO_GUILD_ERROR

# HELP_MESSAGE = """
# # Blowbot
# The official Purdue Blows Discord Bot, built by Purdue Jazz for Purdue Jazz!
# ## Commands
# - /add_to_playlist (link): Adds a link to the Purdue Blows playlist
# - /add_to_queue (link): Add a song to the queue
# - /back: Relisten to the previous song (if it exists)
# - /clear_queue: Clear the current queue (if you are an admin)
# - /create_purdue_plays: Creates a new Purdue Plays challenge (if you are an admin)
# - /edit_playlist_song: Edit the data for a song in the playlist
# - /get_current_song: Get the song that Blowbot is currently playing
# - /get_playlist: Returns a link to the Purdue Blows playlist
# - /get_purdue_plays: Get information about current Purdue Plays challenges
# - /create_playlist (url) (name): Creates a new playlist (if you are an admin)
# - /help: Get some advice on Blowbot and how to best utilize it
# - /jazzle: Determine the jazz standard based on a number of hints. How many tries can you get it in?
# - /jazz_trivia: Get a jazz trivia question
# - /pause: Pause Blowbot
# - /play: Attempt to resume blowbot playback
# - /profile: Get information about your current user profile, from your current roles, badges, jazz trivia and jazzle scores, and more
# - /remove_from_playlist (index): Remove from playlist; you can only remove a song that you added, unless you are an admin
# - /remove_from_queue (index): Remove a song that you added to the queue (or a song in general if you are an admin)
# - /shuffle_playlist: Shuffle the specified playlist or the current playlist if unspecified
# - /skip: Skip the current song
# - /switch_playlist: Switch to a different playlist
# - /sync_playlist: Sync the specified playlist or the current playlist if unspecified
# - /upload_purdue_plays: Upload a submission to a Purdue Plays challenge
# - /view_queue: View the current queue
# """


# @bot.slash_command(
#     name="help",
#     description="Get some advice on Blowbot and how to best utilize it",
#     guild_ids=SERVERS,
# )
# async def help(ctx) -> Any:
#     if ctx.guild is None:
#         raise Exception(NO_GUILD_ERROR)
#     await ctx.respond(HELP_MESSAGE, ephemeral=True)
