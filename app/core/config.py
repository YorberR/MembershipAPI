"""Application configuration management."""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "FastAPI Professional App"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str
    
    # Database
    database_url: str
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "fastapi_db"
    db_user: str
    db_password: str
    
    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Security
    basic_auth_username: str = "admin"
    basic_auth_password: str = "secret"
    
    # Logging
    log_level: str = "INFO"
    
    @field_validator("cors_origins", pre=True)
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @field_validator("database_url", pre=True)
    def assemble_db_connection(cls, v, values):
        """Build database URL if not provided."""
        if isinstance(v, str) and v:
            return v
        
        # Build from individual components
        user = values.get("db_user")
        password = values.get("db_password")
        host = values.get("db_host", "localhost")
        port = values.get("db_port", 5432)
        db = values.get("db_name")
        
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()