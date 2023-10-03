from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fitness_api.core import db_functions, schemas


router = APIRouter()


@router.post("/workout_plan/", response_model=schemas.WorkoutPlan)
def create_workout_plan(workout_plan: schemas.WorkoutPlanCreate, db: Session = Depends(db_functions.get_database)):
    return db_functions.create_workout_plan(db, workout_plan)


@router.get("/workout_plan/{plan_id}", response_model=schemas.WorkoutPlan)
def read_workout_plan(plan_id: int, db: Session = Depends(db_functions.get_database)):
    db_workout_plan = db_functions.get_workout_plan(db, plan_id)
    if db_workout_plan is None:
        raise HTTPException(status_code=404, detail="WorkoutPlan not found")
    return db_workout_plan


@router.put("/workout_plan/{plan_id}", response_model=schemas.WorkoutPlan)
def update_workout_plan(plan_id: int, workout_plan: schemas.WorkoutPlanCreate, 
                        db: Session = Depends(db_functions.get_database)):
    return db_functions.update_workout_plan(db, plan_id, workout_plan)


@router.delete("/workout_plan/{plan_id}", response_model=schemas.WorkoutPlan)
def delete_workout_plan(plan_id: int, db: Session = Depends(db_functions.get_database)):
    return db_functions.delete_workout_plan(db, plan_id)
