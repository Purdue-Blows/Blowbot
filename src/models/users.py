import sqlite3
from typing import Dict, List


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
    ):
        self.name = name
        self.jazzle_streak = jazzle_streak
        self.jazz_trivia_correct = jazz_trivia_correct
        self.jazz_trivia_incorrect = jazz_trivia_incorrect
        self.jazz_trivia_percentage = jazz_trivia_percentage

    @staticmethod
    def from_map(map: Dict[str, any]) -> "User":  # type: ignore
        return User(
            name=map["name"],
            jazzle_streak=map["jazzle_streak"],
            jazz_trivia_correct=map["jazz_trivia_correct"],
            jazz_trivia_incorrect=map["jazz_trivia_incorrect"],
            jazz_trivia_percentage=map["jazz_trivia_percentage"],
        )

    # Adds a user instance to the users table
    @staticmethod
    async def add(user: "User") -> None:
        pass

    @staticmethod
    async def retrieve_many() -> List["User"]:
        # TODO: Retrieve the values that match the most specified params for the users table, in order
        # TODO: If the user is not an admin, they only see a limited amount of data
        pass

    async def retrieve_one(self, played: bool = False, random: bool = True) -> "User":
        # TODO: Retrieve the current user
        # TODO: If you are an admin, you can retrieve other users information as well
        pass

    @staticmethod
    async def update(user: "User") -> None:
        # TODO: updates the corresponding user instance in the database
        pass
