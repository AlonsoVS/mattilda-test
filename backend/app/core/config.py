import os
from typing import Optional
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Settings:
    """Application settings"""
    
    # Database settings
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/mattilda_db"
    )
    
    # API settings
    API_V1_STR: str = os.getenv("API_V1_STR", "/api/v1")
    PROJECT_NAME: str = os.getenv("PROJECT_NAME", "Mattilda API")
    PROJECT_DESCRIPTION: str = os.getenv("PROJECT_DESCRIPTION", "School Management System API")
    VERSION: str = os.getenv("VERSION", "1.0.0")
    
    # Environment
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
    
    # Database
    DB_ECHO: bool = os.getenv("DB_ECHO", "true").lower() == "true"
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
    
    # Default Admin User Configuration
    ADMIN_USERNAME: str = os.getenv("ADMIN_USERNAME", "admin")
    ADMIN_EMAIL: str = os.getenv("ADMIN_EMAIL", "admin@example.com")
    ADMIN_PASSWORD: str = os.getenv("ADMIN_PASSWORD", "admin123")
    ADMIN_FULL_NAME: str = os.getenv("ADMIN_FULL_NAME", "Admin User")
    
    # CORS
    ALLOWED_ORIGINS: str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://localhost:8080,http://localhost:5173,http://127.0.0.1:5173")
    
    @property
    def CORS_ORIGINS(self) -> list[str]:
        """Convert ALLOWED_ORIGINS string to list"""
        return [origin.strip() for origin in self.ALLOWED_ORIGINS.split(",") if origin.strip()]
    
    # Server
    APP_HOST: str = os.getenv("APP_HOST", "127.0.0.1")
    APP_PORT: int = int(os.getenv("APP_PORT", "8000"))
    RELOAD: bool = os.getenv("RELOAD", "true").lower() == "true"


settings = Settings()
