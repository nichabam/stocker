#!/usr/bin/env python3
"""
Database setup script for Stocker
This script helps you set up PostgreSQL database and create tables
"""

import os
import sys
from sqlalchemy import create_engine, text
from app.database import engine
from app.models import Base

def create_database():
    """Create the database if it doesn't exist"""
    # Connect to PostgreSQL server (not specific database)
    db_url = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost:5432/stocker")
    
    # Extract database name from URL
    if "postgresql://" in db_url:
        db_name = db_url.split("/")[-1]
        server_url = db_url.rsplit("/", 1)[0] + "/postgres"
    else:
        print("Invalid DATABASE_URL format")
        return False
    
    try:
        # Connect to default postgres database with autocommit
        temp_engine = create_engine(server_url, isolation_level="AUTOCOMMIT")
        with temp_engine.connect() as conn:
            # Check if database exists
            result = conn.execute(text(f"SELECT 1 FROM pg_database WHERE datname = '{db_name}'"))
            if not result.fetchone():
                # Create database
                conn.execute(text(f"CREATE DATABASE {db_name}"))
                print(f"✅ Database '{db_name}' created successfully")
            else:
                print(f"✅ Database '{db_name}' already exists")
        temp_engine.dispose()
        return True
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

def create_tables():
    """Create all tables"""
    try:
        Base.metadata.create_all(bind=engine)
        print("✅ All tables created successfully")
        return True
    except Exception as e:
        print(f"❌ Error creating tables: {e}")
        return False

def main():
    print("🚀 Setting up Stocker database...")
    
    # Step 1: Create database
    if not create_database():
        print("\n💡 Make sure PostgreSQL is running and accessible")
        print("💡 You may need to:")
        print("   1. Install PostgreSQL")
        print("   2. Start PostgreSQL service")
        print("   3. Create a user with appropriate permissions")
        print("   4. Set DATABASE_URL environment variable")
        sys.exit(1)
    
    # Step 2: Create tables
    if not create_tables():
        sys.exit(1)
    
    print("\n🎉 Database setup complete!")
    print("You can now run your FastAPI application")

if __name__ == "__main__":
    main() 