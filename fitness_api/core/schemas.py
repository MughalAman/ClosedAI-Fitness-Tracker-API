from pydantic import BaseModel
from typing import Optional, List

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


class User(UserBase):
    user_id: int
    friendships_requested: Optional[List['FriendshipBase']]
    friendships_received: Optional[List['FriendshipBase']]
    user_exercises: Optional[List['UserExerciseBase']]
    workout_plans: Optional[List['WorkoutPlanBase']]
    workouts: Optional[List['WorkoutBase']]

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
    user1: Optional['User']
    user2: Optional['User']
    
    class Config:
        from_attributes = True

class UserExerciseBase(BaseModel):
    name: str
    description: Optional[str]
    video_url: Optional[str]
    user_id: int

class UserExerciseCreate(UserExerciseBase):
    pass

class UserExercise(UserExerciseBase):
    user_exercise_id: int
    user: Optional['User']
    exercises: Optional[List['Exercise']]

    class Config:
        from_attributes = True

class WorkoutPlanBase(BaseModel):
    name: str
    is_private: bool
    workout_days: Optional[str]
    user_id: int

class WorkoutPlanCreate(WorkoutPlanBase):
    pass

class WorkoutPlan(WorkoutPlanBase):
    plan_id: int

    user: Optional['User']
    workouts: Optional[List['Workout']]

    class Config:
        from_attributes = True

class WorkoutBase(BaseModel):
    name: str
    date: str
    user_id: int
    plan_id: Optional[int]

class WorkoutCreate(WorkoutBase):
    pass

class Workout(WorkoutBase):
    workout_id: int

    user: Optional['User']
    workout_plan: Optional['WorkoutPlan']
    exercises: Optional[List['Exercise']]

    class Config:
        from_attributes = True

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

    workout: Optional['Workout']
    user_exercise: Optional['UserExercise']

    class Config:
        from_attributes = True