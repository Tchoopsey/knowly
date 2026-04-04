from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from src.api.auth.exceptions import CredentialsError
from src.api.auth.security import decode_access_token
from src.db.models import User, UserRole
from src.db.session import get_db
from src.api.users.service import get_user


ROLE_HIERARCHY = {
    UserRole.ADMIN: 4,
    UserRole.TEAM_LEAD: 3,
    UserRole.SUPERVISOR: 2,
    UserRole.WORKER: 1,
}

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def has_higher_or_equal_role(user: User, role: UserRole):
    return ROLE_HIERARCHY[user.role] >= ROLE_HIERARCHY[role]

def get_current_user(
        token: str = Depends(oauth2_scheme),
        db: Session = Depends(get_db)
):
    payload = decode_access_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise CredentialsError()
    user = get_user(user_id, db)
    return user
