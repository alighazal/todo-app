from typing import Iterable, Optional
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.todo import Todo
from app.schemas.todo import TodoCreate, TodoUpdate


def get_todo(db: Session, todo_id: UUID, *, project_id: Optional[UUID] = None) -> Optional[Todo]:
    stmt = select(Todo).where(Todo.id == todo_id)
    if project_id is not None:
        stmt = stmt.where(Todo.project_id == project_id)
    return db.scalar(stmt)


def get_todos(
    db: Session,
    project_id: UUID,
    *,
    skip: int = 0,
    limit: int = 100,
) -> Iterable[Todo]:
    stmt = (
        select(Todo)
        .where(Todo.project_id == project_id)
        .offset(skip)
        .limit(limit)
    )
    return db.scalars(stmt).all()


def create_todo(db: Session, project_id: UUID, todo_in: TodoCreate) -> Todo:
    db_todo = Todo(
        id=uuid4(),
        project_id=project_id,
        title=todo_in.title,
        description=todo_in.description,
        status=todo_in.status,
        priority=todo_in.priority,
        due_date=todo_in.due_date,
        position=todo_in.position,
    )
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    return db_todo


def update_todo(db: Session, todo: Todo, todo_in: TodoUpdate) -> Todo:
    if todo_in.title is not None:
        todo.title = todo_in.title
    if todo_in.description is not None:
        todo.description = todo_in.description
    if todo_in.status is not None:
        todo.status = todo_in.status
    if todo_in.priority is not None:
        todo.priority = todo_in.priority
    if todo_in.due_date is not None:
        todo.due_date = todo_in.due_date
    if todo_in.position is not None:
        todo.position = todo_in.position
    db.add(todo)
    db.commit()
    db.refresh(todo)
    return todo


def delete_todo(db: Session, todo: Todo) -> None:
    db.delete(todo)
    db.commit()
