from utils.constants import con
from typing import Dict, List, Optional


# A model for a user
# Each user has:
# - A unique server username, name
# - The number of consecutive days playing jazzle, jazzle_streak
# - The number of correct trivia answers, jazz_trivia_correct
# - The number of incorrect trivia answers, jazz_trivia_incorrect
# - The accuracy percentage for jazz trivia, jazz_trivia_percentage
# This model also contains helper functions for
# - Adding a user to the database (called on first command used)
# - Retrieving a user from the database
# - Retrieving a list of users from the database
class User:
    def __init__(
        self,
        name: str,
        jazzle_streak: int,
        jazz_trivia_correct: int,
        jazz_trivia_incorrect: int,
        jazz_trivia_percentage: float,
        id: Optional[int] = None,
    ):
        self.id = id
        self.name = name
        self.jazzle_streak = jazzle_streak
        self.jazz_trivia_correct = jazz_trivia_correct
        self.jazz_trivia_incorrect = jazz_trivia_incorrect
        self.jazz_trivia_percentage = jazz_trivia_percentage

    @staticmethod
    def from_map(map: Dict[str, any]) -> "User":  # type: ignore
        return User(
            id=map["id"],
            name=map["name"],
            jazzle_streak=map["jazzle_streak"],
            jazz_trivia_correct=map["jazz_trivia_correct"],
            jazz_trivia_incorrect=map["jazz_trivia_incorrect"],
            jazz_trivia_percentage=map["jazz_trivia_percentage"],
        )

    # Adds a user instance to the users table
    @staticmethod
    async def add(user: "User") -> Optional["User"]:
        try:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO users (name, jazzle_streak, jazz_trivia_correct, jazz_trivia_incorrect, jazz_trivia_percentage) VALUES (?, ?, ?, ?, ?)",
                (
                    user.name,
                    user.jazzle_streak,
                    user.jazz_trivia_correct,
                    user.jazz_trivia_incorrect,
                    user.jazz_trivia_percentage,
                ),
            ).fetchone()
            con.commit()
            cur.close()
            return user
        except Exception:
            return None

    @staticmethod
    async def retrieve_many() -> Optional[List["User"]]:
        try:
            cur = con.cursor()
            result = cur.execute("SELECT * FROM users").fetchall()
            cur.close()
            return [User.from_map(row) for row in result]
        except Exception:
            return None

    @staticmethod
    async def retrieve_one(id=None, name=None) -> Optional["User"]:
        try:
            cur = con.cursor()
            if id is not None:
                result = cur.execute("SELECT * FROM users WHERE id=?", (id,)).fetchone()
            elif name is not None:
                result = cur.execute(
                    "SELECT * FROM users WHERE name=?", (name,)
                ).fetchone()
            else:
                raise ValueError("Either id or name must be provided.")
            cur.close()
            return User.from_map(result)
        except Exception:
            return None

    @staticmethod
    async def update(user: "User") -> Optional["User"]:
        try:
            cur = con.cursor()
            result = cur.execute(
                "UPDATE users SET name=?, jazzle_streak=?, jazz_trivia_correct=?, jazz_trivia_incorrect=?, jazz_trivia_percentage=? WHERE id=?",
                (
                    user.name,
                    user.jazzle_streak,
                    user.jazz_trivia_correct,
                    user.jazz_trivia_incorrect,
                    user.jazz_trivia_percentage,
                    user.id,
                ),
            ).fetchone()
            con.commit()
            cur.close()
            return User.from_map(result[0])
        except Exception:
            return None

    def to_string(self):
        return (
            "Id: "
            + str(self.id)
            + "\n Name: "
            + self.name
            + "\n Jazzle Streak: "
            + str(self.jazzle_streak)
            + "\n Jazz Trivia Correct:"
            + str(self.jazz_trivia_correct)
            + "\n Jazz Trivia Incorrect:"
            + str(self.jazz_trivia_incorrect)
            + "\n Jazz Trivia Percentage:"
            + str(self.jazz_trivia_percentage)
        )
