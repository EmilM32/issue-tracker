from pydantic import BaseModel
from datetime import datetime


class ProjectBase(BaseModel):
    proj_id: str
    name: str
    description: str


class ProjectCreate(ProjectBase):
    created_at: datetime
    modified_at: datetime


class ProjectUpdate(ProjectBase):
    name: str
    description: str

# Properties shared by models stored in DB
class ProjectInDBBase(ProjectBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class ProjectDB(ProjectInDBBase):
    pass