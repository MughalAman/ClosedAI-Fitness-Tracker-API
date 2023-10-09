from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fitness_api.core import db_functions, schemas


router = APIRouter()


@router.post("/rating/", response_model=schemas.Rating)
def create_rating(
    rating: schemas.RatingCreate, db: Session = Depends(db_functions.get_database)
):
    return db_functions.create_rating(db, rating)


@router.get("/rating/{rating_id}", response_model=schemas.Rating)
def read_rating(rating_id: int, db: Session = Depends(db_functions.get_database)):
    db_rating = db_functions.get_rating(db, rating_id)
    if db_rating is None:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating


@router.put("/rating/{rating_id}", response_model=schemas.Rating)
def update_rating(
    rating_id: int,
    rating: schemas.RatingCreate,
    db: Session = Depends(db_functions.get_database),
):
    return db_functions.update_rating(db, rating_id, rating)


@router.delete("/rating/{rating_id}", response_model=schemas.Rating)
def delete_rating(rating_id: int, db: Session = Depends(db_functions.get_database)):
    return db_functions.delete_rating(db, rating_id)
