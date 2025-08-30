"""Database configuration and session management."""

from typing import Annotated, Generator
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import Session, SQLModel, create_engine
from sqlalchemy.pool import StaticPool

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

# Create engine with PostgreSQL support
engine = create_engine(
    settings.database_url,
    echo=settings.debug,  # Log SQL queries in debug mode
    pool_pre_ping=True,   # Verify connections before use
    pool_recycle=300,     # Recycle connections every 5 minutes
)


def create_db_and_tables() -> None:
    """Create database tables."""
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator:
    """Application lifespan manager."""
    # Startup
    logger.info("Starting up application...")
    create_db_and_tables()
    yield
    # Shutdown
    logger.info("Shutting down application...")


def get_session() -> Generator[Session, None, None]:
    """Get database session."""
    with Session(engine) as session:
        try:
            yield session
        except Exception as e:
            logger.error(f"Database session error: {e}")
            session.rollback()
            raise
        finally:
            session.close()


# Dependency for FastAPI routes
SessionDep = Annotated[Session, Depends(get_session)]