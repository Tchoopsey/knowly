from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from src.db.models import User, UserRole
from src.db.session import get_db
from src.api.permissions.dependencies import require_role

from .schemas import TeamCreateOrUpdate, TeamResponse
from .services import edit_team, read_team, read_teams, create_team as new_team, remove_team


router = APIRouter()

@router.get("/teams", response_model=list[TeamResponse])
async def get_teams(
        db: Session = Depends(get_db),
        user: User = Depends(require_role(UserRole.ADMIN))
):
    return read_teams(db)

@router.get("/teams/{team_id}", response_model=TeamResponse)
async def get_team(
        team_id: str, 
        db: Session = Depends(get_db),
        user: User = Depends(require_role(UserRole.TEAM_LEAD))
):
    return read_team(team_id, db)

@router.post(
    "/teams", 
    response_model=TeamResponse, 
    status_code=status.HTTP_201_CREATED)
async def create_team(
        team: TeamCreateOrUpdate, 
        db: Session = Depends(get_db),
        user: User = Depends(require_role(UserRole.ADMIN))
):
    return new_team(team, db)

@router.patch("/teams/{team_id}", response_model=TeamResponse)
async def update_team(
        team_id: str, 
        team: TeamCreateOrUpdate, 
        db: Session = Depends(get_db),
        user: User = Depends(require_role(UserRole.ADMIN))
):
    return edit_team(team_id, team, db)

@router.delete("/teams/{team_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_team(
        team_id: str, 
        db: Session = Depends(get_db),
        user: User = Depends(require_role(UserRole.ADMIN))
):
    return remove_team(team_id, db)
