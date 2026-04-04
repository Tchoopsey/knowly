from pydantic import BaseModel


class TeamCreateOrUpdate(BaseModel):
    team_lead_id: str | None = None
    team_name: str

    class Config:
        from_attributes = True

class TeamResponse(BaseModel):
    id: str
    team_lead_id: str | None = None
    team_name: str
