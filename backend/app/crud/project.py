from typing import Iterable, Optional
from uuid import UUID, uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_project(db: Session, project_id: UUID) -> Optional[Project]:
    stmt = select(Project).where(Project.id == project_id)
    return db.scalar(stmt)


def get_projects(
    db: Session,
    *,
    owner_id: Optional[UUID] = None,
    skip: int = 0,
    limit: int = 100,
) -> Iterable[Project]:
    stmt = select(Project)
    if owner_id is not None:
        stmt = stmt.where(Project.owner_id == owner_id)
    stmt = stmt.offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_project(db: Session, project_in: ProjectCreate) -> Project:
    db_project = Project(
        id=uuid4(),
        name=project_in.name,
        description=project_in.description,
        owner_id=project_in.owner_id,
    )
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    return db_project


def update_project(db: Session, project: Project, project_in: ProjectUpdate) -> Project:
    if project_in.name is not None:
        project.name = project_in.name
    if project_in.description is not None:
        project.description = project_in.description
    db.add(project)
    db.commit()
    db.refresh(project)
    return project


def delete_project(db: Session, project: Project) -> None:
    db.delete(project)
    db.commit()
