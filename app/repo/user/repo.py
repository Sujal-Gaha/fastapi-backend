from typing import Any, Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.repo.base.repo import BaseRepository
from app.models.user.model import User
from app.core.security import get_password_hash
from app.core.logging import logger
from app.core.exceptions import DuplicateEmailError


class UserRepository(BaseRepository[User, UUID]):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.model = User

    async def find_by_id(self, id: UUID) -> Optional[User]:
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def find_many(self, skip: int = 0, limit: int = 0) -> list[User]:
        stmt = select(self.model).offset(skip).limit(limit).order_by(self.model.id)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def create(self, input: dict[str, Any]) -> User:
        hashed_password = get_password_hash(input["password"])
        db_user = self.model(
            email=input["email"],
            username=input["username"],
            password=hashed_password,
        )
        self.session.add(db_user)

        try:
            await self.session.commit()
            await self.session.refresh(db_user)
            return db_user

        except IntegrityError as e:
            await self.session.rollback()
            logger.error(f"IntegrityError creating user: {e}")
            raise DuplicateEmailError("Email already registered") from e

    async def update(self, id: UUID, input: dict[str, Any]) -> Optional[User]:
        user = await self.find_by_id(id)
        if not user:
            return None

        if "username" in input:
            user.username = input["username"]

        await self.session.commit()
        await self.session.refresh(user)
        return user

    async def delete(self, id: UUID) -> bool:
        user = await self.find_by_id(id)
        if not user:
            return False

        await self.session.delete(user)
        await self.session.commit()
        return True

    # Domain-specific methods
    async def find_by_email(self, email: str) -> Optional[User]:
        stmt = select(self.model).where(self.model.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def get_paginated(self, page: int, per_page: int) -> tuple[list[User], int]:
        stmt = (
            select(self.model)
            .order_by(self.model.id)
            .offset((page - 1) * per_page)
            .limit(per_page)
        )
        result = await self.session.execute(stmt)
        users = list(result.scalars().all())
        total = await self.session.scalar(select(func.count(self.model.id))) or 0

        return users, total
