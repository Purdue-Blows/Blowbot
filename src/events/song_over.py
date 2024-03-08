import random
from models.playlist import Playlist
from discord_service import play_song
from utils.constants import db
from utils.state import CURRENT_SONG, QUEUE_NUM
from discord.ext import commands

END_OF_PLAYLIST = ":confetti_ball: The entire playlist has been listened to! It will now repeat! :confetti_ball:"
DB_ERROR = "An error occurred while trying to update the queue"


async def on_song_over(ctx: commands.Context) -> None:
    global QUEUE_NUM
    global CURRENT_SONG
    if CURRENT_SONG is None:
        return
    if await db.queue.find_one({"song_id": CURRENT_SONG.id}) is not None:
        QUEUE_NUM += 1
        CURRENT_SONG = await db.queue.find_one({"_id": QUEUE_NUM})
        if CURRENT_SONG is None:
            # Get a random song from the playlist
            unplayed_songs = await db.playlist.find({"played": False}).to_list(
                length=None
            )
            if len(unplayed_songs) == 0:
                await ctx.send(END_OF_PLAYLIST)
                await Playlist.reset_playlist()
                CURRENT_SONG = random.choice(
                    await db.playlist.find({}).to_list(length=None)
                )
                await play_song()
                return
            else:
                # Get a random song from the unplayed songs in the playlist
                CURRENT_SONG = random.choice(unplayed_songs)
        await play_song()
        return
    elif await db.playlist.find_one({"song_id": CURRENT_SONG.id}) is not None:
        # Mark the CURRENT_SONG as played
        result = await db.playlist.update_one(
            {"_id": CURRENT_SONG.id}, {"$set": {"played": True}}
        )
        if not result:
            raise Exception("An error occurred while trying to update the playlist")
        # Check if there are any new songs in the queue
        next_song = await db.queue.find_one({"_id": QUEUE_NUM})
        if next_song is not None:
            CURRENT_SONG = next_song
            QUEUE_NUM += 1
            await play_song()
            return
        else:
            # Get the next song from the playlist
            unplayed_songs = await db.playlist.find({"played": False}).to_list(
                length=None
            )
            if len(unplayed_songs) == 0:
                await ctx.send(END_OF_PLAYLIST)
                await Playlist.reset_playlist()
                CURRENT_SONG = random.choice(unplayed_songs)
                return
            else:
                CURRENT_SONG = random.choice(unplayed_songs)
            await play_song()
            return
    else:
        raise Exception("The song is not in the queue or playlist")
