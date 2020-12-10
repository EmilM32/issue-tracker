from sqlalchemy import Column, Integer, String, DateTime

from app.db.base_class import Base

import datetime


class Project(Base):
    id = Column(Integer, primary_key=True, index=True)
    proj_id = Column(String(8), unique=True, nullable=False)
    name = Column(String(15), index=True)
    description = Column(String(150), index=True)
    created_at = Column(DateTime, default=datetime.datetime.now())
    modified_at = Column(DateTime, default=datetime.datetime.now())