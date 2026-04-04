from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from src.api.auth.exceptions import CredentialsError
from src.api.permissions.exceptions import PermissionDenied

from .api.users.exceptions import NoUsersExist, UserNotFound, UserNotMemberOfTeam
from .api.documents.exceptions import *
from .api.teams.exceptions import NoTeamsExist, TeamNotFound as TeamError

from .api.router import api_router

app = FastAPI(title="Knowly", description="Knowly, all knowledge at one place")


### EXCEPTION HANDLERS FOR Document
@app.exception_handler(DocumentNotFound)
async def document_not_found_handler(request: Request, e: DocumentNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={ "detail": "Document not found..." }
    )

@app.exception_handler(TeamNotFound)
async def team_not_found_handler_in_docs(request: Request, e: TeamNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={ "detail": "Team not found..." }
    )

@app.exception_handler(NoDocumentsExist)
async def no_documents_exist_handler(request: Request, e: NoDocumentsExist):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={ "detail": "No files uploaded yet..." }
    )

@app.exception_handler(FileSaveError)
async def file_save_error_handler(request: Request, e: FileSaveError):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={ "detail": "Failed to save file..." }
    )
###

### EXCEPTION HANDLERS FOR User
@app.exception_handler(UserNotFound)
async def user_not_found_handler(request: Request, e: UserNotFound):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={ "detail": "User not found..." }
    )

@app.exception_handler(NoUsersExist)
async def no_users_exist_handler(request: Request, e: NoUsersExist):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={ "detail": "No users yet..." }
    )

@app.exception_handler(UserNotMemberOfTeam)
async def user_not_found_handler(request: Request, e: UserNotMemberOfTeam):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={ "detail": "User is not a member of this team..." }
    )

###

### EXCEPTION HANDLERS FOR Team
@app.exception_handler(TeamError)
async def team_not_found_handler(request: Request, e: TeamError):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={ "detail": "Team not found..." }
    )

@app.exception_handler(NoTeamsExist)
async def no_teams_exist_handler(request: Request, e: NoTeamsExist):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={ "detail": "No teams yet..." }
    )
###

### EXCEPTION HANDLERS FOR Credentials
@app.exception_handler(CredentialsError)
async def credentials_error_handler(request: Request, e: CredentialsError):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={ "detail": "Incorrect username or password!" }
    )

### EXCEPTION HANDLERS FOR Permissions
@app.exception_handler(PermissionDenied)
async def permission_denied_error(request: Request, e: PermissionDenied):
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={ "detail": "Permission Denied!" }
    )

app.include_router(api_router)
