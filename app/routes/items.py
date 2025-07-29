from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import models
from ..database import SessionLocal

router = APIRouter(prefix="/items", tags=["Items"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create Item
@router.post("/")
def create_item(
    name: str,
    unit: str,
    restock_threshold: float,
    category_id: int,
    db: Session = Depends(get_db)
):
    # Check if category exists
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if item with same name already exists
    existing = db.query(models.Item).filter(models.Item.name == name).first()
    if existing:
        raise HTTPException(status_code=400, detail="Item with this name already exists")
    
    new_item = models.Item(
        name=name,
        quantity=0,  # Default to 0
        unit=unit,
        restock_threshold=restock_threshold,
        category_id=category_id
    )
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return {"id": new_item.id, "name": new_item.name, "quantity": new_item.quantity, "unit": new_item.unit, "restock_threshold": new_item.restock_threshold, "category_id": new_item.category_id}

# Update Item Details
@router.put("/{item_id}")
def update_item(
    item_id: int,
    name: Optional[str] = None,
    unit: Optional[str] = None,
    restock_threshold: Optional[float] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_db)
):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    if name is not None:
        # Check if new name conflicts with existing item
        existing = db.query(models.Item).filter(models.Item.name == name, models.Item.id != item_id).first()
        if existing:
            raise HTTPException(status_code=400, detail="Item with this name already exists")
        item.name = name
    
    if unit is not None:
        item.unit = unit
    if restock_threshold is not None:
        item.restock_threshold = restock_threshold
    if category_id is not None:
        # Check if category exists
        category = db.query(models.Category).filter(models.Category.id == category_id).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
        item.category_id = category_id
    
    db.commit()
    db.refresh(item)
    return {"id": item.id, "name": item.name, "quantity": item.quantity, "unit": item.unit, "restock_threshold": item.restock_threshold, "category_id": item.category_id}

# Delete Item
@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

# Get Specific Item Details
@router.get("/{item_id}")
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    return {
        "id": item.id,
        "name": item.name,
        "quantity": item.quantity,
        "unit": item.unit,
        "restock_threshold": item.restock_threshold,
        "category_id": item.category_id,
        "category_name": item.category.name if item.category else None
    }

# Get All Items
@router.get("/")
def get_all_items(db: Session = Depends(get_db)):
    items = db.query(models.Item).all()
    return [
        {
            "id": item.id,
            "name": item.name,
            "quantity": item.quantity,
            "unit": item.unit,
            "restock_threshold": item.restock_threshold,
            "category_id": item.category_id,
            "category_name": item.category.name if item.category else None
        }
        for item in items
    ]

# Get All Items Within a Category
@router.get("/category/{category_id}")
def get_items_by_category(category_id: int, db: Session = Depends(get_db)):
    # Check if category exists
    category = db.query(models.Category).filter(models.Category.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    items = db.query(models.Item).filter(models.Item.category_id == category_id).all()
    return [
        {
            "id": item.id,
            "name": item.name,
            "quantity": item.quantity,
            "unit": item.unit,
            "restock_threshold": item.restock_threshold,
            "category_id": item.category_id,
            "category_name": category.name
        }
        for item in items
    ]
