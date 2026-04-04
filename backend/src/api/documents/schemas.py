from datetime import datetime
from pydantic import BaseModel

class DocumentResponse(BaseModel):
    id: str
    team_id: str
    filename: str
    filetype: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DocumentUpdate(BaseModel):
    name: str | None = None
    description: str | None = None
