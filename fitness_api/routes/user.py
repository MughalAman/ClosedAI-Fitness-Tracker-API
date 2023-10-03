from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from fitness_api.core import db_functions, schemas
from fitness_api.settings import SETTINGS

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def get_current_user(db: Annotated[Session, Depends(db_functions.get_database)], 
                           token: Annotated[str, Depends(oauth2_scheme)]):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SETTINGS.secret_key, algorithms=[SETTINGS.algorithm])
        user_email: str = payload.get("sub")
        if user_email is None:
            raise credentials_exception
        token_data = schemas.TokenData(user_email=user_email)
    except JWTError:
        raise credentials_exception
    user = db_functions.get_user(db, user_email=token_data.user_email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[schemas.User, Depends(get_current_user)]
):
    if current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user


@router.post("/user/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(db_functions.get_database)):
    db_user = db_functions.get_user(db, user_email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return db_functions.create_user(db=db, user_data=user)


@router.get("/user/me", response_model=schemas.User)
def read_user(current_user: schemas.User = Depends(get_current_active_user), 
              db: Session = Depends(db_functions.get_database)):
    db_user = db_functions.get_user(db, user_id=current_user.id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.put("/user/{user_id}", response_model=schemas.User)
def update_user(user: schemas.UserCreate, 
                current_user: schemas.User = Depends(get_current_active_user), 
                db: Session = Depends(db_functions.get_database)):
    
    db_user = db_functions.update_user(db, current_user.user_id, user)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.delete("/user/{user_id}", response_model=schemas.User)
def delete_user(current_user: schemas.User = Depends(get_current_active_user),
                db: Session = Depends(db_functions.get_database)):
    db_user = db_functions.delete_user(db, current_user.user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

