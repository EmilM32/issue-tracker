from typing import Optional, List, Any
from pydantic import BaseModel
from datetime import datetime


class IssueRelationsBase(BaseModel):
    link_from: int
    link_to: int


# Properties shared by models stored in DB
class IssueRelationsDBBase(IssueRelationsBase):
    id: int
    created_at: datetime

    class Config:
        orm_mode = True


class IssueBase(BaseModel):
    issue_id: Optional[str]
    summary: str
    description: str
    status: str
    proj_id: int
    issues_relations: Optional[List[Any]] = []


class IssueCreate(IssueBase):
    created_at: datetime
    modified_at: datetime


class IssueRelationsCreate(IssueRelationsBase):
    created_at: datetime


class IssueUpdate(IssueBase):
    summary: str
    description: str
    status: str


class IssueRelationsUpdate(IssueRelationsBase):
    pass


# Properties shared by models stored in DB
class IssueInDBBase(IssueBase):
    id: int
    created_at: datetime
    modified_at: datetime

    class Config:
        orm_mode = True


# Properties to return to client
class IssueDB(IssueInDBBase):
    pass


# Properties to return to client
class IssueRelationsDB(IssueRelationsDBBase):
    pass