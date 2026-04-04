from passlib.context import CryptContext


password_context = CryptContext(schemes=["argon2"])

def hash_password(usr_pwd: str):
    return password_context.hash(usr_pwd)

def verify_password(plain: str, hashed: str):
    return password_context.verify(plain, hashed)
