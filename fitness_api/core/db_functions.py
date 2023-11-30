from datetime import datetime, timedelta

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import IntegrityError
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
        logger.debug(
            f"User {user_email} attempted to log in with an incorrect password"
        )
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
    encoded_jwt = jwt.encode(
        to_encode, SETTINGS.secret_key, algorithm=SETTINGS.algorithm
    )
    return encoded_jwt


def generate_friend_code(db: Session):
    friend_code = ""
    while True:
        friend_code = "".join(
            random.choices(string.ascii_uppercase + string.digits, k=6)
        )
        if (
            not db.query(models.User)
            .filter(models.User.friend_code == friend_code)
            .first()
        ):
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
        birth_date=user_data.birth_date,
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


def update_user(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = get_user(db, user_id=user_id)
    try:
        for key, value in user.model_dump().items():
            if value is not None:
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


def get_user_id_from_friend_code(db: Session, friend_code: str):
    return (
        db.query(models.User)
        .filter(models.User.friend_code == friend_code)
        .first()
        .user_id
    )


def create_friendship_status(
    db: Session, status: schemas.FriendshipStatusCreate
) -> models.FriendshipStatus:
    db_status = models.FriendshipStatus(name=status.name)
    db.add(db_status)
    db.commit()
    db.refresh(db_status)
    return db_status


def update_friendship_status(
    db: Session, status_id: int, new_status: schemas.FriendshipStatusCreate
) -> models.FriendshipStatus:
    db_status = (
        db.query(models.FriendshipStatus)
        .filter(models.FriendshipStatus.status_id == status_id)
        .first()
    )
    if not db_status:
        return None  # Or raise an appropriate exception
    db_status.name = new_status.name
    db.commit()
    db.refresh(db_status)
    return db_status


def get_friendship_status(db: Session, status_id: int):
    return (
        db.query(models.FriendshipStatus)
        .filter(models.FriendshipStatus.status_id == status_id)
        .first()
    )


def get_all_friendship_statuses(db: Session):
    return db.query(models.FriendshipStatus).all()


def delete_friendship_status(db: Session, status_id: int):
    status = (
        db.query(models.FriendshipStatus)
        .filter(models.FriendshipStatus.status_id == status_id)
        .first()
    )
    db.delete(status)
    db.commit()


def create_friendship(
    db: Session, friendship: schemas.FriendshipCreate
) -> models.Friendship:
    db_friendship = models.Friendship(
        user_id=friendship.user_id,
        friend_id=friendship.friend_id,
        status_id=friendship.status_id,
    )
    db.add(db_friendship)
    db.commit()
    db.refresh(friendship)
    return friendship


def get_friendship(db: Session, friendship_id: int):
    return (
        db.query(models.Friendship)
        .filter(models.Friendship.friendship_id == friendship_id)
        .first()
    )


def get_all_friendships(db: Session):
    return db.query(models.Friendship).all()


def get_all_friendships_for_user(db: Session, user_id: int):
    return (
        db.query(models.Friendship)
        .filter(
            (models.Friendship.user_id == user_id)
            | (models.Friendship.friend_id == user_id)
        )
        .all()
    )


def update_friendships_status(
    db: Session, friendship_id: int, status_id: int
) -> models.Friendship:
    db_friendship = (
        db.query(models.Friendship)
        .filter(models.Friendship.friendship_id == friendship_id)
        .first()
    )

    if not db_friendship:
        return None

    db_friendship.status_id = status_id
    db.commit()
    db.refresh(db_friendship)
    return db_friendship


def delete_friendship(db: Session, friendship_id: int):
    friendship = (
        db.query(models.Friendship)
        .filter(models.Friendship.friendship_id == friendship_id)
        .first()
    )
    db.delete(friendship)
    db.commit()


def create_workout(db: Session, workout: schemas.WorkoutCreate):
    db_workout = models.Workout(user_id=workout.user_id, name=workout.name)
    try:
        db.add(db_workout)
        db.commit()
        db.refresh(db_workout)
        logger.debug(f"Created workout {db_workout.workout_id}")

        if workout.dates:
            for workout_date in workout.dates:
                db_date = models.WorkoutDate(
                    workout_id=db_workout.workout_id, date=workout_date.date
                )
                db.add(db_date)
            db.commit()
            logger.debug(f"Added dates to workout {db_workout.workout_id}")
    except Exception as e:
        logger.error(f"Error creating workout: {e}")
        db.rollback()
        raise e
    return db_workout


def get_workout(db: Session, workout_id: int):
    try:
        return (
            db.query(models.Workout)
            .options(joinedload(models.Workout.dates))
            .filter(models.Workout.workout_id == workout_id)
            .first()
        )
    except Exception as e:
        logger.error(f"Error fetching workout with id {workout_id}: {e}")
        raise e


def update_workout(db: Session, workout_id: int, workout: schemas.WorkoutUpdate):
    db_workout = get_workout(db, workout_id)
    try:
        for key, value in workout.model_dump().items():
            if value is not None:
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


def create_workout_date(db: Session, workout_date: schemas.WorkoutDateCreate):
    db_date = models.WorkoutDate(
        workout_id=workout_date.workout_id, date=workout_date.date
    )
    try:
        db.add(db_date)
        db.commit()
        db.refresh(db_date)
        logger.debug(f"Created workout date {db_date.id}")
    except Exception as e:
        logger.error(f"Error creating workout date: {e}")
        db.rollback()
        raise e
    return db_date


def delete_workout_date(db: Session, workout_date_id: int):
    db_date = (
        db.query(models.WorkoutDate)
        .filter(models.WorkoutDate.id == workout_date_id)
        .first()
    )
    try:
        db.delete(db_date)
        db.commit()
        logger.debug(f"Deleted workout date {workout_date_id}")
    except Exception as e:
        logger.error(f"Error deleting workout date {workout_date_id}: {e}")
        db.rollback()
        raise e
    return db_date


def create_exercise(db: Session, exercise: schemas.ExerciseCreate) -> models.Exercise:
    exercise_data = exercise.model_dump()

    tag_names = exercise_data.pop("tags", [])
    tag_objects = []

    # Check and fetch or create Tag objects
    for tag_name in tag_names:
        tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        if not tag:
            tag = models.Tag(name=tag_name)
            db.add(tag)
            try:
                db.commit()
            except IntegrityError:
                db.rollback()
                tag = db.query(models.Tag).filter(models.Tag.name == tag_name).first()
        tag_objects.append(tag)

    new_exercise = models.Exercise(**exercise_data)
    new_exercise.tags = tag_objects

    db.add(new_exercise)
    db.commit()
    db.refresh(new_exercise)

    return new_exercise


def get_exercise(db: Session, exercise_id: int):
    try:
        return (
            db.query(models.Exercise)
            .filter(models.Exercise.exercise_id == exercise_id)
            .first()
        )
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


def create_rating(db: Session, rating: schemas.RatingCreate):
    db_rating = models.Rating(**rating.model_dump())
    try:
        db.add(db_rating)
        db.commit()
        db.refresh(db_rating)
        logger.debug(f"Created rating {db_rating.rating_id}")
    except Exception as e:
        logger.error(f"Error creating rating: {e}")
        db.rollback()
        raise e
    return db_rating


def get_rating(db: Session, rating_id: int):
    try:
        return (
            db.query(models.Rating).filter(models.Rating.rating_id == rating_id).first()
        )
    except Exception as e:
        logger.error(f"Error fetching rating with id {rating_id}: {e}")
        raise e


def update_rating(db: Session, rating_id: int, rating: schemas.RatingCreate):
    db_rating = get_rating(db, rating_id)
    try:
        for key, value in rating.model_dump().items():
            setattr(db_rating, key, value)
        db.commit()
        db.refresh(db_rating)
        logger.debug(f"Updated rating {rating_id}")
    except Exception as e:
        logger.error(f"Error updating rating {rating_id}: {e}")
        db.rollback()
        raise e
    return db_rating


def delete_rating(db: Session, rating_id: int):
    db_rating = get_rating(db, rating_id)
    try:
        db.delete(db_rating)
        db.commit()
        logger.debug(f"Deleted rating {rating_id}")
    except Exception as e:
        logger.error(f"Error deleting rating {rating_id}: {e}")
        db.rollback()
        raise e
    return db_rating


def create_tag(db: Session, tag: schemas.TagCreate):
    new_tag = models.Tag(**tag.model_dump())
    db.add(new_tag)
    db.commit()
    db.refresh(new_tag)
    return new_tag


def get_tag(db: Session, tag_id: int):
    return db.query(models.Tag).filter(models.Tag.tag_id == tag_id).first()


def get_tags(db: Session, skip: int = 0, limit: int = 10):
    return db.query(models.Tag).offset(skip).limit(limit).all()


def update_tag(db: Session, tag_id: int, tag: schemas.TagUpdate):
    existing_tag = db.query(models.Tag).filter(models.Tag.tag_id == tag_id).first()
    if not existing_tag:
        return None
    for key, value in tag.dict().items():
        if value is not None:
            setattr(existing_tag, key, value)
    db.commit()
    db.refresh(existing_tag)
    return existing_tag


def delete_tag(db: Session, tag_id: int):
    tag = db.query(models.Tag).filter(models.Tag.tag_id == tag_id).first()
    if not tag:
        return None
    db.delete(tag)
    db.commit()
    return tag


def create_lang(db: Session, lang: schemas.LangCreate):
    new_lang = models.Lang(**lang.model_dump())
    db.add(new_lang)
    db.commit()
    db.refresh(new_lang)
    return new_lang


def get_lang(db: Session, lang_id: int):
    return db.query(models.Lang).filter(models.Lang.lang_id == lang_id).first()


def update_lang(db: Session, lang_id: int, lang: schemas.LangUpdate):
    existing_lang = db.query(models.Lang).filter(models.Lang.lang_id == lang_id).first()
    if not existing_lang:
        return None
    for key, value in lang.dict().items():
        if value is not None:
            setattr(existing_lang, key, value)
    db.commit()
    db.refresh(existing_lang)
    return existing_lang


def delete_lang(db: Session, lang_id: int):
    lang = db.query(models.Lang).filter(models.Lang.lang_id == lang_id).first()
    if not lang:
        return None
    db.delete(lang)
    db.commit()
    return lang
