from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Optional
from .. import models
from ..database import SessionLocal

router = APIRouter(prefix="/restocks", tags=["Restock"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# POST - Log Restock
@router.post("/")
def log_restock(
    item_id: int,
    restock_amount: float,
    supplier: Optional[str] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    # Check if item exists
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Create restock history entry
    restock_entry = models.RestockHistory(
        item_id=item_id,
        restock_amount=restock_amount,
        supplier=supplier,
        notes=notes
    )
    db.add(restock_entry)
    
    # Update current stock in items table
    item.quantity += restock_amount
    
    db.commit()
    db.refresh(restock_entry)
    
    return {
        "id": restock_entry.id,
        "item_id": restock_entry.item_id,
        "item_name": item.name,
        "restock_amount": restock_entry.restock_amount,
        "date": restock_entry.date,
        "supplier": restock_entry.supplier,
        "notes": restock_entry.notes
    }

# PUT - Edit Restock Log
@router.put("/{restock_id}")
def edit_restock_log(
    restock_id: int,
    restock_amount: Optional[float] = None,
    supplier: Optional[str] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    restock_entry = db.query(models.RestockHistory).filter(models.RestockHistory.id == restock_id).first()
    if not restock_entry:
        raise HTTPException(status_code=404, detail="Restock log not found")
    
    # Calculate the difference if restock_amount changes
    old_amount = restock_entry.restock_amount
    if restock_amount is not None and restock_amount != old_amount:
        restock_entry.restock_amount = restock_amount
        # Update current stock in items table
        item = db.query(models.Item).filter(models.Item.id == restock_entry.item_id).first()
        if item:
            # Remove old amount and add new amount
            item.quantity = item.quantity - old_amount + restock_amount
    
    if supplier is not None:
        restock_entry.supplier = supplier
    
    if notes is not None:
        restock_entry.notes = notes
    
    db.commit()
    db.refresh(restock_entry)
    
    return {
        "id": restock_entry.id,
        "item_id": restock_entry.item_id,
        "restock_amount": restock_entry.restock_amount,
        "date": restock_entry.date,
        "supplier": restock_entry.supplier,
        "notes": restock_entry.notes
    }

# DELETE - Delete Restock Log
@router.delete("/{restock_id}")
def delete_restock_log(restock_id: int, db: Session = Depends(get_db)):
    restock_entry = db.query(models.RestockHistory).filter(models.RestockHistory.id == restock_id).first()
    if not restock_entry:
        raise HTTPException(status_code=404, detail="Restock log not found")
    
    # Update current stock in items table (remove the restock amount)
    item = db.query(models.Item).filter(models.Item.id == restock_entry.item_id).first()
    if item:
        item.quantity -= restock_entry.restock_amount
    
    db.delete(restock_entry)
    db.commit()
    
    return {"message": "Restock log deleted successfully"}

# GET - Get All Restock History
@router.get("/")
def get_all_restock_history(db: Session = Depends(get_db)):
    restock_entries = db.query(models.RestockHistory).order_by(models.RestockHistory.date.desc()).all()
    
    return [
        {
            "id": entry.id,
            "item_id": entry.item_id,
            "item_name": entry.item.name if entry.item else None,
            "restock_amount": entry.restock_amount,
            "date": entry.date,
            "supplier": entry.supplier,
            "notes": entry.notes
        }
        for entry in restock_entries
    ]

# GET - Get Restock History for Specific Item
@router.get("/item/{item_id}")
def get_restock_history_for_item(item_id: int, db: Session = Depends(get_db)):
    # Check if item exists
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    restock_entries = db.query(models.RestockHistory).filter(
        models.RestockHistory.item_id == item_id
    ).order_by(models.RestockHistory.date.desc()).all()
    
    return [
        {
            "id": entry.id,
            "item_id": entry.item_id,
            "item_name": item.name,
            "restock_amount": entry.restock_amount,
            "date": entry.date,
            "supplier": entry.supplier,
            "notes": entry.notes
        }
        for entry in restock_entries
    ] 