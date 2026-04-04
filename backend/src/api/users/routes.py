from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.models import User, UserRole
from src.db.session import get_db
from src.api.auth.dependencies import get_current_user
from src.api.permissions.dependencies import require_role
from src.api.users.service import edit_user, read_user, read_users, create_user as new_user, remove_user

from .schemas import UserCreate, UserResponse, UserUpdate


router = APIRouter()

@router.get("/knowly/users/{user_id}", response_model=UserResponse)
async def get_user(
        user_id: str, 
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
):
    return read_user(user_id, db, current_user)

@router.get("/knowly/users/", response_model=list[UserResponse])
async def get_users(
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
):
    return read_users(db, user)

@router.post(
    "/knowly/users/", 
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_user(
        user: UserCreate, 
        db: Session = Depends(get_db),
        superuser: User = Depends(require_role(UserRole.ADMIN))
):
    return new_user(user, db, superuser)

@router.delete("/knowly/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: str, 
        db: Session = Depends(get_db),
        superuser: User = Depends(require_role(UserRole.ADMIN))
):
    return remove_user(user_id, db, superuser)

@router.patch("/knowly/users/{user_id}", response_model=UserResponse)
async def update_user(
        user: UserUpdate, 
        db: Session = Depends(get_db),
        current_user = Depends(get_current_user)
):
    return edit_user(current_user.id, user, db)
