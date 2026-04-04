import os, uuid
from datetime import datetime, timezone

from fastapi import UploadFile
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.db.models import Document as Doc, Team
from .exceptions import DatabaseError, DocumentNotFound, FileSaveError, NoDocumentsExist, TeamNotFound


STORAGE_PATH = f"./storage/documents/"


def create_filename():
    now = datetime.now(timezone.utc)
    timestamp = now.strftime("%Y%m%d%H%M%S%f")
    return f"{timestamp}.txt"

async def save_document(team_id: str, file: UploadFile, db: Session):
    # TODO: implement FileAlreadyExists exception!!!!
    team_path = STORAGE_PATH + f"team_{team_id}"
    filename = file.filename
    if not filename:
        filename = create_filename()
    os.makedirs(team_path, exist_ok=True)
    abs_path = os.path.join(team_path, filename)

    content = await file.read()
    try:
        with open(abs_path, 'wb') as f:
            f.write(content)
    except OSError as e:
        raise FileSaveError(f"Cannot save file: {str(e)}")
    
    created_at = datetime.now(timezone.utc)
    doc = Doc(
        id=str(uuid.uuid4()),
        team_id=team_id,
        filename=filename,
        filepath=abs_path,
        filetype=filename.split(".")[-1],
        created_at=created_at,
        updated_at=created_at
    )

    try:
        db.add(doc)
        db.commit()
        db.refresh(doc)
    except SQLAlchemyError as e:
        db.rollback()
        os.remove(abs_path)
        raise DatabaseError(str(e))

    return doc

def read_documents(team_id: str, db: Session):
    exists = db.query(Team).filter(Team.id == team_id).first()
    if not exists:
        raise TeamNotFound()
    docs = db.query(Doc).filter_by(team_id=team_id).all()
    if not docs:
        raise NoDocumentsExist()
    return docs

def read_document(team_id: str, doc_id: str, db: Session):
    exists = db.query(Team).filter(Team.id == team_id).first()
    if not exists:
        raise TeamNotFound()
    doc = db.query(Doc).filter_by(team_id=team_id, id=doc_id).first()
    if not doc:
        raise DocumentNotFound()

    return doc

def remove_document(team_id: str, doc_id: str, db: Session):
    doc = db.query(Doc).filter_by(team_id=team_id, id=doc_id).first()
    if not doc:
        raise DocumentNotFound()

    if os.path.exists(str(doc.filepath)):
        os.remove(str(doc.filepath))

    try:
        db.delete(doc)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(str(e))

def edit_document(
        team_id: str, 
        doc_id: str, 
        name: str | None, 
        description: str | None,
        db: Session
):
    exists = db.query(Doc).filter(Doc.team_id == team_id).first()
    if not exists:
        raise TeamNotFound()
    doc = db.query(Doc).filter_by(team_id=team_id, id=doc_id).first()
    if not doc:
        raise DocumentNotFound()

    filepath = doc.filepath
    print(filepath)

    if name is not None and name != "": 
        doc.filename = name
        doc.filepath = os.path.join(STORAGE_PATH + f"team_{team_id}", name)
    if not os.path.exists(filepath):
        raise DocumentNotFound()
    os.rename(filepath, doc.filepath)

    if description is not None: doc.description = description

    doc.updated_at = datetime.now(timezone.utc)

    try:
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(str(e))

    db.refresh(doc)

    return doc

# def replace_document(
#         team_id: str, 
#         doc_id: str, 
#         file: UploadFile = File(...)
# ):
#     """
#     TODO: Implement replacement of the file
#     """
#     pass
