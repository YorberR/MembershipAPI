"""Logging configuration."""

import logging
import os
import sys
from typing import Dict, Any

from .config import get_settings

settings = get_settings()


def setup_logging() -> None:
    """Configure application logging."""
    
    # Create logs directory if it doesn't exist
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)
    
    # Configure root logger
    logging.basicConfig(
        level=getattr(logging, settings.log_level.upper()),
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler(sys.stdout),
            logging.FileHandler(os.path.join(logs_dir, "app.log"))
        ]
    )
    
    # Configure specific loggers
    loggers = {
        "uvicorn": logging.INFO,
        "uvicorn.error": logging.INFO,
        "uvicorn.access": logging.INFO,
        "sqlalchemy.engine": logging.WARNING if not settings.debug else logging.INFO,
    }
    
    for logger_name, level in loggers.items():
        logging.getLogger(logger_name).setLevel(level)


def get_logger(name: str) -> logging.Logger:
    """Get a logger instance."""
    return logging.getLogger(name)