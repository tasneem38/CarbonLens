from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.schemas import UserCreate, UserOut
from backend.db.session import get_db
from backend.db import models

router = APIRouter(tags=["users"])

@router.post("/users", response_model=UserOut)
def create_user(payload: UserCreate, db: Session = Depends(get_db)):
    user = models.User(email=payload.email, name=payload.name)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
