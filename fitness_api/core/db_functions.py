from datetime import datetime, timedelta

from sqlalchemy.orm import Session
from jose import jwt
from passlib.context import CryptContext

from fitness_api.settings import SETTINGS

from . import database, models, schemas
from .logging import logger

import random
import string

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_database():
    try:
        return database.Base.metadata.create_all(bind=database.engine)
    except Exception as e:
        logger.error(f"Error creating database: {e}")
        raise e


def get_database():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


def verify_password(plain_password, password_hash):
    return pwd_context.verify(plain_password, password_hash)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db: Session, user_email: str | None = None, user_id: int | None = None):
    try:
        if user_email:
            return db.query(models.User).filter(models.User.email == user_email).first()
        elif user_id:
            return db.query(models.User).filter(models.User.user_id == user_id).first()
        else:
            raise Exception("Must provide either user_email or user_id")
    except Exception as e:
        logger.error(f"Error fetching user: {e}")
        raise e


def authenticate_user(db: Session, user_email: str, password: str):
    user = get_user(db, user_email=user_email)
    if not user:
        logger.debug(f"User {user_email} attempted to log in but does not exist")
        return False
    if not verify_password(password, user.password_hash):
        logger.debug(f"User {user_email} attempted to log in with an incorrect password")
        return False
    
    logger.debug(f"User {user_email} successfully logged in")
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SETTINGS.secret_key, algorithm=SETTINGS.algorithm)
    return encoded_jwt


def generate_friend_code(db: Session):
    friend_code = ""
    while True:
        friend_code = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        if not db.query(models.User).filter(models.User.friend_code == friend_code).first():
            logger.debug(f"Generated friend code {friend_code}")
            break
        logger.debug(f"Friend code {friend_code} already exists, generating another")
    return friend_code


def create_user(db: Session, user_data: schemas.UserCreate):
    db_user = models.User(
        name=user_data.name,
        email=user_data.email,
        height=user_data.height,
        weight=user_data.weight,
        gender=user_data.gender,
        friend_code=generate_friend_code(db),
        password_hash=get_password_hash(user_data.password),
        account_type="USER",
    )

    try:
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

        logger.debug(f"Created user {user_data.email}")
    except Exception as e:
        logger.error(f"Error creating user: {e}")
        db.rollback()
        raise e

    return db_user


def update_user(db: Session, user_id: int, user: schemas.UserCreate):
    db_user = get_user(db, user_id=user_id)
    try:
        for key, value in user.model_dump().items():
            setattr(db_user, key, value)
        db.commit()
        db.refresh(db_user)
        logger.debug(f"Updated user {user_id}")
    except Exception as e:
        logger.error(f"Error updating user {user_id}: {e}")
        db.rollback()
        raise e
    return db_user



def delete_user(db: Session, user_id: int):
    db_user = get_user(db, user_id=user_id)
    try:
        db.delete(db_user)
        db.commit()
        logger.debug(f"Deleted user {user_id}")
    except Exception as e:
        logger.error(f"Error deleting user {user_id}: {e}")
        db.rollback()
        raise e
    return db_user


def create_friendship(db: Session, friendship: schemas.FriendshipCreate):
    db_friendship = models.Friendship(**friendship.model_dump())
    try:
        db.add(db_friendship)
        db.commit()
        db.refresh(db_friendship)
        logger.debug(f"Created friendship between {friendship.user1_id} and {friendship.user2_id}")
    except Exception as e:
        logger.error(f"Error creating friendship: {e}")
        db.rollback()
        raise e
    return db_friendship

def get_friendship(db: Session, user1_id: int, user2_id: int):
    try:
        return (
            db.query(models.Friendship)
            .filter(models.Friendship.user1_id == user1_id, models.Friendship.user2_id == user2_id)
            .first()
            )
    except Exception as e:
        logger.error(f"Error fetching friendship between {user1_id} and {user2_id}: {e}")
        raise e


def update_friendship(db: Session, user1_id: int, user2_id: int, friendship: schemas.FriendshipCreate):
    db_friendship = get_friendship(db, user1_id, user2_id)
    try:
        for key, value in friendship.model_dump().items():
            setattr(db_friendship, key, value)
        db.commit()
        db.refresh(db_friendship)
        logger.debug(f"Updated friendship between {user1_id} and {user2_id}")
    except Exception as e:
        logger.error(f"Error updating friendship between {user1_id} and {user2_id}: {e}")
        db.rollback()
        raise e
    return db_friendship



def delete_friendship(db: Session, user1_id: int, user2_id: int):
    db_friendship = get_friendship(db, user1_id, user2_id)
    try:
        db.delete(db_friendship)
        db.commit()
        logger.debug(f"Deleted friendship between {user1_id} and {user2_id}")
    except Exception as e:
        logger.error(f"Error deleting friendship between {user1_id} and {user2_id}: {e}")
        db.rollback()
        raise e
    return db_friendship



def create_user_exercise(db: Session, user_exercise: schemas.UserExerciseCreate):
    db_user_exercise = models.UserExercise(**user_exercise.model_dump())
    try:
        db.add(db_user_exercise)
        db.commit()
        db.refresh(db_user_exercise)
        logger.debug(f"Created user exercise {db_user_exercise.user_exercise_id}")
    except Exception as e:
        logger.error(f"Error creating user exercise: {e}")
        db.rollback()
        raise e
    return db_user_exercise


def get_user_exercise(db: Session, user_exercise_id: int):
    try:
        return db.query(models.UserExercise).filter(models.UserExercise.user_exercise_id == user_exercise_id).first()
    except Exception as e:
        logger.error(f"Error fetching user exercise with id {user_exercise_id}: {e}")
        raise e


def update_user_exercise(db: Session, user_exercise_id: int, user_exercise: schemas.UserExerciseCreate):
    db_user_exercise = get_user_exercise(db, user_exercise_id)
    try:
        for key, value in user_exercise.model_dump().items():
            setattr(db_user_exercise, key, value)
        db.commit()
        db.refresh(db_user_exercise)
        logger.debug(f"Updated user exercise {user_exercise_id}")
    except Exception as e:
        logger.error(f"Error updating user exercise {user_exercise_id}: {e}")
        db.rollback()
        raise e
    return db_user_exercise



def delete_user_exercise(db: Session, user_exercise_id: int):
    db_user_exercise = get_user_exercise(db, user_exercise_id)
    try:
        db.delete(db_user_exercise)
        db.commit()
        logger.debug(f"Deleted user exercise {user_exercise_id}")
    except Exception as e:
        logger.error(f"Error deleting user exercise {user_exercise_id}: {e}")
        db.rollback()
        raise e
    return db_user_exercise


def create_workout_plan(db: Session, workout_plan: schemas.WorkoutPlanCreate):
    db_workout_plan = models.WorkoutPlan(**workout_plan.model_dump())
    try:
        db.add(db_workout_plan)
        db.commit()
        db.refresh(db_workout_plan)
        logger.debug(f"Created workout plan {db_workout_plan.plan_id}")
    except Exception as e:
        logger.error(f"Error creating workout plan: {e}")
        db.rollback()
        raise e
    return db_workout_plan


def get_workout_plan(db: Session, plan_id: int):
    try:
        return db.query(models.WorkoutPlan).filter(models.WorkoutPlan.plan_id == plan_id).first()
    except Exception as e:
        logger.error(f"Error fetching workout plan with id {plan_id}: {e}")
        raise e


def update_workout_plan(db: Session, plan_id: int, workout_plan: schemas.WorkoutPlanCreate):
    db_workout_plan = get_workout_plan(db, plan_id)
    try:
        for key, value in workout_plan.model_dump().items():
            setattr(db_workout_plan, key, value)
        db.commit()
        db.refresh(db_workout_plan)
        logger.debug(f"Updated workout plan {plan_id}")
    except Exception as e:
        logger.error(f"Error updating workout plan {plan_id}: {e}")
        db.rollback()
        raise e
    return db_workout_plan


def delete_workout_plan(db: Session, plan_id: int):
    db_workout_plan = get_workout_plan(db, plan_id)
    try:
        db.delete(db_workout_plan)
        db.commit()
        logger.debug(f"Deleted workout plan {plan_id}")
    except Exception as e:
        logger.error(f"Error deleting workout plan {plan_id}: {e}")
        db.rollback()
        raise e
    return db_workout_plan



def create_workout(db: Session, workout: schemas.WorkoutCreate):
    db_workout = models.Workout(**workout.model_dump())
    try:
        db.add(db_workout)
        db.commit()
        db.refresh(db_workout)
        logger.debug(f"Created workout {db_workout.workout_id}")
    except Exception as e:
        logger.error(f"Error creating workout: {e}")
        db.rollback()
        raise e
    return db_workout


def get_workout(db: Session, workout_id: int):
    try:
        return db.query(models.Workout).filter(models.Workout.workout_id == workout_id).first()
    except Exception as e:
        logger.error(f"Error fetching workout with id {workout_id}: {e}")
        raise e


def update_workout(db: Session, workout_id: int, workout: schemas.WorkoutCreate):
    db_workout = get_workout(db, workout_id)
    try:
        for key, value in workout.model_dump().items():
            setattr(db_workout, key, value)
        db.commit()
        db.refresh(db_workout)
        logger.debug(f"Updated workout {workout_id}")
    except Exception as e:
        logger.error(f"Error updating workout {workout_id}: {e}")
        db.rollback()
        raise e
    return db_workout


def delete_workout(db: Session, workout_id: int):
    db_workout = get_workout(db, workout_id)
    try:
        db.delete(db_workout)
        db.commit()
        logger.debug(f"Deleted workout {workout_id}")
    except Exception as e:
        logger.error(f"Error deleting workout {workout_id}: {e}")
        db.rollback()
        raise e
    return db_workout


def create_exercise(db: Session, exercise: schemas.ExerciseCreate):
    try:
        db_exercise = models.Exercise(**exercise.model_dump())
        db.add(db_exercise)
        db.commit()
        db.refresh(db_exercise)
        logger.debug(f"Created exercise {db_exercise.exercise_id}")
    except Exception as e:
        logger.error(f"Error creating exercise: {e}")
        db.rollback()
        raise e


def get_exercise(db: Session, exercise_id: int):
    try:
        return db.query(models.Exercise).filter(models.Exercise.exercise_id == exercise_id).first()
    except Exception as e:
        logger.error(f"Error fetching exercise with id {exercise_id}: {e}")
        raise e


def update_exercise(db: Session, exercise_id: int, exercise: schemas.ExerciseCreate):
    db_exercise = get_exercise(db, exercise_id)
    try:
        for key, value in exercise.model_dump().items():
            setattr(db_exercise, key, value)
        db.commit()
        db.refresh(db_exercise)
        logger.debug(f"Updated exercise {exercise_id}")
    except Exception as e:
        logger.error(f"Error updating exercise {exercise_id}: {e}")
        db.rollback()
        raise e
    return db_exercise



def delete_exercise(db: Session, exercise_id: int):
    db_exercise = get_exercise(db, exercise_id)
    try:
        db.delete(db_exercise)
        db.commit()
        logger.debug(f"Deleted exercise {exercise_id}")
    except Exception as e:
        logger.error(f"Error deleting exercise {exercise_id}: {e}")
        db.rollback()
        raise e
    return db_exercise
