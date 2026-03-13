from fastapi import APIRouter, HTTPException, status

from app.api.deps import AsyncSessionDep
from app.schemas.base.schema import PaginationOutputSchema
from app.schemas.user import (
    CreateUserInputSchema,
    UserSchema,
    CreateUserResponseSchema,
    GetUserByIdResponseSchema,
    GetAllUsersResponseSchema,
    GetAllUsersOutputSchema,
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


@router.get(
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


@router.get(
    "/get_all_users",
    response_model=GetAllUsersResponseSchema,
)
async def get_all_users(session: AsyncSessionDep, page: int = 1, per_page: int = 10):
    repo = UserRepository(session)

    users, total = await repo.get_paginated(page, per_page)

    pages = (total + per_page - 1) // per_page

    pagination = PaginationOutputSchema(
        page=page,
        per_page=per_page,
        total=total,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )

    return GetAllUsersResponseSchema(
        message="Users",
        is_success=True,
        data=GetAllUsersOutputSchema(
            users=[UserSchema.model_validate(user) for user in users],
            pagination=pagination,
        ),
    )
