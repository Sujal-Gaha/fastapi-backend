from fastapi import APIRouter, HTTPException, status

from app.api.deps import AsyncSessionDep
from app.schemas.user import (
    CreateUserInputSchema,
    UserSchema,
    CreateUserResponseSchema,
    GetUserByIdResponseSchema,
    GetUserByIdInputSchema,
)
from app.repo.user import UserRepository

from app.core.exceptions import DuplicateEmailError
from app.core.logging import logger

router = APIRouter()


@router.post(
    "/create_user",
    response_model=CreateUserResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_user(session: AsyncSessionDep, user_data: CreateUserInputSchema):
    repo = UserRepository(session)

    try:
        user = await repo.create(user_data.model_dump())
    except DuplicateEmailError as e:
        logger.warning(f"Duplicate email attempt: {e}")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))

    return CreateUserResponseSchema(
        message="User created successfully", data=UserSchema.model_validate(user)
    )


@router.post(
    "/get_user_by_id/{user_id}",
    response_model=GetUserByIdResponseSchema,
    status_code=status.HTTP_200_OK,
)
async def get_user_by_id(session: AsyncSessionDep, user_id: str):
    repo = UserRepository(session=session)

    user = await repo.find_by_id(user_id)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="User not found"
        )

    return GetUserByIdResponseSchema(
        message="User retrieved", is_success=True, data=UserSchema.model_validate(user)
    )
