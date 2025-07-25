import os
from typing import Optional

class Settings:
    # Database Configuration
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL", 
        "postgresql://postgres:password@localhost:5432/stocker"
    )
    
    # You can add more configuration settings here
    # API_KEY: Optional[str] = os.getenv("API_KEY")
    # DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings() 