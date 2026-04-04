"""
Provides routes for the Document
"""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from src.db.models import User
from src.db.session import get_db
from src.api.permissions.dependencies import require_role_and_team_access, require_team_access
from .schemas import *
from .service import *


router = APIRouter()

@router.get("/knowly/documents/{team_id}/{doc_id}", response_model=DocumentResponse)
async def get_document(
        team_id: str, 
        doc_id: str, 
        db: Session = Depends(get_db),
        user: User = Depends(require_team_access)
):
    return read_document(team_id, doc_id, db)

@router.get("/knowly/documents/{team_id}/", response_model=list[DocumentResponse])
async def get_documents(
        team_id: str, 
        db: Session = Depends(get_db),
        user: User = Depends(require_team_access)
):
    return read_documents(team_id, db)

@router.post(
    "/knowly/documents/{team_id}/", 
    status_code=status.HTTP_201_CREATED,
    response_model=DocumentResponse
)
async def upload_document(
        team_id: str,
        file: UploadFile = File(...),
        db: Session = Depends(get_db),
        user: User = Depends(require_role_and_team_access)
):
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authorized"
        )
    return await save_document(team_id, file, db)

@router.patch("/knowly/documents/{team_id}/{doc_id}", response_model=DocumentResponse)
async def update_document(
        team_id: str, 
        doc_id: str,
        update_data: DocumentUpdate,
        db: Session = Depends(get_db),
        user: User = Depends(require_role_and_team_access)
):
    return edit_document(
        team_id, 
        doc_id, 
        update_data.name, 
        update_data.description,
        db
    )

@router.delete(
    "/knowly/documents/{team_id}/{doc_id}", 
    status_code=status.HTTP_204_NO_CONTENT
)
async def delete_document(
        team_id: str, 
        doc_id: str,
        db: Session = Depends(get_db),
        user: User = Depends(require_role_and_team_access)
):
    return remove_document(team_id, doc_id, db)

# @router.put("/knowly/documents/{team_id}/{doc_id}")
# async def put_document(
#         team_id: str,
#         doc_id: str,
#         UploadFile = File(...)
# ):
#     pass
