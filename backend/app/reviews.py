from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from . import crud,models, schemas
#from .database import get_db # Assume get_db dep
from .database import SessionLocal,get_db, engine, Base
router = APIRouter()

#@router.post("/reviews", response_model=schemas.Review)
#def create_review(review: schemas.ReviewCreate, db: Session):
#    return crud.create_review(db, review)