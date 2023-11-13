from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fitness_api.core import db_functions, schemas


router = APIRouter()


@router.post("/workout/", response_model=schemas.Workout)
def create_workout(workout: schemas.WorkoutCreate, db: Session = Depends(db_functions.get_database)):
    return db_functions.create_workout(db, workout)


@router.get("/workout/{workout_id}", response_model=schemas.Workout)
def read_workout(workout_id: int, db: Session = Depends(db_functions.get_database)):
    db_workout = db_functions.get_workout(db, workout_id)
    if db_workout is None:
        raise HTTPException(status_code=404, detail="Workout not found")
    return db_workout


@router.put("/workout/{workout_id}", response_model=schemas.Workout)
def update_workout(workout_id: int, workout: schemas.WorkoutUpdate, db: Session = Depends(db_functions.get_database)):
    return db_functions.update_workout(db, workout_id, workout)


@router.delete("/workout/{workout_id}", response_model=schemas.Workout)
def delete_workout(workout_id: int, db: Session = Depends(db_functions.get_database)):
    return db_functions.delete_workout(db, workout_id)


@router.post("/workout/date/", response_model=schemas.WorkoutDate)
def create_workout_date(workout_date: schemas.WorkoutDateCreate, db: Session = Depends(db_functions.get_database)):
    return db_functions.create_workout_date(db, workout_date)


@router.delete("/workout/date/{workout_date_id}")
def delete_workout_date(workout_date_id: int, db: Session = Depends(db_functions.get_database)):
    return db_functions.delete_workout_date(db, workout_date_id)