from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    ForeignKey,
    Date,
    Boolean,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import ENUM, JSON
from .database import Base

gender_enum = ENUM("MALE", "FEMALE", "OTHER", name="gender_enum_type")
account_type_enum = ENUM("ADMIN", "USER", name="account_type_enum")
status_enum = ENUM("PENDING", "ACCEPTED", name="status_enum_type")


class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    gender = Column(gender_enum, nullable=False)
    friend_code = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(500), nullable=False)
    account_type = Column(account_type_enum, nullable=False)
    disabled = Column(Boolean, nullable=False, default=False)
    extra_data = Column(JSON)

    workouts = relationship("Workout", back_populates="user")


# Redesigned Friendship
class FriendshipStatus(Base):
    __tablename__ = "friendship_status"

    status_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(status_enum, nullable=False)

    friendships = relationship("Friendship", back_populates="status")


class Friendship(Base):
    __tablename__ = "friendship"

    friendship_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    friend_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    status_id = Column(
        Integer, ForeignKey("friendship_status.status_id"), nullable=False
    )

    status = relationship("FriendshipStatus", back_populates="friendships")

    __table_args__ = (UniqueConstraint("user_id", "friend_id", name="uq_friendship"),)


class WorkoutDate(Base):
    __tablename__ = "workout_date"

    id = Column(Integer, primary_key=True, autoincrement=True)
    workout_id = Column(Integer, ForeignKey("workout.workout_id"), nullable=False)
    date = Column(Date, nullable=False)

    workout = relationship("Workout", back_populates="dates")


class Workout(Base):
    __tablename__ = "workout"

    workout_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    is_private = Column(Boolean, nullable=False, default=True)

    user = relationship("User", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout")

    dates = relationship("WorkoutDate", back_populates="workout")


class Tag(Base):
    __tablename__ = "tag"

    tag_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)


class ExerciseTag(Base):
    __tablename__ = "exercise_tag"

    exercise_id = Column(Integer, ForeignKey("exercise.exercise_id"), primary_key=True)
    tag_id = Column(Integer, ForeignKey("tag.tag_id"), primary_key=True)


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

    workout = relationship("Workout", back_populates="exercises")
    tags = relationship("Tag", secondary="exercise_tag")
    ratings = relationship("Rating", back_populates="exercise")


class Rating(Base):
    __tablename__ = "rating"

    rating_id = Column(Integer, primary_key=True, autoincrement=True)
    rating = Column(Float, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    exercise_id = Column(Integer, ForeignKey("exercise.exercise_id"), nullable=False)

    exercise = relationship("Exercise", back_populates="ratings")
