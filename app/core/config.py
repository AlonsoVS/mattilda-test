import os
from typing import Optional


class Settings:
    """Application settings"""
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:Post12.gres@localhost:5432/mattilda_db"
    )
    
    # API settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Mattilda API"
    PROJECT_DESCRIPTION: str = "School Management System API"
    VERSION: str = "1.0.0"
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Database
    DB_ECHO: bool = os.getenv("DB_ECHO", "true").lower() == "true"


settings = Settings()
