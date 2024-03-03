from models.songs import Song
from models.users import User
from utils.constants import con
from typing import Dict, Any, List, Optional, Union
from models.songs import Song
from models.users import User


class Playlist:
    def __init__(
        self,
        song: Song,
        audio: bytes,
        played: bool,
        user: User,
        id: Optional[int] = None,
    ) -> None:
        self.song = song
        self.audio = audio
        self.played = played
        self.user = user
        self.id = id
        # super().__init__(
        #     name=song.name,
        #     artist=song.artist,
        #     url=song.url,
        #     album=song.album,
        #     release_date=song.release_date,
        # )

    @staticmethod
    def from_map(map: Dict[str, Any]) -> "Playlist":
        return Playlist(
            id=map["id"],
            song=map["song"],
            audio=map["audio"],
            played=map["played"],
            user=map["user"],
        )

    @staticmethod
    async def add(playlist: "Playlist") -> Union["Playlist", None]:
        try:
            cur = con.cursor()
            # If the song isn't already in songs, add it
            song = await Song.add(playlist.song)

            if song:
                cur.execute(
                    "INSERT INTO playlist (song_id, song, played, user_id) VALUES (?, ?, ?, ?)",
                    (song.id, playlist.audio, playlist.played, playlist.user.id),
                )
            else:
                cur.execute(
                    "INSERT INTO playlist (song_id, song, played, user_id) VALUES (?, ?, ?, ?)",
                    (
                        playlist.song.id,
                        playlist.audio,
                        playlist.played,
                        playlist.user.id,
                    ),
                )
            return
        except Exception as e:
            return None
        finally:
            cur.close()

    @staticmethod
    async def retrieve_many() -> List["Playlist"]:
        try:
            cur = con.cursor()
            cur.execute("SELECT * FROM playlist")
            rows = cur.fetchall()
            playlists = []
            for row in rows:
                playlist = Playlist.from_map(row)
                playlists.append(playlist)
            return playlists
        except Exception as e:
            return []
        finally:
            cur.close()

    @staticmethod
    async def retrieve_one(
        id=None, played: bool = False, random: bool = True
    ) -> Optional["Playlist"]:
        try:
            cur = con.cursor()
            if id:
                cur.execute("SELECT * FROM playlist WHERE id=?", (id,))
            elif played:
                cur.execute("SELECT * FROM playlist WHERE played=?", (played,))
            elif random:
                cur.execute("SELECT * FROM playlist ORDER BY RANDOM() LIMIT 1")
            else:
                return None
            row = cur.fetchone()
            if row:
                playlist = Playlist.from_map(row)
                return playlist
            else:
                return None
        except Exception as e:
            return None
        finally:
            cur.close()

    @staticmethod
    async def reset_playlist() -> None:
        try:
            cur = con.cursor()
            cur.execute("DELETE * FROM playlist")
            con.commit()
        except Exception as e:
            pass
        finally:
            cur.close()

    @staticmethod
    async def remove_song(playlist: "Playlist") -> None:
        try:
            cur = con.cursor()
            cur.execute("DELETE * FROM playlist WHERE id=?", (playlist.id,))
            con.commit()
        except Exception as e:
            pass
        finally:
            cur.close()

    @staticmethod
    async def update(playlist: "Playlist") -> Optional["Playlist"]:
        try:
            cur = con.cursor()
            cur.execute(
                "UPDATE playlist SET song_id=?, song=?, played=?, user_id=? WHERE id=?",
                (
                    playlist.song.id,
                    playlist.audio,
                    playlist.played,
                    playlist.user.id,
                    playlist.id,
                ),
            )
            con.commit()
            return playlist
        except Exception as e:
            return None
        finally:
            cur.close()
