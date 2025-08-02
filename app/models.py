from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone
from .database import Base

class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    quantity = Column(Float, default=0)
    unit = Column(String)
    restock_threshold = Column(Float, default=0)
    category_id = Column(Integer, ForeignKey("categories.id"))
    is_active = Column(Boolean, default=True)  # For menu optimization
    cost_per_unit = Column(Float, nullable=True)  # For cost analysis
    last_sale_date = Column(DateTime, nullable=True)  # For performance tracking
    
    category = relationship("Category", back_populates="items")
    stock_history = relationship("StockHistory", back_populates="item")
    restock_history = relationship("RestockHistory", back_populates="item")
    sales_history = relationship("SalesHistory", back_populates="item")
    analytics = relationship("ItemAnalytics", back_populates="item")
    menu_optimization = relationship("MenuOptimization", back_populates="item")

class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, index=True)
    items = relationship("Item", back_populates="category")

class StockHistory(Base):
    __tablename__ = "stock_history"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity = Column(Float, nullable=False)  # Current stock level
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    notes = Column(String, nullable=True)  # "Weekly count", "Restock", etc.
    staff_name = Column(String, nullable=True)  # Staff member who logged the count
    
    item = relationship("Item", back_populates="stock_history")

class RestockHistory(Base):
    __tablename__ = "restock_history"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    restock_amount = Column(Float, nullable=False)  # How much was added
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    supplier = Column(String, nullable=True)  # Optional supplier info
    notes = Column(String, nullable=True)  # Optional notes
    cost_per_unit = Column(Float, nullable=True)  # Cost per unit for analytics
    
    item = relationship("Item", back_populates="restock_history")

class SalesHistory(Base):
    __tablename__ = "sales_history"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    quantity_sold = Column(Float, nullable=False)  # How much was sold
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    revenue = Column(Float, nullable=True)  # Revenue from this sale
    notes = Column(String, nullable=True)  # Optional notes
    
    item = relationship("Item", back_populates="sales_history")

class ItemAnalytics(Base):
    __tablename__ = "item_analytics"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # ML Predictions
    predicted_restock_date = Column(DateTime, nullable=True)
    predicted_stock_life_days = Column(Float, nullable=True)
    predicted_restock_quantity = Column(Float, nullable=True)
    confidence_score = Column(Float, nullable=True)
    
    # Analytics
    avg_daily_consumption = Column(Float, nullable=True)
    consumption_trend = Column(Float, nullable=True)  # Positive = increasing, negative = decreasing
    seasonality_factor = Column(Float, nullable=True)
    
    # Cost Analysis
    optimal_restock_frequency = Column(Float, nullable=True)  # Days between restocks
    cost_per_day = Column(Float, nullable=True)
    waste_percentage = Column(Float, nullable=True)
    
    # Performance Metrics
    sales_velocity = Column(Float, nullable=True)  # Units sold per day
    stockout_risk = Column(Float, nullable=True)  # 0-1 scale
    overstock_risk = Column(Float, nullable=True)  # 0-1 scale
    
    # ML Model Metadata
    model_version = Column(String, nullable=True)
    last_training_date = Column(DateTime, nullable=True)
    model_accuracy = Column(Float, nullable=True)
    
    item = relationship("Item", back_populates="analytics")

class MenuOptimization(Base):
    __tablename__ = "menu_optimization"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"))
    date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    # Performance Metrics
    days_since_last_sale = Column(Integer, nullable=True)
    total_sales_last_30_days = Column(Float, nullable=True)
    total_sales_last_90_days = Column(Float, nullable=True)
    revenue_last_30_days = Column(Float, nullable=True)
    revenue_last_90_days = Column(Float, nullable=True)
    
    # Recommendations
    recommendation = Column(String, nullable=True)  # "keep", "reduce", "remove", "increase"
    confidence = Column(Float, nullable=True)
    reasoning = Column(String, nullable=True)
    
    # Cost Impact
    potential_savings = Column(Float, nullable=True)
    potential_revenue_loss = Column(Float, nullable=True)
    
    item = relationship("Item", back_populates="menu_optimization")