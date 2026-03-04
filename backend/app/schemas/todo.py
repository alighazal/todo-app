from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models.todo import TodoPriority, TodoStatus


class TodoBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: TodoStatus = TodoStatus.TODO
    priority: TodoPriority = TodoPriority.MEDIUM
    due_date: Optional[date] = None
    position: Optional[int] = None


class TodoCreate(TodoBase):
    pass


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TodoStatus] = None
    priority: Optional[TodoPriority] = None
    due_date: Optional[date] = None
    position: Optional[int] = None


class TodoRead(TodoBase):
    id: UUID
    project_id: UUID
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime] = None

    class ConfigDict:
        from_attributes = True
