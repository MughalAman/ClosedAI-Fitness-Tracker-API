from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fitness_api.core import db_functions, schemas


router = APIRouter()


@router.post("/exercise/", response_model=schemas.Exercise)
def create_exercise(exercise: schemas.ExerciseCreate, db: Session = Depends(db_functions.get_database)):
    return db_functions.create_exercise(db, exercise)


@router.get("/exercise/{exercise_id}", response_model=schemas.Exercise)
def read_exercise(exercise_id: int, db: Session = Depends(db_functions.get_database)):
    db_exercise = db_functions.get_exercise(db, exercise_id)
    if db_exercise is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return db_exercise


@router.put("/exercise/{exercise_id}", response_model=schemas.Exercise)
def update_exercise(exercise_id: int, exercise: schemas.ExerciseCreate, 
                    db: Session = Depends(db_functions.get_database)):
    return db_functions.update_exercise(db, exercise_id, exercise)


@router.delete("/exercise/{exercise_id}", response_model=schemas.Exercise)
def delete_exercise(exercise_id: int, db: Session = Depends(db_functions.get_database)):
    return db_functions.delete_exercise(db, exercise_id)
