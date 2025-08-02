from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Optional
from .. import models
from ..database import SessionLocal
from ..ml_analytics import InventoryAnalytics
from datetime import datetime, timedelta

router = APIRouter(prefix="/analytics", tags=["Analytics"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/predictions/{item_id}")
def get_item_predictions(item_id: int, db: Session = Depends(get_db)):
    """Get ML predictions for a specific item"""
    analytics = InventoryAnalytics(db)
    
    try:
        predictions = analytics.run_full_analytics(item_id)
        return predictions
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics error: {str(e)}")

@router.get("/restock-predictions")
def get_all_restock_predictions(db: Session = Depends(get_db)):
    """Get restock predictions for all items"""
    analytics = InventoryAnalytics(db)
    
    items = db.query(models.Item).filter(models.Item.is_active == True).all()
    predictions = []
    
    for item in items:
        try:
            restock_date, confidence = analytics.predict_restock_date(item.id)
            stock_life = analytics.predict_stock_life(item.id)
            optimal_quantity = analytics.predict_optimal_restock_quantity(item.id)
            
            predictions.append({
                "item_id": item.id,
                "item_name": item.name,
                "current_stock": item.quantity,
                "restock_threshold": item.restock_threshold,
                "predicted_restock_date": restock_date,
                "confidence": confidence,
                "stock_life_days": stock_life,
                "optimal_restock_quantity": optimal_quantity,
                "daily_consumption": analytics.calculate_daily_consumption(item.id)
            })
        except Exception as e:
            continue  # Skip items with errors
    
    return predictions

@router.get("/cost-optimization")
def get_cost_optimization_analysis(db: Session = Depends(get_db)):
    """Get cost optimization analysis for all items"""
    analytics = InventoryAnalytics(db)
    
    items = db.query(models.Item).filter(models.Item.is_active == True).all()
    cost_analysis = []
    
    for item in items:
        try:
            cost_data = analytics.calculate_cost_optimization(item.id)
            if cost_data:  # Only include items with cost data
                cost_analysis.append({
                    "item_id": item.id,
                    "item_name": item.name,
                    "cost_per_unit": item.cost_per_unit,
                    **cost_data
                })
        except Exception as e:
            continue
    
    return cost_analysis

@router.get("/sales-performance")
def get_sales_performance_analysis(db: Session = Depends(get_db)):
    """Get sales performance analysis for all items"""
    analytics = InventoryAnalytics(db)
    
    items = db.query(models.Item).filter(models.Item.is_active == True).all()
    performance_data = []
    
    for item in items:
        try:
            sales_data = analytics.analyze_sales_performance(item.id)
            performance_data.append({
                "item_id": item.id,
                "item_name": item.name,
                "category": item.category.name if item.category else None,
                **sales_data
            })
        except Exception as e:
            continue
    
    return performance_data

@router.get("/menu-recommendations")
def get_menu_optimization_recommendations(db: Session = Depends(get_db)):
    """Get menu optimization recommendations"""
    analytics = InventoryAnalytics(db)
    
    items = db.query(models.Item).filter(models.Item.is_active == True).all()
    recommendations = []
    
    for item in items:
        try:
            menu_data = analytics.generate_menu_recommendations(item.id)
            recommendations.append({
                "item_id": item.id,
                "item_name": item.name,
                "category": item.category.name if item.category else None,
                "is_active": item.is_active,
                **menu_data
            })
        except Exception as e:
            continue
    
    return recommendations

@router.post("/sales-log")
def log_sale(
    item_id: int,
    quantity_sold: float,
    revenue: Optional[float] = None,
    notes: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Log a sale for analytics"""
    # Check if item exists
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    # Create sales history entry
    sale_entry = models.SalesHistory(
        item_id=item_id,
        quantity_sold=quantity_sold,
        revenue=revenue,
        notes=notes
    )
    db.add(sale_entry)
    
    # Update item's last sale date
    item.last_sale_date = sale_entry.date
    
    db.commit()
    db.refresh(sale_entry)
    
    return {
        "id": sale_entry.id,
        "item_id": sale_entry.item_id,
        "item_name": item.name,
        "quantity_sold": sale_entry.quantity_sold,
        "revenue": sale_entry.revenue,
        "date": sale_entry.date,
        "notes": sale_entry.notes
    }

@router.get("/dashboard-summary")
def get_analytics_dashboard_summary(db: Session = Depends(get_db)):
    """Get summary analytics for dashboard"""
    analytics = InventoryAnalytics(db)
    
    items = db.query(models.Item).filter(models.Item.is_active == True).all()
    
    # Calculate summary statistics
    total_items = len(items)
    low_stock_items = 0
    items_needing_restock = 0
    total_daily_cost = 0
    high_performance_items = 0
    items_to_remove = 0
    
    for item in items:
        try:
            # Check low stock
            if item.quantity <= item.restock_threshold:
                low_stock_items += 1
            
            # Check restock predictions
            restock_date, _ = analytics.predict_restock_date(item.id)
            if restock_date and restock_date <= (datetime.now() + timedelta(days=7)):
                items_needing_restock += 1
            
            # Calculate costs
            cost_data = analytics.calculate_cost_optimization(item.id)
            if cost_data and cost_data.get("daily_cost"):
                total_daily_cost += cost_data["daily_cost"]
            
            # Check performance
            sales_data = analytics.analyze_sales_performance(item.id)
            if sales_data["sales_velocity"] > 5:  # High performing
                high_performance_items += 1
            
            # Check menu recommendations
            menu_data = analytics.generate_menu_recommendations(item.id)
            if menu_data["recommendation"] == "remove":
                items_to_remove += 1
                
        except Exception as e:
            continue
    
    return {
        "total_items": total_items,
        "low_stock_items": low_stock_items,
        "items_needing_restock": items_needing_restock,
        "total_daily_cost": round(total_daily_cost, 2),
        "high_performance_items": high_performance_items,
        "items_to_remove": items_to_remove,
        "analytics_updated": datetime.now().isoformat()
    }

@router.post("/update-analytics")
def update_all_analytics(db: Session = Depends(get_db)):
    """Update analytics for all items (background job)"""
    analytics = InventoryAnalytics(db)
    
    try:
        analytics.update_analytics_for_all_items()
        return {"message": "Analytics updated successfully", "timestamp": datetime.now().isoformat()}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to update analytics: {str(e)}")

@router.get("/item/{item_id}/analytics")
def get_item_analytics_history(item_id: int, db: Session = Depends(get_db)):
    """Get historical analytics for an item"""
    # Get latest analytics record
    latest_analytics = db.query(models.ItemAnalytics).filter(
        models.ItemAnalytics.item_id == item_id
    ).order_by(models.ItemAnalytics.date.desc()).first()
    
    # Get latest menu optimization
    latest_menu = db.query(models.MenuOptimization).filter(
        models.MenuOptimization.item_id == item_id
    ).order_by(models.MenuOptimization.date.desc()).first()
    
    if not latest_analytics:
        raise HTTPException(status_code=404, detail="No analytics found for this item")
    
    return {
        "item_id": item_id,
        "analytics": {
            "predicted_restock_date": latest_analytics.predicted_restock_date,
            "predicted_stock_life_days": latest_analytics.predicted_stock_life_days,
            "predicted_restock_quantity": latest_analytics.predicted_restock_quantity,
            "confidence_score": latest_analytics.confidence_score,
            "avg_daily_consumption": latest_analytics.avg_daily_consumption,
            "sales_velocity": latest_analytics.sales_velocity,
            "model_version": latest_analytics.model_version,
            "last_training_date": latest_analytics.last_training_date
        },
        "menu_optimization": {
            "recommendation": latest_menu.recommendation if latest_menu else None,
            "confidence": latest_menu.confidence if latest_menu else None,
            "reasoning": latest_menu.reasoning if latest_menu else None,
            "days_since_last_sale": latest_menu.days_since_last_sale if latest_menu else None
        } if latest_menu else None
    } 