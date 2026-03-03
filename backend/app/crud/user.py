from typing import Iterable, Optional
from uuid import uuid4

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.user import User
from app.schemas.user import UserCreate


def get_user(db: Session, user_id) -> Optional[User]:
    stmt = select(User).where(User.id == user_id, User.is_deleted.is_(False))
    return db.scalar(stmt)


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email, User.is_deleted.is_(False))
    return db.scalar(stmt)


def get_users(db: Session, skip: int = 0, limit: int = 100) -> Iterable[User]:
    stmt = select(User).where(User.is_deleted.is_(False)).offset(skip).limit(limit)
    return db.scalars(stmt).all()


def create_user(db: Session, user_in: UserCreate) -> User:
    db_user = User(
        id=uuid4(),
        email=user_in.email,
        hashed_password=user_in.password,  # NOTE: plain for now; no auth yet
        full_name=user_in.full_name,
        is_active=user_in.is_active,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def soft_delete_user(db: Session, user: User) -> None:
    user.is_deleted = True
    db.add(user)
    db.commit()

