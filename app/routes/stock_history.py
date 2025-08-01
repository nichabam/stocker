from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from .. import models
from ..database import SessionLocal

router = APIRouter(prefix="/stock", tags=["Stock"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST - Log Stock Count
@router.post("/")
def log_stock(
    item_id: int,
    quantity: float,
    notes: Optional[str] = None,
    staff_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Check if item exists
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Create stock history entry
    stock_entry = models.StockHistory(
        item_id=item_id,
        quantity=quantity,
        notes=notes,
        staff_name=staff_name
    )
    db.add(stock_entry)
    
    # Update current stock in items table
    item.quantity = quantity
    
    db.commit()
    db.refresh(stock_entry)
    
    return {
        "id": stock_entry.id,
        "item_id": stock_entry.item_id,
        "item_name": item.name,
        "quantity": stock_entry.quantity,
        "date": stock_entry.date,
        "notes": stock_entry.notes,
        "staff_name": stock_entry.staff_name
    }

# PUT - Edit Stock Log
@router.put("/{stock_id}")
def edit_stock_log(
    stock_id: int,
    quantity: Optional[float] = None,
    notes: Optional[str] = None,
    staff_name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    stock_entry = db.query(models.StockHistory).filter(models.StockHistory.id == stock_id).first()
    if not stock_entry:
        raise HTTPException(status_code=404, detail="Stock log not found")
    
    if quantity is not None:
        stock_entry.quantity = quantity
        # Update current stock in items table
        item = db.query(models.Item).filter(models.Item.id == stock_entry.item_id).first()
        if item:
            item.quantity = quantity
    
    if notes is not None:
        stock_entry.notes = notes
    
    if staff_name is not None:
        stock_entry.staff_name = staff_name
    
    db.commit()
    db.refresh(stock_entry)
    
    return {
        "id": stock_entry.id,
        "item_id": stock_entry.item_id,
        "quantity": stock_entry.quantity,
        "date": stock_entry.date,
        "notes": stock_entry.notes,
        "staff_name": stock_entry.staff_name
    }

# DELETE - Delete Stock Log
@router.delete("/{stock_id}")
def delete_stock_log(stock_id: int, db: Session = Depends(get_db)):
    stock_entry = db.query(models.StockHistory).filter(models.StockHistory.id == stock_id).first()
    if not stock_entry:
        raise HTTPException(status_code=404, detail="Stock log not found")
    
    db.delete(stock_entry)
    db.commit()
    
    return {"message": "Stock log deleted successfully"}

# GET - Get All Stock History
@router.get("/")
def get_all_stock_history(db: Session = Depends(get_db)):
    stock_entries = db.query(models.StockHistory).order_by(models.StockHistory.date.desc()).all()
    
    return [
        {
            "id": entry.id,
            "item_id": entry.item_id,
            "item_name": entry.item.name if entry.item else None,
            "quantity": entry.quantity,
            "date": entry.date,
            "notes": entry.notes,
            "staff_name": entry.staff_name
        }
        for entry in stock_entries
    ]

# GET - Get Stock History for Specific Item
@router.get("/item/{item_id}")
def get_stock_history_for_item(item_id: int, db: Session = Depends(get_db)):
    # Check if item exists
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    stock_entries = db.query(models.StockHistory).filter(
        models.StockHistory.item_id == item_id
    ).order_by(models.StockHistory.date.desc()).all()
    
    return [
        {
            "id": entry.id,
            "item_id": entry.item_id,
            "item_name": item.name,
            "quantity": entry.quantity,
            "date": entry.date,
            "notes": entry.notes,
            "staff_name": entry.staff_name
        }
        for entry in stock_entries
    ] 