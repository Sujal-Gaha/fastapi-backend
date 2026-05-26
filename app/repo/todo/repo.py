from typing import Any, Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.todo.model import Todo
from app.repo.base.repo import BaseRepository


class TodoRepository(BaseRepository[Todo, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = Todo

    async def find_by_id(self, id: UUID) -> Optional[Todo]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_many(self, skip: int = 0, limit: int = 0) -> list[Todo]:
        stmt = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, input: dict[str, Any]) -> Todo:
        db_todo = self.model(
            user_id=input["user_id"],
            title=input["title"],
            description=input["description"],
            priority=input.get("priority"),
        )
        self.session.add(db_todo)
        await self.session.commit()
        await self.session.refresh(db_todo)
        return db_todo

    async def update(self, id: UUID, input: dict[str, Any]) -> Optional[Todo]:
        todo = await self.find_by_id(id)
        if not todo:
            return None

        for key, value in input.items():
            if value is not None and hasattr(todo, key):
                setattr(todo, key, value)

        await self.session.commit()
        await self.session.refresh(todo)
        return todo

    async def delete(self, id: UUID) -> bool:
        todo = await self.find_by_id(id)

        if not todo:
            return False

        await self.session.delete(todo)
        await self.session.commit()
        return True

    async def get_paginated(
        self, page: int, per_page: int, user_id: Optional[UUID] = None
    ) -> tuple[list[Todo], int]:
        stmt = (
            select(self.model)
            .order_by(self.model.id)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        
        count_stmt = select(func.count(self.model.id))

        if user_id:
            stmt = stmt.where(self.model.user_id == user_id)
            count_stmt = count_stmt.where(self.model.user_id == user_id)

        result = await self.session.execute(stmt)
        todos = list(result.scalars().all())
        total = await self.session.scalar(count_stmt) or 0

        return todos, total
    
    async def find_by_user_id(self, user_id: UUID) -> list[Todo]:
        stmt = select(self.model).where(self.model.user_id == user_id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())
