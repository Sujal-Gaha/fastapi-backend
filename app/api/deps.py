from typing import Annotated

from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import get_async_session
from app.models.user import User

AsyncSessionDep = Annotated[AsyncSession, Depends(get_async_session)]


async def get_current_user(session: AsyncSessionDep) -> User:
    """
    Placeholder authentication dependency.
    Replace with JWT/OAuth2 authentication later.
    """
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )


CurrentUser = Annotated[User, Depends(get_current_user)]
