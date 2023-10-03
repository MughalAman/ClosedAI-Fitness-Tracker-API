from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: Optional[str]

class TokenData(BaseModel):
    user_email: Optional[str]

class UserBase(BaseModel):
    name: str
    email: str
    height: float
    weight: float
    gender: str
    friend_code: str
    password_hash: str
    account_type: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    user_id: int

    class Config:
        orm_mode = True

class FriendshipBase(BaseModel):
    user1_id: int
    user2_id: int
    status: str

class FriendshipCreate(FriendshipBase):
    pass

class Friendship(FriendshipBase):
    class Config:
        orm_mode = True

class UserExerciseBase(BaseModel):
    name: str
    description: Optional[str]
    video_url: Optional[str]
    user_id: int

class UserExerciseCreate(UserExerciseBase):
    pass

class UserExercise(UserExerciseBase):
    user_exercise_id: int

    class Config:
        orm_mode = True

class WorkoutPlanBase(BaseModel):
    name: str
    is_private: bool
    workout_days: Optional[str]
    user_id: int

class WorkoutPlanCreate(WorkoutPlanBase):
    pass

class WorkoutPlan(WorkoutPlanBase):
    plan_id: int

    class Config:
        orm_mode = True

class WorkoutBase(BaseModel):
    name: str
    date: str
    user_id: int
    plan_id: Optional[int]

class WorkoutCreate(WorkoutBase):
    pass

class Workout(WorkoutBase):
    workout_id: int

    class Config:
        orm_mode = True

class ExerciseBase(BaseModel):
    user_exercise_id: Optional[int]
    set: int
    repetition: int
    rating: float
    duration: int
    weight: Optional[float]
    rpe: Optional[int]
    workout_id: Optional[int]

class ExerciseCreate(ExerciseBase):
    pass

class Exercise(ExerciseBase):
    exercise_id: int

    class Config:
        orm_mode = True