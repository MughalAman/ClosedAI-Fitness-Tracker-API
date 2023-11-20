from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from fitness_api.core import db_functions, schemas


router = APIRouter()


@router.post("/lang/", response_model=schemas.LangRead)
def create_exercise(lang: schemas.LangCreate, db: Session = Depends(db_functions.get_database)):
    return db_functions.create_exercise(db, lang)


@router.get("/lang/{lang_id}", response_model=schemas.LangRead)
def read_lang(lang_id: int, db: Session = Depends(db_functions.get_database)):
    db_lang = db_functions.get_exercise(db, lang_id)
    if db_lang is None:
        raise HTTPException(status_code=404, detail="Exercise not found")
    return db_lang


@router.put("/lang/{lang_id}", response_model=schemas.LangRead)
def update_lang(lang_id: int, lang: schemas.LangUpdate, 
                    db: Session = Depends(db_functions.get_database)):
    return db_functions.update_lang(db, lang_id, lang)


@router.delete("/lang/{lang_id}", response_model=schemas.LangRead)
def delete_lang(lang_id: int, db: Session = Depends(db_functions.get_database)):
    return db_functions.delete_lang(db, lang_id)
