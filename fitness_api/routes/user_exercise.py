from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fitness_api.core import db_functions, schemas


router = APIRouter()

@router.post("/user_exercise/", response_model=schemas.UserExercise)
def create_user_exercise(user_exercise: schemas.UserExerciseCreate, db: Session = Depends(db_functions.get_database)):
    return db_functions.create_user_exercise(db, user_exercise)


@router.get("/user_exercise/{user_exercise_id}", response_model=schemas.UserExercise)
def read_user_exercise(user_exercise_id: int, db: Session = Depends(db_functions.get_database)):
    db_user_exercise = db_functions.get_user_exercise(db, user_exercise_id)
    if db_user_exercise is None:
        raise HTTPException(status_code=404, detail="UserExercise not found")
    return db_user_exercise


@router.put("/user_exercise/{user_exercise_id}", response_model=schemas.UserExercise)
def update_user_exercise(user_exercise_id: int, 
                         user_exercise: schemas.UserExerciseCreate, 
                         db: Session = Depends(db_functions.get_database)):
    return db_functions.update_user_exercise(db, user_exercise_id, user_exercise)


@router.delete("/user_exercise/{user_exercise_id}", response_model=schemas.UserExercise)
def delete_user_exercise(user_exercise_id: int, 
                         db: Session = Depends(db_functions.get_database)):
    return db_functions.delete_user_exercise(db, user_exercise_id)
