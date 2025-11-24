"""Application configuration management."""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator, ValidationInfo
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "FastAPI Professional App"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str
    
    # Database
    # Reordered fields so database_url can be computed from others
    db_host: str = "localhost"
    db_port: int = 5432
    db_name: str = "fastapi_db"
    db_user: str
    db_password: str
    database_url: str | None = None
    
    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: List[str] = ["http://localhost:3000"]
    
    # Security
    basic_auth_username: str = "admin"
    basic_auth_password: str = "secret"
    
    # Logging
    log_level: str = "INFO"
    
    @field_validator("cors_origins", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v):
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    @field_validator("database_url", mode='before')
    @classmethod
    def assemble_db_connection(cls, v, info: ValidationInfo):
        """Build database URL if not provided."""
        if isinstance(v, str) and v:
            return v
        
        # Build from individual components
        values = info.data
        user = values.get("db_user")
        password = values.get("db_password")
        host = values.get("db_host", "localhost")
        port = values.get("db_port", 5432)
        db = values.get("db_name")
        
        # If any component is missing, we can't build it. 
        # But since they are required fields (except host/port/db which have defaults), 
        # they should be in values if validation passed for them?
        # Wait, mode='before' runs before validation of the field itself, but info.data has *validated* previous fields.
        # db_user and db_password are required str. If they were missing, BaseSettings would have raised error?
        # Yes, hopefully.
        
        if user and password and db:
             return f"postgresql://{user}:{password}@{host}:{port}/{db}"
        
        # If we can't build it and v is None, we return None.
        # But database_url is str | None.
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = False


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()