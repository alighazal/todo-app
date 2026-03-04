from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.crud import project as crud_project
from app.crud import todo as crud_todo
from app.schemas.todo import TodoCreate, TodoRead, TodoUpdate

router = APIRouter(prefix="/projects/{project_id}/todos", tags=["todos"])


def _require_project(db: Session, project_id: UUID) -> None:
    project = crud_project.get_project(db, project_id)
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Project not found")


@router.post("/", response_model=TodoRead, status_code=status.HTTP_201_CREATED)
def create_todo(
    project_id: UUID,
    todo_in: TodoCreate,
    db: Session = Depends(get_db),
) -> TodoRead:
    _require_project(db, project_id)
    return crud_todo.create_todo(db, project_id, todo_in)


@router.get("/", response_model=List[TodoRead])
def list_todos(
    project_id: UUID,
    skip: int = 0,
    limit: int = Query(100, le=100),
    db: Session = Depends(get_db),
) -> List[TodoRead]:
    _require_project(db, project_id)
    todos = crud_todo.get_todos(db, project_id, skip=skip, limit=limit)
    return list(todos)


@router.get("/{todo_id}", response_model=TodoRead)
def get_todo(
    project_id: UUID,
    todo_id: UUID,
    db: Session = Depends(get_db),
) -> TodoRead:
    todo = crud_todo.get_todo(db, todo_id, project_id=project_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return todo


@router.patch("/{todo_id}", response_model=TodoRead)
def update_todo(
    project_id: UUID,
    todo_id: UUID,
    todo_in: TodoUpdate,
    db: Session = Depends(get_db),
) -> TodoRead:
    todo = crud_todo.get_todo(db, todo_id, project_id=project_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    return crud_todo.update_todo(db, todo, todo_in)


@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(
    project_id: UUID,
    todo_id: UUID,
    db: Session = Depends(get_db),
) -> None:
    todo = crud_todo.get_todo(db, todo_id, project_id=project_id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found")
    crud_todo.delete_todo(db, todo)
    return None
