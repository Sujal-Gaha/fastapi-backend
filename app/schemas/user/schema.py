from datetime import datetime
from pydantic import BaseModel, EmailStr, Field, field_validator

from uuid import UUID

from app.schemas.base import SuccessSchema, PaginationOutputSchema
from app.schemas.mixins import StripLowerMixin


class UserSchema(BaseModel):
    "Schema of User"

    id: str
    username: str
    email: EmailStr

    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CreateUserInputSchema(StripLowerMixin, BaseModel):
    """Schema for creting user"""

    username: str = Field(
        ...,
        min_length=8,
        max_length=30,
        description="Username between 8 and 30 characters",
    )

    email: EmailStr

    password: str = Field(
        ...,
        min_length=8,
        description="Password must be at least 8 characters",
    )

    @field_validator("username")
    @classmethod
    def validate_username(cls, value: str):
        if not value.strip():
            raise ValueError("Username cannot be empty or whitespace.")

        if not any(c.isalpha() for c in value):
            raise ValueError("Username must contain at least one letter.")

        return value


class CreateUserResponseSchema(SuccessSchema):
    """Schema for creating user response"""

    data: UserSchema


class GetAllUsersInputSchema(BaseModel):
    """Schema for getting all users"""

    page: int
    per_page: int


class GetAllUsersOutputSchema(BaseModel):
    """Schema for getting all users output"""

    users: list[UserSchema]
    pagination: PaginationOutputSchema


class GetAllUsersResponseSchema(SuccessSchema):
    """Schema for getting all users response"""

    data: GetAllUsersOutputSchema


class GetUserByIdInputSchema(BaseModel):
    """Schema for getting user by id"""

    id: UUID


class GetUserByIdResponseSchema(SuccessSchema):
    """Schema for getting user by id response"""

    data: UserSchema
