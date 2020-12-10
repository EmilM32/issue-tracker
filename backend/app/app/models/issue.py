from typing import TYPE_CHECKING
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from app.db.base_class import Base

import datetime

if TYPE_CHECKING:
    from .project import Project


class IssuesRelations(Base):
    id = Column(Integer, primary_key=True, index=True)
    link_from = Column(Integer, ForeignKey("issue.id"), nullable=False)
    link_to = Column(Integer, ForeignKey("issue.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now())


class Issue(Base):
    id = Column(Integer, primary_key=True, index=True)
    issue_id = Column(String(12), unique=True, nullable=False)
    summary = Column(String(50), index=True)
    description = Column(String(150), index=True)
    status = Column(String(11), index=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    modified_at = Column(DateTime, default=datetime.datetime.now())
    proj_id = Column(Integer, ForeignKey("project.id"))
