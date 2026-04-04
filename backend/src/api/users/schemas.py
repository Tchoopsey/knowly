from pydantic import BaseModel

from src.db.models import UserRole


class UserResponse(BaseModel):
    id: str
    team_id: str
    first_name: str
    last_name: str
    username: str
    role: UserRole

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    team_id: str
    first_name: str
    last_name: str
    email: str
    username: str
    password: str
    role: UserRole

class UserUpdate(BaseModel):
    team_id: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    email: str | None = None
    username: str | None = None
    password: str | None = None
    role: UserRole | None = None
