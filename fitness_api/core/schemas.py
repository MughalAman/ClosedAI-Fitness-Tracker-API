from pydantic import BaseModel
from typing import Optional, List
from enum import Enum
from datetime import date


class GenderEnum(str, Enum):
    MALE = "MALE"
    FEMALE = "FEMALE"
    OTHER = "OTHER"


class AccountTypeEnum(str, Enum):
    ADMIN = "ADMIN"
    USER = "USER"


class StatusEnum(str, Enum):
    PENDING = "PENDING"
    ACCEPTED = "ACCEPTED"


class Token(BaseModel):
    access_token: str
    token_type: Optional[str]


class TokenData(BaseModel):
    user_email: Optional[str]


class RatingBase(BaseModel):
    rating: float
    user_id: int
    exercise_id: int


class RatingCreate(RatingBase):
    pass


class Rating(RatingBase):
    rating_id: int

    class Config:
        from_attributes = True


# Base schema for Tag
class TagBase(BaseModel):
    name: str

    class Config:
        from_attributes = True


class Tag(TagBase):
    tag_id: int

    class Config:
        from_attributes = True


# Schema for reading (or retrieving) a Tag
class TagRead(TagBase):
    tag_id: int


# Schema for creating a Tag
class TagCreate(TagBase):
    pass


# Schema for updating a Tag
class TagUpdate(BaseModel):
    name: Optional[str]

    class Config:
        from_attributes = True


class ExerciseBase(BaseModel):
    name: str
    description: Optional[str]
    video_url: Optional[str]
    user_id: Optional[int]
    set: int
    repetition: int
    duration: int
    weight: Optional[float]
    rpe: Optional[int]
    workout_id: Optional[int]


class ExerciseCreate(ExerciseBase):
    tags: List[str] = []


class ExerciseUpdate(ExerciseBase):
    tags: Optional[List[str]]


class ExerciseRead(ExerciseBase):
    exercise_id: int
    tags: List[Tag] = []

    class Config:
        from_attributes = True


class WorkoutDateBase(BaseModel):
    date: date
    completed: bool


class WorkoutDateCreate(WorkoutDateBase):
    workout_id: int


class WorkoutDate(WorkoutDateBase):
    id: int

    class Config:
        from_attributes = True


class WorkoutBase(BaseModel):
    name: str
    user_id: int


class WorkoutCreate(WorkoutBase):
    dates: Optional[List[WorkoutDateBase]]


class WorkoutUpdate(BaseModel):
    name: Optional[str]
    user_id: Optional[int]


class Workout(WorkoutBase):
    workout_id: int
    exercises: Optional[List["ExerciseRead"]]
    dates: Optional[List[WorkoutDate]]

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    profile_pic_url: Optional[str]
    email: str
    height: float
    weight: float
    gender: GenderEnum
    birth_date: Optional[date]
    friend_code: str
    account_type: AccountTypeEnum
    disabled: Optional[bool] = False
    extra_data: Optional[dict]


class User(UserBase):
    user_id: int
    workouts: Optional[List["Workout"]]

    class Config:
        from_attributes = True


class UserCreate(BaseModel):
    name: str
    email: str
    password: str
    height: float
    weight: float
    gender: str
    birth_date: Optional[date]


class UserUpdate(BaseModel):
    name: Optional[str] = None
    profile_pic_url: Optional[str] = None
    email: Optional[str] = None
    height: Optional[float] = None
    weight: Optional[float] = None
    gender: Optional[str] = None
    extra_data: Optional[dict] = None


class FriendshipStatusBase(BaseModel):
    name: StatusEnum


class FriendshipStatusCreate(FriendshipStatusBase):
    pass


class FriendshipStatusInDB(FriendshipStatusBase):
    status_id: int

    class Config:
        from_attributes = True


class FriendshipBase(BaseModel):
    user_id: int
    friend_id: int
    status_id: int


class FriendshipCreate(FriendshipBase):
    pass


class FriendshipInDB(FriendshipBase):
    friendship_id: int

    class Config:
        from_attributes = True


class LangCreate(BaseModel):
    ru_RU: dict
    tr_TR: dict


class LangUpdate(BaseModel):
    ru_RU: Optional[dict] = None
    tr_TR: Optional[dict] = None


class LangRead(LangCreate):
    lang_id: int

    class Config:
        from_attributes = True