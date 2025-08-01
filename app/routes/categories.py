from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
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

# Get Category by ID
@router.get("/{category_id}")
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return {"id": category.id, "name": category.name, "description": category.description}

# Update Category
@router.put("/{category_id}")
def update_category(
    category_id: int, 
    name: Optional[str] = None, 
    description: Optional[str] = None, 
    db: Session = Depends(get_db)
):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    if name is not None:
        # Check if new name conflicts with existing category
        existing = db.query(models.Category).filter(models.Category.name == name, models.Category.id != category_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Category with this name already exists")
        category.name = name
    
    if description is not None:
        category.description = description
    
    db.commit()
    db.refresh(category)
    return {"id": category.id, "name": category.name, "description": category.description}

# Delete Category
@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has items
    items_count = db.query(models.Item).filter(models.Item.category_id == category_id).count()
    if items_count > 0:
        raise HTTPException(
            status_code=400, 
            detail=f"Cannot delete category. It has {items_count} item(s). Remove all items first."
        )
    
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}

# List All Categories
@router.get("/")
def list_categories(db: Session = Depends(get_db)):
    categories = db.query(models.Category).all()
    return categories