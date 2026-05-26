from fastapi import APIRouter

from app.api.v1.user import router as user
from app.api.v1.todo import router as todo

router = APIRouter()

router.include_router(user.router, prefix="/users", tags=["users"])
router.include_router(todo.router, prefix="/todos", tags=["todos"])
