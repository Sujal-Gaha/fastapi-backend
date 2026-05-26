from fastapi import APIRouter, HTTPException, status
from uuid import UUID
from typing import Optional

from app.api.deps import AsyncSessionDep
from app.schemas.todo.schema import (
    CreateTodoInputSchema,
    CreateTodoResponseSchema,
    UpdateTodoInputSchema,
    UpdateTodoResponseSchema,
    GetTodoByIdResponseSchema,
    GetAllTodosResponseSchema,
    GetAllTodosOutputSchema,
    DeleteTodoResponseSchema,
    TodoSchema,
)
from app.repo.todo.repo import TodoRepository
from app.schemas.base.schema import PaginationOutputSchema

router = APIRouter()


@router.post(
    "/create_todo",
    response_model=CreateTodoResponseSchema,
    status_code=status.HTTP_201_CREATED,
)
async def create_todo(
    session: AsyncSessionDep, user_id: UUID, todo_data: CreateTodoInputSchema
):
    repo = TodoRepository(session)

    input_data = todo_data.model_dump()
    input_data["user_id"] = user_id

    todo = await repo.create(input_data)

    return CreateTodoResponseSchema(
        message="Todo created successfully",
        is_success=True,
        data=TodoSchema.model_validate(todo),
    )


@router.get(
    "/get_todo/{todo_id}",
    response_model=GetTodoByIdResponseSchema,
)
async def get_todo(session: AsyncSessionDep, todo_id: UUID):
    repo = TodoRepository(session)
    todo = await repo.find_by_id(todo_id)

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return GetTodoByIdResponseSchema(
        message="Todo retrieved successfully",
        is_success=True,
        data=TodoSchema.model_validate(todo),
    )


@router.get(
    "/get_todos",
    response_model=GetAllTodosResponseSchema,
)
async def get_todos(
    session: AsyncSessionDep,
    user_id: Optional[UUID] = None,
    page: int = 1,
    per_page: int = 10,
):
    repo = TodoRepository(session)
    todos, total = await repo.get_paginated(page, per_page, user_id=user_id)

    pages = (total + per_page - 1) // per_page

    pagination = PaginationOutputSchema(
        page=page,
        per_page=per_page,
        total=total,
        pages=pages,
        has_next=page < pages,
        has_prev=page > 1,
    )

    return GetAllTodosResponseSchema(
        message="Todos retrieved successfully",
        is_success=True,
        data=GetAllTodosOutputSchema(
            todos=[TodoSchema.model_validate(todo) for todo in todos],
            pagination=pagination,
        ),
    )


@router.patch(
    "/update_todo/{todo_id}",
    response_model=UpdateTodoResponseSchema,
)
async def update_todo(
    session: AsyncSessionDep, todo_id: UUID, todo_data: UpdateTodoInputSchema
):
    repo = TodoRepository(session)
    todo = await repo.update(todo_id, todo_data.model_dump(exclude_unset=True))

    if not todo:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return UpdateTodoResponseSchema(
        message="Todo updated successfully",
        is_success=True,
        data=TodoSchema.model_validate(todo),
    )


@router.delete(
    "/delete_todo/{todo_id}",
    response_model=DeleteTodoResponseSchema,
)
async def delete_todo(session: AsyncSessionDep, todo_id: UUID):
    repo = TodoRepository(session)
    success = await repo.delete(todo_id)

    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found"
        )

    return DeleteTodoResponseSchema(
        message="Todo deleted successfully", is_success=True, data=True
    )
