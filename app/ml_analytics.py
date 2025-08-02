import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple
from sqlalchemy.orm import Session
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_absolute_error, r2_score
import warnings
warnings.filterwarnings('ignore')

class InventoryAnalytics:
    def __init__(self, db: Session):
        self.db = db
        self.scaler = StandardScaler()
        
    def calculate_daily_consumption(self, item_id: int, days: int = 30) -> float:
        """Calculate average daily consumption for an item"""
        from . import models
        
        # Get stock history for the last N days
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        stock_records = self.db.query(models.StockHistory).filter(
            models.StockHistory.item_id == item_id,
            models.StockHistory.date >= start_date
        ).order_by(models.StockHistory.date).all()
        
        if len(stock_records) < 2:
            return 0.0
            
        # Calculate consumption from stock changes
        total_consumption = 0
        for i in range(1, len(stock_records)):
            consumption = stock_records[i-1].quantity - stock_records[i].quantity
            if consumption > 0:  # Only count positive consumption
                total_consumption += consumption
                
        return total_consumption / days
    
    def predict_restock_date(self, item_id: int) -> Tuple[datetime, float]:
        """Predict when an item will need restocking"""
        from . import models
        
        item = self.db.query(models.Item).filter(models.Item.id == item_id).first()
        if not item:
            return None, 0.0
            
        daily_consumption = self.calculate_daily_consumption(item_id)
        if daily_consumption <= 0:
            return None, 0.0
            
        # Calculate days until restock threshold
        days_until_restock = (item.quantity - item.restock_threshold) / daily_consumption
        predicted_date = datetime.now() + timedelta(days=days_until_restock)
        
        # Calculate confidence based on data consistency
        confidence = min(0.95, max(0.1, self._calculate_prediction_confidence(item_id)))
        
        return predicted_date, confidence
    
    def predict_stock_life(self, item_id: int) -> float:
        """Predict how many days current stock will last"""
        from . import models
        
        item = self.db.query(models.Item).filter(models.Item.id == item_id).first()
        if not item:
            return 0.0
            
        daily_consumption = self.calculate_daily_consumption(item_id)
        if daily_consumption <= 0:
            return 999.0  # Large number instead of infinity
            
        return item.quantity / daily_consumption
    
    def predict_optimal_restock_quantity(self, item_id: int) -> float:
        """Predict optimal restock quantity to minimize waste and stockouts"""
        from . import models
        
        item = self.db.query(models.Item).filter(models.Item.id == item_id).first()
        if not item:
            return 0.0
            
        daily_consumption = self.calculate_daily_consumption(item_id)
        if daily_consumption <= 0:
            return item.restock_threshold
            
        # Calculate optimal quantity based on consumption patterns
        # Aim for 2-3 weeks of stock
        optimal_days = 21  # 3 weeks
        optimal_quantity = daily_consumption * optimal_days
        
        # Ensure it's at least the restock threshold
        return max(optimal_quantity, item.restock_threshold)
    
    def calculate_cost_optimization(self, item_id: int) -> Dict:
        """Calculate cost optimization metrics"""
        from . import models
        
        item = self.db.query(models.Item).filter(models.Item.id == item_id).first()
        if not item or not item.cost_per_unit:
            return {}
            
        daily_consumption = self.calculate_daily_consumption(item_id)
        current_stock_life = self.predict_stock_life(item_id)
        
        # Calculate costs
        current_daily_cost = daily_consumption * item.cost_per_unit
        optimal_restock_quantity = self.predict_optimal_restock_quantity(item_id)
        optimal_restock_cost = optimal_restock_quantity * item.cost_per_unit
        
        # Calculate waste percentage (if overstocked)
        waste_percentage = 0
        if current_stock_life > 30:  # If stock lasts more than 30 days
            waste_percentage = min(0.3, (current_stock_life - 30) / current_stock_life)
            
        return {
            "daily_cost": current_daily_cost,
            "optimal_restock_quantity": optimal_restock_quantity,
            "optimal_restock_cost": optimal_restock_cost,
            "waste_percentage": waste_percentage,
            "optimal_restock_frequency": 21  # 3 weeks
        }
    
    def analyze_sales_performance(self, item_id: int) -> Dict:
        """Analyze sales performance and trends"""
        from . import models
        
        # Get sales data
        sales_records = self.db.query(models.SalesHistory).filter(
            models.SalesHistory.item_id == item_id
        ).order_by(models.SalesHistory.date.desc()).all()
        
        if not sales_records:
            return {"sales_velocity": 0, "trend": "no_data"}
            
        # Calculate sales velocity (units per day)
        total_sales = sum(record.quantity_sold for record in sales_records)
        days_since_first_sale = (datetime.now() - sales_records[-1].date).days
        sales_velocity = total_sales / max(days_since_first_sale, 1)
        
        # Calculate trend (last 30 days vs previous 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        sixty_days_ago = datetime.now() - timedelta(days=60)
        
        recent_sales = sum(r.quantity_sold for r in sales_records 
                          if r.date >= thirty_days_ago)
        previous_sales = sum(r.quantity_sold for r in sales_records 
                           if r.date >= sixty_days_ago and r.date < thirty_days_ago)
        
        trend = "increasing" if recent_sales > previous_sales else "decreasing"
        
        return {
            "sales_velocity": sales_velocity,
            "trend": trend,
            "total_sales": total_sales,
            "recent_sales": recent_sales,
            "previous_sales": previous_sales
        }
    
    def generate_menu_recommendations(self, item_id: int) -> Dict:
        """Generate menu optimization recommendations"""
        from . import models
        
        item = self.db.query(models.Item).filter(models.Item.id == item_id).first()
        if not item:
            return {}
            
        # Get sales performance
        sales_data = self.analyze_sales_performance(item_id)
        
        # Get days since last sale
        last_sale = self.db.query(models.SalesHistory).filter(
            models.SalesHistory.item_id == item_id
        ).order_by(models.SalesHistory.date.desc()).first()
        
        days_since_last_sale = (datetime.now() - last_sale.date).days if last_sale else 999
        
        # Generate recommendation
        recommendation = "keep"
        confidence = 0.5
        reasoning = ""
        
        if days_since_last_sale > 90:  # No sales for 3 months
            recommendation = "remove"
            confidence = 0.9
            reasoning = "No sales for over 3 months"
        elif days_since_last_sale > 30:  # No sales for 1 month
            recommendation = "reduce"
            confidence = 0.7
            reasoning = "Low sales activity"
        elif sales_data["trend"] == "decreasing":
            recommendation = "reduce"
            confidence = 0.6
            reasoning = "Declining sales trend"
        elif sales_data["sales_velocity"] > 10:  # High sales velocity
            recommendation = "increase"
            confidence = 0.8
            reasoning = "High demand item"
            
        return {
            "recommendation": recommendation,
            "confidence": confidence,
            "reasoning": reasoning,
            "days_since_last_sale": days_since_last_sale,
            "sales_velocity": sales_data["sales_velocity"]
        }
    
    def _calculate_prediction_confidence(self, item_id: int) -> float:
        """Calculate confidence score for predictions based on data quality"""
        from . import models
        
        # Count data points
        stock_records = self.db.query(models.StockHistory).filter(
            models.StockHistory.item_id == item_id
        ).count()
        
        sales_records = self.db.query(models.SalesHistory).filter(
            models.SalesHistory.item_id == item_id
        ).count()
        
        # More data = higher confidence
        total_records = stock_records + sales_records
        if total_records < 5:
            return 0.1
        elif total_records < 10:
            return 0.3
        elif total_records < 20:
            return 0.6
        else:
            return 0.9
    
    def _clean_json_values(self, data):
        """Clean data to ensure JSON compatibility"""
        if isinstance(data, dict):
            return {k: self._clean_json_values(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self._clean_json_values(item) for item in data]
        elif isinstance(data, float):
            if data == float('inf') or data == float('-inf'):
                return 999.0 if data > 0 else -999.0
            elif data != data:  # NaN check
                return 0.0
            return data
        return data

    def run_full_analytics(self, item_id: int) -> Dict:
        """Run complete analytics for an item"""
        from . import models
        
        # Get predictions
        restock_date, confidence = self.predict_restock_date(item_id)
        stock_life = self.predict_stock_life(item_id)
        optimal_quantity = self.predict_optimal_restock_quantity(item_id)
        
        # Get cost analysis
        cost_data = self.calculate_cost_optimization(item_id)
        
        # Get sales performance
        sales_data = self.analyze_sales_performance(item_id)
        
        # Get menu recommendations
        menu_data = self.generate_menu_recommendations(item_id)
        
        result = {
            "item_id": item_id,
            "predictions": {
                "restock_date": restock_date,
                "confidence": confidence,
                "stock_life_days": stock_life,
                "optimal_restock_quantity": optimal_quantity
            },
            "cost_analysis": cost_data,
            "sales_performance": sales_data,
            "menu_recommendations": menu_data
        }
        
        # Clean the result to ensure JSON compatibility
        return self._clean_json_values(result)
    
    def update_analytics_for_all_items(self):
        """Update analytics for all items"""
        from . import models
        
        items = self.db.query(models.Item).filter(models.Item.is_active == True).all()
        
        for item in items:
            analytics_data = self.run_full_analytics(item.id)
            
            # Save to ItemAnalytics table
            analytics_record = models.ItemAnalytics(
                item_id=item.id,
                predicted_restock_date=analytics_data["predictions"]["restock_date"],
                predicted_stock_life_days=analytics_data["predictions"]["stock_life_days"],
                predicted_restock_quantity=analytics_data["predictions"]["optimal_restock_quantity"],
                confidence_score=analytics_data["predictions"]["confidence"],
                avg_daily_consumption=self.calculate_daily_consumption(item.id),
                sales_velocity=analytics_data["sales_performance"]["sales_velocity"],
                model_version="1.0",
                last_training_date=datetime.now()
            )
            
            # Save to MenuOptimization table
            menu_record = models.MenuOptimization(
                item_id=item.id,
                recommendation=analytics_data["menu_recommendations"]["recommendation"],
                confidence=analytics_data["menu_recommendations"]["confidence"],
                reasoning=analytics_data["menu_recommendations"]["reasoning"],
                days_since_last_sale=analytics_data["menu_recommendations"]["days_since_last_sale"]
            )
            
            self.db.add(analytics_record)
            self.db.add(menu_record)
            
        self.db.commit() 