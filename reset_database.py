#!/usr/bin/env python3
"""
Database Reset Script
Drops all tables and recreates them with the new schema
"""

import sys
import os

# Add the app directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app.database import engine
from app import models

def reset_database():
    """Drop all tables and recreate them"""
    print("🗄️  Resetting database...")
    
    try:
        # Drop all tables
        print("📉 Dropping all tables...")
        models.Base.metadata.drop_all(bind=engine)
        print("✅ Tables dropped successfully")
        
        # Create all tables with new schema
        print("📈 Creating new tables...")
        models.Base.metadata.create_all(bind=engine)
        print("✅ Tables created successfully")
        
        print("🎉 Database reset complete!")
        print("\n📋 New tables created:")
        print("- items (with cost_per_unit, is_active, last_sale_date)")
        print("- categories")
        print("- stock_history")
        print("- restock_history (with cost_per_unit)")
        print("- sales_history (NEW)")
        print("- item_analytics (NEW)")
        print("- menu_optimization (NEW)")
        
    except Exception as e:
        print(f"❌ Error resetting database: {e}")
        sys.exit(1)

if __name__ == "__main__":
    reset_database() 