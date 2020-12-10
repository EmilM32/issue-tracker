from typing import List, Union, Dict, Any

from fastapi import HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.crud.base import CRUDBase
from app.models.project import Project
from app.schemas.project import ProjectBase, ProjectDB, ProjectCreate, ProjectUpdate

import datetime


class CRUDProject(CRUDBase[Project, ProjectCreate, ProjectUpdate]):
    def create(self, db: Session, *, obj_in: ProjectBase) -> Project:
        db_obj = Project(
            proj_id=obj_in.proj_id, name=obj_in.name, description=obj_in.description
        )
        db.add(db_obj)

        try:
            db.commit()
            db.refresh(db_obj)
        except IntegrityError:
            raise HTTPException(status_code=400, detail="Project id is not unique")

        return db_obj

    def get_multi(self, db: Session) -> List[ProjectDB]:
        return db.query(self.model).all()

    def update(
        self,
        db: Session,
        *,
        db_obj: Project,
        obj_in: Union[ProjectUpdate, Dict[str, Any]]
    ) -> Project:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_data["modified_at"] = datetime.datetime.now()
        return super().update(db, db_obj=db_obj, obj_in=update_data)


project = CRUDProject(Project)
