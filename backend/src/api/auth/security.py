import jwt
from datetime import timedelta, datetime, timezone
from jwt.exceptions import InvalidTokenError
from sqlalchemy.orm import Session

from src.core.security import verify_password
from src.api.users.service import get_user_by_username

from .exceptions import CredentialsError

# Just for testing purposes:
DUMMY_SECRET_KEY="75b12c7bb9b12d63ad177776216394b3950d2ea2c281a051bcf32577e6b23d18"
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM="HS256"

def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_username(db, username)
    if not user:
        raise CredentialsError()
    if not verify_password(password, user.password):
        raise CredentialsError()
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, DUMMY_SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    try:
        payload = jwt.decode(token, DUMMY_SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except InvalidTokenError:
        raise CredentialsError()
