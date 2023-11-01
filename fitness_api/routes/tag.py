from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fitness_api.core import db_functions, schemas

router = APIRouter()

@router.post("/tag/", response_model=schemas.TagRead)
def create_tag(tag: schemas.TagCreate, db: Session = Depends(db_functions.get_database)):
    return db_functions.create_tag(db, tag)

@router.get("/tags/", response_model=List[schemas.TagRead])
def read_tags(skip: int = 0, limit: int = 100, db: Session = Depends(db_functions.get_database)):
    tags = db_functions.get_tags(db, skip=skip, limit=limit)
    return tags

@router.get("/tag/{tag_id}/", response_model=schemas.TagRead)
def read_tag(tag_id: int, db: Session = Depends(db_functions.get_database)):
    db_tag = db_functions.get_tag(db, tag_id=tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@router.put("/tag/{tag_id}/", response_model=schemas.TagRead)
def update_tag(tag_id: int, tag: schemas.TagUpdate, db: Session = Depends(db_functions.get_database)):
    db_tag = db_functions.update_tag(db, tag_id, tag)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag

@router.delete("/tag/{tag_id}/", response_model=schemas.TagRead)
def delete_tag(tag_id: int, db: Session = Depends(db_functions.get_database)):
    db_tag = db_functions.delete_tag(db, tag_id)
    if db_tag is None:
        raise HTTPException(status_code=404, detail="Tag not found")
    return db_tag
