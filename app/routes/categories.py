from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from .. import models
from ..database import SessionLocal

router = APIRouter(prefix="/categories", tags=["Categories"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Category
@router.post("/")
def create_category(name: str, db: Session = Depends(get_db)):
    existing = db.query(models.Category).filter(models.Category.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Category already exists")
    new_category = models.Category(name=name)
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return {"id": new_category.id, "name": new_category.name}

# List All Categories
@router.get("/")
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories