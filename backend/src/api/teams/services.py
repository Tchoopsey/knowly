import os
import uuid
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from src.db.models import Team

from .schemas import TeamCreateOrUpdate
from .exceptions import DatabaseError, NoTeamsExist, TeamNotFound


STORAGE_PATH = f"./storage/documents/"

def get_team(team_id: str, db: Session):
    team = db.query(Team).filter_by(id=team_id).first()

    if not team:
        raise TeamNotFound
    return team

def read_teams(db: Session):
    teams = db.query(Team).all()

    if not teams:
        raise NoTeamsExist
    return teams

def read_team(team_id: str, db: Session):
    return get_team(team_id, db)

def create_team(team: TeamCreateOrUpdate, db: Session):
    team_id = str(uuid.uuid4())
    team_path = STORAGE_PATH + f"team_{team_id}/"

    os.mkdir(team_path)

    team = Team(
        id=team_id,
        team_lead_id=team.team_lead_id,
        team_name=team.team_name,
        team_path=team_path
    )

    try:
        db.add(team)
        db.commit()
        db.refresh(team)
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(str(e))

    return team

def edit_team(team_id: str, team_update: TeamCreateOrUpdate, db: Session):
    team = get_team(team_id, db)

    update_data = team_update.model_dump(exclude_unset=True)
    update_data = {k: v for k, v in update_data.items() if v not in (None, "")}
    
    for field, value in update_data.items():
        setattr(team, field, value)

    try:
        db.commit()
    except SQLAlchemyError as e:
        raise DatabaseError(str(e))

    return team

def remove_team(team_id: str, db: Session):
    team = get_team(team_id, db)

    try:
        db.delete(team)
        db.commit()
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(str(e))
