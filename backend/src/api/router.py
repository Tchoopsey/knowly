from fastapi import APIRouter

from .documents.routes import router as doc_router
from .users.routes import router as user_router
from .teams.routes import router as team_router
from .auth.routes import router as auth_router

api_router = APIRouter()

api_router.include_router(doc_router, prefix="", tags=["documents"])
api_router.include_router(user_router, prefix="", tags=["users"])
api_router.include_router(team_router, prefix="", tags=["teams"])
api_router.include_router(auth_router, prefix="", tags=["auth"])
