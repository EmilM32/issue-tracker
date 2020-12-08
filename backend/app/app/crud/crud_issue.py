from typing import List, Union, Dict, Any

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.issue import Issue
from app.schemas.issue import IssueBase, IssueDB, IssueCreate, IssueUpdate
from app import crud

import datetime


class CRUDIssue(CRUDBase[Issue, IssueCreate, IssueUpdate]):
    def create(self, db: Session, *, obj_in: Union[IssueBase, Dict[str, Any]]) -> Issue:

        if isinstance(obj_in, dict):
            create_item = obj_in
        else:
            create_item = obj_in.dict(exclude_unset=True)

        all_issue = (
            db.query(self.model.issue_id)
            .filter(Issue.proj_id == create_item["proj_id"])
            .all()
        )

        issue_counter_list = []
        for issue in all_issue:
            counter = issue[0].split("-")[1]
            issue_counter_list.append(counter)

        next_issue_id = int(max(issue_counter_list)) + 1 if issue_counter_list else 1
        create_item["issue_id"] = f"{create_item['issue_id']}-{next_issue_id}"

        db_obj = Issue(
            proj_id=create_item["proj_id"],
            issue_id=create_item["issue_id"],
            description=create_item["description"],
            summary=create_item["summary"],
            status=create_item["status"],
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)

        return db_obj

    def get_issues_for_project(self, db: Session, proj_id: int) -> List[IssueDB]:
        issues = db.query(self.model).filter(Issue.proj_id == proj_id).all()
        issue_id_list = [el.id for el in issues]
        issues_relations = crud.issue_relations.get_multi(db=db, id_list=issue_id_list)

        return issues, issues_relations, issue_id_list

    def get_multi(self, db: Session, proj_id: int) -> List[IssueDB]:
        issues_tuple = self.get_issues_for_project(db=db, proj_id=proj_id)
        issues = issues_tuple[0]
        issues_relations = issues_tuple[1]

        issues_relations_dict = {el.link_from: [] for el in issues_relations}

        for issues_relation in issues_relations:
            issues_relations_dict[issues_relation.link_from].append(issues_relation)

        for issue in issues:
            if issue.id in issues_relations_dict:
                issue.issues_relations = issues_relations_dict[issue.id]

        return issues

    def update(
        self, db: Session, *, db_obj: Issue, obj_in: Union[IssueUpdate, Dict[str, Any]]
    ) -> Issue:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)

        update_data["modified_at"] = datetime.datetime.now()
        return super().update(db, db_obj=db_obj, obj_in=update_data)

    def remove_multi(self, db: Session, issue_id_list: int) -> int:
        return (
            db.query(self.model)
            .filter(self.model.id.in_(issue_id_list))
            .delete(synchronize_session=False)
        )


issue = CRUDIssue(Issue)
