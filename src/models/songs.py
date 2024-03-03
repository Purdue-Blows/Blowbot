from utils.constants import con
from typing import Optional, List, Union


class Song:
    def __init__(
        self,
        url: str,
        name: Optional[str] = None,
        artist: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
        id: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.artist = artist
        cur = con.cursor()
        cur.execute("SELECT * FROM songs WHERE url = ?", (url,))
        result = cur.fetchone()
        cur.close()
        if result is not None:
            raise ValueError("URL already exists in the database")
        self.url = url
        self.album = album
        self.release_date = release_date
        pass

    @staticmethod
    def from_map(map: dict) -> "Song":
        return Song(
            map["id"],
            map["name"],
            map["artist"],
            map["url"],
            map["album"],
            map["release_date"],
        )

    # Add the song to the database
    @staticmethod
    async def add(song: "Song") -> Optional["Song"]:
        try:
            cur = con.cursor()
            result = cur.execute(
                "INSERT INTO songs (name, artist, url, album, release_date) VALUES (?, ?, ?, ?, ?)",
                (song.name, song.artist, song.url, song.album, song.release_date),
            ).fetchone()
            cur.close()
            return Song.from_map(result[0])
        except Exception as e:
            print(f"Error occurred while adding song: {e}")
            return None

    @staticmethod
    async def retrieve_many(
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> List["Song"]:
        try:
            cur = con.cursor()
            query = "SELECT * FROM songs WHERE 1=1"
            params = []

            if name:
                query += " AND name = ?"
                params.append(name)
            if artist:
                query += " AND artist = ?"
                params.append(artist)
            if url:
                query += " AND url = ?"
                params.append(url)
            if album:
                query += " AND album = ?"
                params.append(album)
            if release_date:
                query += " AND release_date = ?"
                params.append(release_date)

            cur.execute(query, params)
            results = cur.fetchall()
            cur.close()

            return [Song.from_map(result) for result in results]
        except Exception as e:
            print(f"Error occurred while retrieving songs: {e}")
            return []

    @staticmethod
    async def retrieve_one(
        id: Optional[int] = None,
        name: Optional[str] = None,
        artist: Optional[str] = None,
        url: Optional[str] = None,
        album: Optional[str] = None,
        release_date: Optional[str] = None,
    ) -> Optional["Song"]:
        try:
            cur = con.cursor()
            query = "SELECT * FROM songs WHERE 1=1"
            params = []

            if id:
                query += " AND id = ?"
                params.append(id)
            if name:
                query += " AND name = ?"
                params.append(name)
            if artist:
                query += " AND artist = ?"
                params.append(artist)
            if url:
                query += " AND url = ?"
                params.append(url)
            if album:
                query += " AND album = ?"
                params.append(album)
            if release_date:
                query += " AND release_date = ?"
                params.append(release_date)

            cur.execute(query, params)
            result = cur.fetchone()
            cur.close()

            return Song.from_map(result) if result else None
        except Exception as e:
            print(f"Error occurred while retrieving song: {e}")
            return None

    @staticmethod
    async def update(song: "Song") -> Optional["Song"]:
        try:
            cur = con.cursor()
            cur.execute(
                "UPDATE songs SET name = ?, artist = ?, url = ?, album = ?, release_date = ? WHERE id = ?",
                (
                    song.name,
                    song.artist,
                    song.url,
                    song.album,
                    song.release_date,
                    song.id,
                ),
            )
            cur.close()
            return song
        except Exception as e:
            print(f"Error occurred while updating song: {e}")
            return None

    @staticmethod
    async def format_song(song: "Song") -> str:
        return f"Name: {song.name}\nArtist: {song.artist}\nURL: {song.url}\nAlbum: {song.album}\nRelease Date: {song.release_date}"
