from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from fitness_api.core import db_functions
from fitness_api.core.schemas import FriendshipCreate, FriendshipInDB, FriendshipStatusCreate, FriendshipStatusInDB


router = APIRouter()


# FriendshipStatus routes

@router.post("/status/", response_model=FriendshipStatusInDB)
def create_status(status: FriendshipStatusCreate, db: Session = Depends(db_functions.get_database)):
    return db_functions.create_friendship_status(db, status)

@router.get("/status/{status_id}", response_model=FriendshipStatusInDB)
def read_status(status_id: int, db: Session = Depends(db_functions.get_database)):
    status = db_functions.get_friendship_status(db, status_id)
    if status is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Status not found")
    return status

@router.get("/statuses/", response_model=List[FriendshipStatusInDB])
def read_all_statuses(db: Session = Depends(db_functions.get_database)):
    return db_functions.get_all_friendship_statuses(db)

@router.put("/status/{status_id}/", response_model=FriendshipStatusInDB)
def update_status(status_id: int, status: FriendshipStatusCreate, db: Session = Depends(db_functions.get_database)):
    db_status = db_functions.update_friendship_status(db, status_id, status)
    if not db_status:
        raise HTTPException(status_code=404, detail="Status not found")
    return db_status

@router.delete("/status/{status_id}")
def delete_status(status_id: int, db: Session = Depends(db_functions.get_database)):
    db_functions.delete_friendship_status(db, status_id)
    return {"status": "deleted"}


# Friendship routes

@router.post("/friendship/", response_model=FriendshipInDB)
def create_friendship(friendship: FriendshipCreate, db: Session = Depends(db_functions.get_database)):
    return db_functions.create_friendship(db, friendship)

@router.get("/friendship/{friendship_id}", response_model=FriendshipInDB)
def read_friendship(friendship_id: int, db: Session = Depends(db_functions.get_database)):
    friendship = db_functions.get_friendship(db, friendship_id)
    if friendship is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Friendship not found")
    return friendship

@router.put("/friendship/{friendship_id}/", response_model=FriendshipInDB)
def update_friendship_status(friendship_id: int, status_id: int, db: Session = Depends(db_functions.get_database)):
    db_friendship = db_functions.update_friendships_status(db, friendship_id, status_id)
    if not db_friendship:
        raise HTTPException(status_code=404, detail="Friendship not found")
    return db_friendship

@router.get("/friendships/", response_model=List[FriendshipInDB])
def read_all_friendships(db: Session = Depends(db_functions.get_database)):
    return db_functions.get_all_friendships(db)

@router.get("/friendships/user/{user_id}", response_model=List[FriendshipInDB])
def read_all_friendships_for_user(user_id: int, db: Session = Depends(db_functions.get_database)):
    return db_functions.get_all_friendships_for_user(db, user_id)

@router.delete("/friendship/{friendship_id}")
def delete_friendship(friendship_id: int, db: Session = Depends(db_functions.get_database)):
    db_functions.delete_friendship(db, friendship_id)
    return {"status": "deleted"}