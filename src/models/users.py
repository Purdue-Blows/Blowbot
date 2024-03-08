from enum import Enum
from re import U
from typing import Dict, List, Optional

from models.model_fields import UserFields


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
    def log_doc(user: "User") -> None:
        print("USER DOC")
        print(f"Id: {user.id}")
        print(f"Name: {user.name}")
        print(f"Jazzle Streak: {user.jazzle_streak}")
        print(f"Jazz Trivia Correct: {user.jazz_trivia_correct}")
        print(f"Jazz Trivia Incorrect: {user.jazz_trivia_incorrect}")
        print(f"Jazz Trivia Percentage: {user.jazz_trivia_percentage}")

    @staticmethod
    def from_map(map: Dict[str, any]) -> "User":  # type: ignore
        return User(
            id=map[UserFields.ID.name],
            name=map[UserFields.NAME.name],
            jazzle_streak=map[UserFields.JAZZLE_STREAK.name],
            jazz_trivia_correct=map[UserFields.JAZZ_TRIVIA_CORRECT.name],
            jazz_trivia_incorrect=map[UserFields.JAZZ_TRIVIA_INCORRECT.name],
            jazz_trivia_percentage=map[UserFields.JAZZ_TRIVIA_PERCENTAGE.name],
        )

    # Adds a user instance to the users table
    @staticmethod
    async def add(db, user: "User") -> Optional["User"]:
        result = await db.users.insert_one(
            {
                UserFields.NAME.name: user.name,
                UserFields.JAZZLE_STREAK.name: user.jazzle_streak,
                UserFields.JAZZ_TRIVIA_CORRECT.name: user.jazz_trivia_correct,
                UserFields.JAZZ_TRIVIA_INCORRECT.name: user.jazz_trivia_incorrect,
                UserFields.JAZZ_TRIVIA_PERCENTAGE.name: user.jazz_trivia_percentage,
            }
        )
        user.id = result.inserted_id
        return user

    @staticmethod
    async def retrieve_many(
        db,
        name=None,
        jazzle_streak=None,
        jazz_trivia_correct=None,
        jazz_trivia_incorrect=None,
        jazz_trivia_percentage=None,
    ) -> Optional[List["User"]]:
        query = {}
        if name is not None:
            query[UserFields.NAME.name] = name
        if jazzle_streak is not None:
            query[UserFields.JAZZLE_STREAK.name] = jazzle_streak
        if jazz_trivia_correct is not None:
            query[UserFields.JAZZ_TRIVIA_CORRECT.name] = jazz_trivia_correct
        if jazz_trivia_incorrect is not None:
            query[UserFields.JAZZ_TRIVIA_INCORRECT.name] = jazz_trivia_incorrect
        if jazz_trivia_percentage is not None:
            query[UserFields.JAZZ_TRIVIA_PERCENTAGE.name] = jazz_trivia_percentage

        result = await db.users.find(query).to_list(length=None)
        return [User.from_map(row) for row in result]

    @staticmethod
    async def retrieve_one(
        db,
        id=None,
        name=None,
        jazzle_streak=None,
        jazz_trivia_correct=None,
        jazz_trivia_incorrect=None,
        jazz_trivia_percentage=None,
    ) -> Optional["User"]:
        query = {}
        if id is not None:
            query[UserFields.ID.name] = id
        if name is not None:
            query[UserFields.NAME.name] = name
        if jazzle_streak is not None:
            query[UserFields.JAZZLE_STREAK.name] = jazzle_streak
        if jazz_trivia_correct is not None:
            query[UserFields.JAZZ_TRIVIA_CORRECT.name] = jazz_trivia_correct
        if jazz_trivia_incorrect is not None:
            query[UserFields.JAZZ_TRIVIA_INCORRECT.name] = jazz_trivia_incorrect
        if jazz_trivia_percentage is not None:
            query[UserFields.JAZZ_TRIVIA_PERCENTAGE.name] = jazz_trivia_percentage

        result = await db.users.find_one(query)
        if result is None:
            return None
        return User.from_map(result)

    @staticmethod
    async def update(db, user: "User") -> Optional["User"]:
        query = {UserFields.ID.name: user.id}
        update = {
            "$set": {
                UserFields.NAME.name: user.name,
                UserFields.JAZZLE_STREAK.name: user.jazzle_streak,
                UserFields.JAZZ_TRIVIA_CORRECT.name: user.jazz_trivia_correct,
                UserFields.JAZZ_TRIVIA_INCORRECT.name: user.jazz_trivia_incorrect,
                UserFields.JAZZ_TRIVIA_PERCENTAGE.name: user.jazz_trivia_percentage,
            }
        }
        await db.users.update_one(query, update)
        return user

    def to_string(self):
        return "USER\n" "Id: " + str(
            self.id
        ) + "\n Name: " + self.name + "\n Jazzle Streak: " + str(
            self.jazzle_streak
        ) + "\n Jazz Trivia Correct:" + str(
            self.jazz_trivia_correct
        ) + "\n Jazz Trivia Incorrect:" + str(
            self.jazz_trivia_incorrect
        ) + "\n Jazz Trivia Percentage:" + str(
            self.jazz_trivia_percentage
        )
