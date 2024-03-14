from typing import Dict, List, Optional

from models.model_fields import UserFields
from sqlalchemy.orm import Session
from typing import Dict, List, Optional
from models.model_fields import UserFields
from sqlalchemy.orm import Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import BigInteger, Column, Integer, String, Float
from sqlalchemy.util import concurrency
from sqlalchemy.ext.declarative import declarative_base

from utils.constants import Base


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


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    jazzle_streak = Column(Integer)
    jazz_trivia_correct = Column(Integer)
    jazz_trivia_incorrect = Column(Integer)
    jazz_trivia_percentage = Column(Float)
    guild_id = Column(BigInteger, unique=True)

    @staticmethod
    def add_sync(session: Session, user: "User") -> Optional["User"]:
        try:
            session.add(user)
            session.commit()
            return user
        except:
            session.rollback()
            raise

    @staticmethod
    async def add(session: Session, user: "User"):
        return await concurrency.greenlet_spawn(User.add_sync, session, user)

    @staticmethod
    def retrieve_many_sync(
        session: Session,
        guild_id,
        name=None,
        jazzle_streak=None,
        jazz_trivia_correct=None,
        jazz_trivia_incorrect=None,
        jazz_trivia_percentage=None,
    ) -> Optional[List["User"]]:
        try:
            query = session.query(User).filter(User.guild_id == guild_id)
            if name is not None:
                query = query.filter(User.name == name)
            if jazzle_streak is not None:
                query = query.filter(User.jazzle_streak == jazzle_streak)
            if jazz_trivia_correct is not None:
                query = query.filter(User.jazz_trivia_correct == jazz_trivia_correct)
            if jazz_trivia_incorrect is not None:
                query = query.filter(
                    User.jazz_trivia_incorrect == jazz_trivia_incorrect
                )
            if jazz_trivia_percentage is not None:
                query = query.filter(
                    User.jazz_trivia_percentage == jazz_trivia_percentage
                )
            result = query.all()
            return result
        except:
            session.rollback()
            raise

    @staticmethod
    async def retrieve_many(
        session: Session,
        guild_id,
        name=None,
        jazzle_streak=None,
        jazz_trivia_correct=None,
        jazz_trivia_incorrect=None,
        jazz_trivia_percentage=None,
    ):
        return await concurrency.greenlet_spawn(
            User.retrieve_many_sync,
            session,
            guild_id,
            name,
            jazzle_streak,
            jazz_trivia_correct,
            jazz_trivia_incorrect,
            jazz_trivia_percentage,
        )

    @staticmethod
    def retrieve_one_sync(
        session: Session,
        guild_id,
        id=None,
        name=None,
        jazzle_streak=None,
        jazz_trivia_correct=None,
        jazz_trivia_incorrect=None,
        jazz_trivia_percentage=None,
    ) -> Optional["User"]:
        try:
            query = session.query(User).filter(User.guild_id == guild_id)
            if id is not None:
                query = query.filter(User.id == id)
            if name is not None:
                query = query.filter(User.name == name)
            if jazzle_streak is not None:
                query = query.filter(User.jazzle_streak == jazzle_streak)
            if jazz_trivia_correct is not None:
                query = query.filter(User.jazz_trivia_correct == jazz_trivia_correct)
            if jazz_trivia_incorrect is not None:
                query = query.filter(
                    User.jazz_trivia_incorrect == jazz_trivia_incorrect
                )
            if jazz_trivia_percentage is not None:
                query = query.filter(
                    User.jazz_trivia_percentage == jazz_trivia_percentage
                )
            result = query.first()
            return result
        except:
            session.rollback()
            raise

    @staticmethod
    async def retrieve_one(
        session: Session,
        guild_id,
        id=None,
        name=None,
        jazzle_streak=None,
        jazz_trivia_correct=None,
        jazz_trivia_incorrect=None,
        jazz_trivia_percentage=None,
    ):
        return await concurrency.greenlet_spawn(
            User.retrieve_one_sync,
            session,
            guild_id,
            id,
            name,
            jazzle_streak,
            jazz_trivia_correct,
            jazz_trivia_incorrect,
            jazz_trivia_percentage,
        )

    @staticmethod
    def update_sync(session: Session, user: "User") -> bool:
        try:
            update = session.merge(user)
            if update:
                session.commit()
                return True
            session.rollback()
            return False
        except:
            session.rollback()
            raise

    @staticmethod
    async def update(session: Session, user: "User"):
        return await concurrency.greenlet_spawn(User.update_sync, session, user)

    @staticmethod
    def log_doc(user: dict) -> None:
        print("USER")
        print(f"Id: {user[UserFields.ID.value]}")
        print(f"Name: {user[UserFields.NAME.value]}")
        print(f"Jazzle Streak: {user[UserFields.JAZZLE_STREAK.value]}")
        print(f"Jazz Trivia Correct: {user[UserFields.JAZZ_TRIVIA_CORRECT.value]}")
        print(f"Jazz Trivia Incorrect: {user[UserFields.JAZZ_TRIVIA_INCORRECT.value]}")
        print(
            f"Jazz Trivia Percentage: {user[UserFields.JAZZ_TRIVIA_PERCENTAGE.value]}"
        )
        print(f"Guild Id: {user[UserFields.GUILD_ID.value]}")

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
        ) + "\n Guild Id: " + str(
            self.guild_id
        )
