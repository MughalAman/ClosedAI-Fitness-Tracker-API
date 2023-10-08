from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum, Boolean
from sqlalchemy.orm import relationship

from .database import Base


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    gender = Column(Enum("MALE", "FEMALE", "OTHER"), nullable=False)
    friend_code = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(500), nullable=False)
    account_type = Column(Enum("ADMIN", "USER"), nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
    extra_data = Column(String(1000))

    friendships_requested = relationship(
        "Friendship", foreign_keys="[Friendship.user1_id]", back_populates="user1"
    )
    friendships_received = relationship(
        "Friendship", foreign_keys="[Friendship.user2_id]", back_populates="user2"
    )
    workouts = relationship("Workout", back_populates="user")


class Friendship(Base):
    __tablename__ = "friendship"

    user1_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    user2_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    status = Column(Enum("PENDING", "ACCEPTED"), nullable=False)

    user1 = relationship(
        "User", foreign_keys=[user1_id], back_populates="friendships_requested"
    )
    user2 = relationship(
        "User", foreign_keys=[user2_id], back_populates="friendships_received"
    )


class Workout(Base):
    __tablename__ = "workout"

    workout_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    date = Column(Date, nullable=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    is_private = Column(Boolean, nullable=False, default=True)

    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout")


class Exercise(Base):
    __tablename__ = "exercise"

    exercise_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(500))
    video_url = Column(String(500))
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=True)
    set = Column(Integer, nullable=False)
    repetition = Column(Integer, nullable=False)
    duration = Column(Integer, nullable=False)
    weight = Column(Float)
    rpe = Column(Integer)
    workout_id = Column(Integer, ForeignKey("workout.workout_id"), nullable=True)
    tags = Column(String(500))

    workout = relationship("Workout", back_populates="exercises")
    ratings = relationship("Rating", back_populates="exercise")


class Rating(Base):
    __tablename__ = "rating"

    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercise.exercise_id"), nullable=False)

    exercise = relationship("Exercise", back_populates="ratings")
