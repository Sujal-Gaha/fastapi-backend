import uuid
import enum

from sqlalchemy import UUID, ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column
from app.db.session import Base


class TodoPriorityEnum(str, enum.Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Todo(Base):
    "Todo Model"

    __tablename__ = "todos"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True
    )

    title: Mapped[str] = mapped_column(String(50), nullable=False)
    description: Mapped[str] = mapped_column(String(250), nullable=False)

    priority: Mapped[TodoPriorityEnum] = mapped_column(
        Enum(TodoPriorityEnum, native_enum=False),
        nullable=False,
        index=True,
        default=TodoPriorityEnum.LOW,
    )
