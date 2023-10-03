from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fitness_api.core import db_functions, schemas


router = APIRouter()


@router.post("/friendship/", response_model=schemas.Friendship)
def create_friendship(friendship: schemas.FriendshipCreate, db: Session = Depends(db_functions.get_database)):
    return db_functions.create_friendship(db, friendship)

@router.get("/friendship/{user1_id}/{user2_id}", response_model=schemas.Friendship)
def read_friendship(user1_id: int, user2_id: int, db: Session = Depends(db_functions.get_database)):
    db_friendship = db_functions.get_friendship(db, user1_id, user2_id)
    if db_friendship is None:
        raise HTTPException(status_code=404, detail="Friendship not found")
    return db_friendship

@router.put("/friendship/{user1_id}/{user2_id}", response_model=schemas.Friendship)
def update_friendship(user1_id: int, 
                      user2_id: int, 
                      friendship: schemas.FriendshipCreate, 
                      db: Session = Depends(db_functions.get_database)):
    
    return db_functions.update_friendship(db, user1_id, user2_id, friendship)

@router.delete("/friendship/{user1_id}/{user2_id}", response_model=schemas.Friendship)
def delete_friendship(user1_id: int, user2_id: int, db: Session = Depends(db_functions.get_database)):
    return db_functions.delete_friendship(db, user1_id, user2_id)
