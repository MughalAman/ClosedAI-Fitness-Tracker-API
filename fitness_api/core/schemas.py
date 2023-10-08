from pydantic import BaseModel
from typing import Optional, List


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
    tags: Optional[str]


class ExerciseCreate(ExerciseBase):
    pass


class Exercise(ExerciseBase):
    exercise_id: int

    ratings: Optional[List["Rating"]]

    class Config:
        from_attributes = True


class WorkoutBase(BaseModel):
    name: str
    date: Optional[str]
    user_id: int


class WorkoutCreate(WorkoutBase):
    pass


class Workout(WorkoutBase):
    workout_id: int

    exercises: Optional[List["Exercise"]]

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    name: str
    email: str
    height: float
    weight: float
    gender: str
    friend_code: str
    password_hash: str
    account_type: str
    extra_data: Optional[str]


class User(UserBase):
    user_id: int
    friendships_requested: Optional[List["FriendshipBase"]]
    friendships_received: Optional[List["FriendshipBase"]]
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


class FriendshipBase(BaseModel):
    user1_id: int
    user2_id: int
    status: str


class FriendshipCreate(BaseModel):
    requestor_friend_code: str
    receiver_friend_code: str


class Friendship(FriendshipBase):
    user1: Optional["User"]
    user2: Optional["User"]

    class Config:
        from_attributes = True
