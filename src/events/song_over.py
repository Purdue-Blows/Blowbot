# Retrieves the next song to be played on the "completion"
# of the previous song
# The next song will either be the next song in the queue, or,
# if the queue is empty, a random selection is made from songs
# that haven't been played in the playlist (i.e. where played == False)
# If all the songs have been played, a fun "thanks for listening" message is sent
# to notify current listeners and the playlist repeats
async def on_song_over():
    pass
