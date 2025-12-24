"""Database configuration and session management."""

from typing import Annotated, Generator
from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends
from sqlmodel import Session, SQLModel, create_engine, select

from app.core.config import get_settings
from app.core.logging import get_logger

settings = get_settings()
logger = get_logger(__name__)

# Check if using SQLite
is_sqlite = settings.database_url.startswith("sqlite")

# Create engine with appropriate settings
if is_sqlite:
    # SQLite specific settings
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        connect_args={"check_same_thread": False}
    )
else:
    # Other databases (PostgreSQL, MySQL, etc.)
    engine = create_engine(
        settings.database_url,
        echo=settings.debug,
        pool_pre_ping=True,
        pool_recycle=300,
    )


def create_db_and_tables() -> None:
    """Create database tables."""
    try:
        SQLModel.metadata.create_all(engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating database tables: {e}")
        raise


def seed_demo_data() -> None:
    """Seed database with demo data for portfolio showcase."""
    from app.models import Customer, Plan, Transaction, CustomerPlan
    
    with Session(engine) as session:
        # Check if data already exists
        existing = session.exec(select(Customer)).first()
        if existing:
            logger.info("Demo data already exists, skipping seed")
            return
        
        logger.info("Seeding demo data...")
        
        # Create demo plans
        plans = [
            Plan(name="Basic Plan", price=999, description="Basic membership with essential features"),
            Plan(name="Pro Plan", price=2999, description="Professional membership with advanced features"),
            Plan(name="Enterprise", price=9999, description="Full access enterprise membership"),
        ]
        for plan in plans:
            session.add(plan)
        session.commit()
        
        # Refresh to get IDs
        for plan in plans:
            session.refresh(plan)
        
        # Create demo customers
        customers = [
            Customer(name="John Doe", email="john@example.com", age=28, description="Premium customer"),
            Customer(name="Jane Smith", email="jane@example.com", age=34, description="VIP member"),
            Customer(name="Bob Johnson", email="bob@example.com", age=45, description="Regular customer"),
            Customer(name="Alice Brown", email="alice@example.com", age=29, description="New member"),
            Customer(name="Charlie Wilson", email="charlie@example.com", age=52, description="Long-time customer"),
        ]
        for customer in customers:
            session.add(customer)
        session.commit()
        
        # Refresh customers to get IDs
        for customer in customers:
            session.refresh(customer)
        
        # Create customer-plan associations
        associations = [
            CustomerPlan(customer_id=customers[0].id, plan_id=plans[1].id),  # John -> Pro
            CustomerPlan(customer_id=customers[1].id, plan_id=plans[2].id),  # Jane -> Enterprise
            CustomerPlan(customer_id=customers[2].id, plan_id=plans[0].id),  # Bob -> Basic
            CustomerPlan(customer_id=customers[3].id, plan_id=plans[0].id),  # Alice -> Basic
            CustomerPlan(customer_id=customers[4].id, plan_id=plans[1].id),  # Charlie -> Pro
        ]
        for assoc in associations:
            session.add(assoc)
        session.commit()
        
        # Create demo transactions
        transactions = [
            Transaction(amount=2999, description="Monthly Pro subscription", customer_id=customers[0].id),
            Transaction(amount=2999, description="Monthly Pro subscription", customer_id=customers[0].id),
            Transaction(amount=9999, description="Enterprise annual payment", customer_id=customers[1].id),
            Transaction(amount=999, description="Basic monthly subscription", customer_id=customers[2].id),
            Transaction(amount=999, description="Basic monthly subscription", customer_id=customers[3].id),
            Transaction(amount=2999, description="Pro upgrade payment", customer_id=customers[4].id),
            Transaction(amount=500, description="Add-on purchase", customer_id=customers[0].id),
            Transaction(amount=1500, description="Premium support", customer_id=customers[1].id),
        ]
        for transaction in transactions:
            session.add(transaction)
        session.commit()
        
        logger.info(f"Demo data seeded: {len(customers)} customers, {len(plans)} plans, {len(transactions)} transactions")


@asynccontextmanager
async def lifespan(app: FastAPI) -> Generator:
    """Application lifespan manager."""
    # Startup
    logger.info("Starting up application...")
    create_db_and_tables()
    seed_demo_data()  # Seed demo data on startup
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