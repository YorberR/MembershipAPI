"""Application configuration management."""

import os
from typing import List
from pydantic_settings import BaseSettings
from pydantic import field_validator
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings."""
    
    # Application
    app_name: str = "MembershipAPI"
    app_version: str = "1.0.0"
    debug: bool = False
    secret_key: str = "your-secret-key-change-in-production"
    
    # Database - SQLite by default (works with Render free tier)
    database_url: str = "sqlite:///./data.db"
    
    # API
    api_v1_prefix: str = "/api/v1"
    cors_origins: List[str] = ["*"]
    
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
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        extra = "ignore"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()