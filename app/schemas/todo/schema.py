from datetime import datetime
from uuid import UUID
from typing import Optional
from pydantic import BaseModel, Field

from app.schemas.base.schema import PaginationOutputSchema, SuccessSchema
from app.schemas.mixins.schema import StripLowerMixin
from app.models.todo.model import TodoPriorityEnum


class TodoSchema(BaseModel):
    """Schema for Todo"""

    id: UUID
    title: str
    description: str
    priority: TodoPriorityEnum

    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class CreateTodoInputSchema(StripLowerMixin, BaseModel):
    """Schema for Todo"""

    title: str = Field(
        ...,
        min_length=4,
        max_length=50,
        description="Title must be between 4 and 50 characters",
    )

    description: str = Field(
        ..., min_length=10, description="Description must be at least 10 characters"
    )

    priority: TodoPriorityEnum = Field(
        default=TodoPriorityEnum.LOW, description="Priority of the todo"
    )


class CreateTodoResponseSchema(SuccessSchema):
    """Schema for creating todo response"""

    data: TodoSchema


class UpdateTodoInputSchema(StripLowerMixin, BaseModel):
    """Schema for updating todo"""

    title: Optional[str] = Field(
        None,
        min_length=4,
        max_length=50,
        description="Title must be between 4 and 50 characters",
    )

    description: Optional[str] = Field(
        None, min_length=10, description="Description must be at least 10 characters"
    )

    priority: Optional[TodoPriorityEnum] = Field(
        None, description="Priority of the todo"
    )


class UpdateTodoResponseSchema(SuccessSchema):
    """Schema for updating todo response"""

    data: TodoSchema


class GetAllTodosInputSchema(BaseModel):
    """Schema for getting all todos input"""

    page: int
    per_page: int


class GetAllTodosOutputSchema(BaseModel):
    """Schema for getting all users output"""

    todos: list[TodoSchema]
    pagination: PaginationOutputSchema


class GetAllTodosResponseSchema(SuccessSchema):
    """Schema for getting all todos response"""

    data: GetAllTodosOutputSchema


class GetTodoByIdInputSchema(BaseModel):
    """Schema for getting todo by id"""

    id: UUID


class GetTodoByIdResponseSchema(SuccessSchema):
    """Schema for getting todo by id response"""

    data: TodoSchema


class DeleteTodoResponseSchema(SuccessSchema):
    """Schema for deleting todo response"""

    data: bool
