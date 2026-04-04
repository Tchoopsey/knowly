import uuid
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.core.security import hash_password
from src.db.models import User, UserRole
from src.api.permissions.exceptions import PermissionDenied

from .schemas import UserCreate, UserUpdate
from .exceptions import DatabaseError, NoUsersExist, UserNotFound


def read_users(db: Session, current_user: User):
    if current_user.role == UserRole.ADMIN:
        return db.query(User).all()

    users = db.query(User).filter_by(team_id=current_user.team_id).all()
    if not users:
        raise NoUsersExist
    return users

def read_user(user_id: str, db: Session, current_user: User):
    user = get_user(user_id, db)
    if not user.team_id == current_user.team_id:
        raise UserNotFound
    return user

def create_user(new_user: UserCreate, db: Session, superuser: User):
    if not superuser:
        raise PermissionDenied

    hashed_password = hash_password(new_user.password)
    user = User(
        id=str(uuid.uuid4()),
        team_id=new_user.team_id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        email=new_user.email,
        username=new_user.username,
        password=hashed_password,
        role=new_user.role
    )

    try:
        db.add(user)
        db.commit()
        db.refresh(user)
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(str(e))

    return user

def remove_user(user_id: str, db: Session, superuser: User):
    if not superuser:
        raise PermissionDenied

    user = get_user(user_id, db)

    try:
        db.delete(user)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(str(e))

def edit_user(user_id: str, user_update: UserUpdate, db: Session):
    user = get_user(user_id, db)
    update_data = user_update.model_dump(exclude_unset=True)
    update_data = {k: v for k, v in update_data.items() if v not in (None, "")}

    for field, value in update_data.items():
        setattr(user, field, value)

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(str(e))

    db.refresh(user)

    return user

def get_user(user_id: str, db: Session):
    user = db.query(User).filter_by(id=user_id).first()
    if not user:
        raise UserNotFound
    return user

def get_user_by_username(db: Session, username: str):
    user = db.query(User).filter_by(username=username).first()
    if not user:
        raise UserNotFound
    return user

def is_member_of_team(user: User, team_id: str) -> bool:
    return user.team_id == team_id
