from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()



class User(Base):
    __tablename__ = "user"

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    height = Column(Float, nullable=False)
    weight = Column(Float, nullable=False)
    gender = Column(Enum('MALE', 'FEMALE', 'OTHER'), nullable=False)
    friend_code = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(500), nullable=False)
    gender = relationship("Gender", back_populates="users")
    account_type = Column(Enum('ADMIN', 'USER'), nullable=False)
    friendships = relationship("Friendship", back_populates="user1")
    user_exercises = relationship("UserExercise", back_populates="user")
    workout_plans = relationship("WorkoutPlan", back_populates="user")
    workouts = relationship("Workout", back_populates="user")


class Friendship(Base):
    __tablename__ = "friendship"

    user1_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    user2_id = Column(Integer, ForeignKey("user.user_id"), primary_key=True)
    status = Column(Enum("PENDING", "ACCEPTED"), nullable=False)

    user1 = relationship("User", back_populates="friendships")
    user2 = relationship("User", foreign_keys=[user2_id])


class UserExercise(Base):
    __tablename__ = "user_exercise"

    user_exercise_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    description = Column(String(500))
    video_url = Column(String(500))
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)

    user = relationship("User", back_populates="user_exercises")
    exercises = relationship("Exercise", back_populates="user_exercise")


class WorkoutPlan(Base):
    __tablename__ = "workout_plan"

    plan_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(500), nullable=False)
    is_private = Column(Boolean, nullable=False)
    workout_days = Column(String(7))
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)

    user = relationship("User", back_populates="workout_plans")
    workouts = relationship("Workout", back_populates="workout_plan")


class Workout(Base):
    __tablename__ = "workout"

    workout_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    date = Column(Date, nullable=False)
    user_id = Column(Integer, ForeignKey("user.user_id"), nullable=False)
    plan_id = Column(Integer, ForeignKey("workout_plan.plan_id"))

    user = relationship("User", back_populates="workouts")
    workout_plan = relationship("WorkoutPlan", back_populates="workouts")
    exercises = relationship("Exercise", back_populates="workout")


class Exercise(Base):
    __tablename__ = "exercise"

    exercise_id = Column(Integer, primary_key=True, autoincrement=True)
    user_exercise_id = Column(Integer, ForeignKey('user_exercise.user_exercise_id'), nullable=True)
    set = Column(Integer, nullable=False)
    repetition = Column(Integer, nullable=False)
    rating = Column(Float, nullable=False)
    duration = Column(Integer, nullable=False)
    weight = Column(Float)
    rpe = Column(Integer)
    workout_id = Column(Integer, ForeignKey('workout.workout_id'), nullable=True)
    
    workout = relationship("Workout", back_populates="exercises")
    user_exercise = relationship("UserExercise", back_populates="exercises")
