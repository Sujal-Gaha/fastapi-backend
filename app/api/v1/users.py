from fastapi import APIRouter, HTTPException, status

from app.api.deps import AsyncSessionDep
from app.schemas.user import CreateUserInputSchema, UserSchema, CreateUserResponseSchema
from app.repo.user import UserRepository

from app.core.exceptions import DuplicateEmailError
from app.core.logging import logger

router = APIRouter()


@router.post(
    "/users",
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
