from fastapi import Depends

from src.api.auth.dependencies import ROLE_HIERARCHY, get_current_user
from src.db.models import User, UserRole
from src.api.users.exceptions import UserNotMemberOfTeam
from src.api.users.service import is_member_of_team

from .exceptions import PermissionDenied


def require_role(role: UserRole):
    def role_checker(user: User = Depends(get_current_user)):
        if ROLE_HIERARCHY[user.role] < ROLE_HIERARCHY[role]:
            raise PermissionDenied
        return user
    return role_checker

def require_team_access(
        team_id: str,
        user: User = Depends(get_current_user),
):
    if user.role == UserRole.ADMIN:
        return user
    if not is_member_of_team(user, team_id):
        raise UserNotMemberOfTeam()

def require_role_and_team_access(
        team_id: str,
        user: User = Depends(require_role(UserRole.SUPERVISOR))
):
    if not is_member_of_team(user, team_id):
        raise UserNotMemberOfTeam()
