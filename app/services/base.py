"""Base service class."""

from typing import Generic, TypeVar, Type, Optional, List
from sqlmodel import Session, SQLModel, select
from sqlalchemy.exc import IntegrityError

from app.api.exceptions import NotFoundError, ConflictError
from app.core.logging import get_logger

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)

logger = get_logger(__name__)


class BaseService(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """Base service with CRUD operations."""
    
    def __init__(self, model: Type[ModelType]):
        self.model = model
    
    def get(self, db: Session, id: int) -> Optional[ModelType]:
        """Get a single record by ID."""
        return db.get(self.model, id)
    
    def get_or_404(self, db: Session, id: int) -> ModelType:
        """Get a single record by ID or raise 404."""
        obj = self.get(db, id)
        if not obj:
            raise NotFoundError(self.model.__name__, id)
        return obj
    
    def get_multi(
        self, 
        db: Session, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[ModelType]:
        """Get multiple records with pagination."""
        statement = select(self.model).offset(skip).limit(limit)
        return db.exec(statement).all()
    
    def count(self, db: Session) -> int:
        """Count total records."""
        statement = select(self.model)
        return len(db.exec(statement).all())
    
    def create(self, db: Session, obj_in: CreateSchemaType) -> ModelType:
        """Create a new record."""
        try:
            obj_data = obj_in.model_dump()
            db_obj = self.model(**obj_data)
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"Created {self.model.__name__} with id {db_obj.id}")
            return db_obj
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error creating {self.model.__name__}: {e}")
            raise ConflictError("Resource already exists or violates constraints")
    
    def update(
        self, 
        db: Session, 
        db_obj: ModelType, 
        obj_in: UpdateSchemaType
    ) -> ModelType:
        """Update an existing record."""
        try:
            obj_data = obj_in.model_dump(exclude_unset=True)
            for field, value in obj_data.items():
                setattr(db_obj, field, value)
            
            db.add(db_obj)
            db.commit()
            db.refresh(db_obj)
            logger.info(f"Updated {self.model.__name__} with id {db_obj.id}")
            return db_obj
        except IntegrityError as e:
            db.rollback()
            logger.error(f"Integrity error updating {self.model.__name__}: {e}")
            raise ConflictError("Update violates constraints")
    
    def delete(self, db: Session, id: int) -> bool:
        """Delete a record by ID."""
        obj = self.get_or_404(db, id)
        db.delete(obj)
        db.commit()
        logger.info(f"Deleted {self.model.__name__} with id {id}")
        return True