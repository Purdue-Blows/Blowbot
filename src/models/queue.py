from optparse import Option
from utils.constants import con
from typing import Any, List, Dict, Union, Optional

from models.songs import Song
from models.users import User


# A model for the queue table
# Note that the entire queue isn't loaded into memory because it's already in the database,
# This is just more of a utility model to ensure that the data
# flows smoothly and correctly
class Queue:
    def __init__(
        self, song: Song, audio: bytes, user: User, id: Optional[int] = None
    ) -> None:
        self.song = song
        self.audio = audio
        self.user = user
        self.id = id

    @staticmethod
    def from_map(map: Dict[str, Any]) -> "Queue":
        return Queue(
            id=map["id"], song=map["song"], audio=map["audio"], user=map["user"]
        )

    # Adds a queue instance to the queue table
    @staticmethod
    async def add(queue: "Queue") -> Optional["Queue"]:
        try:
            cur = con.cursor()
            # If the song isn't already in songs, add it
            song = await Song.add(queue.song)

            if song:
                cur.execute(
                    "INSERT INTO queue (song_id, song, user_id) VALUES (?, ?, ?)",
                    (song.id, queue.audio, queue.user.id),
                )
            else:
                cur.execute(
                    "INSERT INTO queue (song_id, song, user_id) VALUES (?, ?, ?)",
                    (queue.song.id, queue.audio, queue.user.id),
                )
            return queue
        except Exception as e:
            return None
        finally:
            con.commit()
            cur.close()

    @staticmethod
    async def retrieve_many(
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
        user_id: Optional[int] = None,
    ) -> Optional[List["Queue"]]:
        try:
            cur = con.cursor()
            query = "SELECT * FROM queue WHERE 1=1"
            params = []

            if name:
                query += " AND song_id IN (SELECT id FROM songs WHERE name = ?)"
                params.append(name)
            if artist:
                query += " AND song_id IN (SELECT id FROM songs WHERE artist = ?)"
                params.append(artist)
            if url:
                query += " AND song_id IN (SELECT id FROM songs WHERE url = ?)"
                params.append(url)
            if album:
                query += " AND song_id IN (SELECT id FROM songs WHERE album = ?)"
                params.append(album)
            if release_date:
                query += " AND song_id IN (SELECT id FROM songs WHERE release_date = ?)"
                params.append(release_date)
            if user_id:
                query += " AND user_id = ?"
                params.append(user_id)

            cur.execute(query, params)
            rows = cur.fetchall()
            queues = []
            for row in rows:
                song = await Song.retrieve_one(row["song_id"])
                user = await User.retrieve_one(row["user_id"])
                if song and user:
                    queue = Queue(song=song, audio=row["song"], user=user)
                else:
                    return None
                queues.append(queue)
            return queues
        except Exception as e:
            return []
        finally:
            cur.close()

    @staticmethod
    async def retrieve_one(
        id: int, played: bool = False, random: bool = True
    ) -> Optional["Queue"]:
        try:
            cur = con.cursor()
            if random:
                cur.execute(
                    "SELECT * FROM queue WHERE played = ? ORDER BY RANDOM() LIMIT 1",
                    (played,),
                )
            else:
                cur.execute(
                    "SELECT * FROM queue WHERE played = ? ORDER BY id LIMIT 1",
                    (played,),
                )
            row = cur.fetchone()
            if row:
                song = await Song.retrieve_one(row["song_id"])
                user = await User.retrieve_one(row["user_id"])
                if song and user:
                    queue = Queue(song=song, audio=row["song"], user=user)
                else:
                    return None
                return queue
            else:
                return None
        except Exception as e:
            return None
        finally:
            cur.close()

    @staticmethod
    async def clear_queue() -> None:
        try:
            cur = con.cursor()
            cur.execute("DELETE * FROM queue")
            con.commit()
        except Exception as e:
            pass
        finally:
            con.commit()
            cur.close()

    # Removes a song from the queue table (shifting all the songs up 1)
    @staticmethod
    async def remove_song(queue: "Queue") -> None:
        try:
            cur = con.cursor()
            cur.execute("DELETE FROM queue WHERE id = ?", (queue.id,))
            con.commit()
        except Exception as e:
            pass
        finally:
            cur.close()

    @staticmethod
    async def update(queue: "Queue") -> Optional["Queue"]:
        try:
            cur = con.cursor()
            # Update the song instance
            await Song.update(queue.song)
            # Update the queue instance
            cur.execute(
                "UPDATE queue SET audio = ?, user_id = ? WHERE id = ?",
                (queue.audio, queue.user.id, queue.id),
            )
            con.commit()
            return queue
        except Exception as e:
            return None
        finally:
            con.commit()
            cur.close()

    def to_string(self):
        return (
            "Id: "
            + str(self.id)
            + "\n Song: "
            + self.song.to_string()
            + "\n User:"
            + self.user.to_string()
        )
