from datetime import datetime
from enum import Enum

from sqlalchemy import Date, DateTime, Enum as SAEnum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class TodoStatus(str, Enum):
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    DONE = "done"
    ARCHIVED = "archived"


class TodoPriority(int, Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class Todo(Base):
    __tablename__ = "todos"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
    )
    project_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("projects.id", ondelete="CASCADE"),
        nullable=False,
    )
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[TodoStatus] = mapped_column(
        SAEnum(
            TodoStatus,
            name="todo_status",
            create_type=False,
        ),
        nullable=False,
        default=TodoStatus.TODO,
        server_default=TodoStatus.TODO.value,
    )
    priority: Mapped[TodoPriority] = mapped_column(
        SAEnum(
            TodoPriority,
            name="todo_priority",
            create_type=False,
        ),
        nullable=False,
        default=TodoPriority.MEDIUM,
        server_default=str(TodoPriority.MEDIUM.value),
    )
    due_date: Mapped[datetime | None] = mapped_column(Date, nullable=True)
    position: Mapped[int | None] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        server_default="now()",
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        server_default="now()",
    )
    completed_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)

    project = relationship("Project", back_populates="todos")

