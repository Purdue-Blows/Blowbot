# A variable that gets updated with the instance of the currently playing song
from models.songs import Song
from typing import Optional
from models.songs import Song


CURRENT_SONG: Optional[Song] = None
# The current queue_num; gets incremented or decremented and serves as a utility
# For the skip and back commands
QUEUE_NUM = 0
