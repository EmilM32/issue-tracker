from typing import List

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.issue import IssuesRelations
from app.schemas.issue import (
    IssueRelationsCreate,
    IssueRelationsUpdate,
    IssueRelationsBase,
    IssueRelationsDB,
)

import datetime


class CRUDIssueRelations(
    CRUDBase[IssuesRelations, IssueRelationsCreate, IssueRelationsUpdate]
):
    def create(self, db: Session, *, link_from: int, link_to: int) -> IssueRelationsDB:
        db_obj = IssuesRelations(link_from=link_from, link_to=link_to)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get_multi(self, db: Session, id_list: List[int]) -> List[IssueRelationsDB]:
        return (
            db.query(self.model)
            .filter(
                (IssuesRelations.link_from.in_(id_list))
                | (IssuesRelations.link_to.in_(id_list))
            )
            .all()
        )

    def remove_relations_for_issue(
        self, db: Session, *, id_list: List[int]
    ) -> int:
        return (
            db.query(self.model)
            .filter(self.model.id.in_(id_list))
            .delete(synchronize_session=False)
        )


issue_relations = CRUDIssueRelations(IssuesRelations)
