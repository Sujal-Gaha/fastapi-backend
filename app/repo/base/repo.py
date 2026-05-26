from abc import ABC, abstractmethod
from typing import Any, Generic, Optional, TypeVar

from sqlalchemy.ext.asyncio import AsyncSession

ModelType = TypeVar("ModelType")
IDType = TypeVar("IDType")


class BaseRepository(ABC, Generic[ModelType, IDType]):
    """Abstract base repository with common CRUD operations."""

    def __init__(self, session: AsyncSession):
        self.session = session

    @abstractmethod
    async def find_by_id(self, id: IDType) -> Optional[ModelType]:
        """Retrieve a single record by ID."""
        pass

    @abstractmethod
    async def find_many(self, skip: int = 0, limit: int = 0) -> list[ModelType]:
        """Retrieve many records with pagination."""
        pass

    @abstractmethod
    async def create(self, input: dict[str, Any]) -> ModelType:
        """Create a new record from validated data."""
        pass

    @abstractmethod
    async def update(self, id: IDType, input: dict[str, Any]) -> Optional[ModelType]:
        """Update an existing record with validated data."""
        pass

    @abstractmethod
    async def delete(self, id: IDType) -> bool:
        """Delete a record by ID. Returns True if deleted."""
        pass
