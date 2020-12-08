from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from app.api import deps
from app.schemas.issue import IssueDB, IssueUpdate
from app import crud, models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.IssueDB)
def create_issue(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.IssueBase,
) -> Any:
    """
    Create new issue.
    """

    issue = crud.issue.create(db=db, obj_in=item_in)
    issue_dict = jsonable_encoder(issue)
    issue_dict["issues_relations"] = []

    link_from = issue.id
    for link_to in item_in.issues_relations:
        relations = crud.issue_relations.create(
            db=db, link_from=link_from, link_to=link_to['id']
        )
        relation_issue = crud.issue.get(db=db, id=relations.link_to)
        issue_dict["issues_relations"].append(jsonable_encoder(relation_issue))

    return issue_dict


@router.get("/{id}", response_model=List[schemas.IssueDB])
def read_issues(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> IssueDB:
    """
    Retrieve issues for selected project.
    """

    issues = crud.issue.get_multi(db=db, proj_id=id)
    return issues


@router.put("/{id}", response_model=schemas.IssueDB)
def update_issue(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    item_in: schemas.IssueUpdate,
) -> IssueDB:
    """
    Update issue.
    """

    issue = crud.issue.get(db=db, id=id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    crud.issue_relations.remove_relations_for_issue(db=db, id_list=[issue.id])

    issue = crud.project.update(db=db, db_obj=issue, obj_in=item_in)

    issue_dict = jsonable_encoder(issue)
    if "issues_relations" not in issue_dict:
        issue_dict["issues_relations"] = []

    link_from = issue.id
    for link_to in item_in.issues_relations:
        relations = crud.issue_relations.create(
            db=db, link_from=link_from, link_to=link_to['id']
        )
        relation_issue = crud.issue.get(db=db, id=relations.link_to)
        issue_dict["issues_relations"].append(jsonable_encoder(relation_issue))

    return issue_dict


@router.delete("/{id}", response_model=schemas.IssueDB)
def delete_issue(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> IssueDB:
    """
    Delete issue.
    """

    issue = crud.issue.get(db=db, id=id)
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")

    issue_relations = crud.issue_relations.get_multi(db=db, id_list=[id])
    issue_relations_id_to_delete = [el.id for el in issue_relations]

    crud.issue_relations.remove_relations_for_issue(
        db=db, id_list=issue_relations_id_to_delete
    )

    issue = crud.issue.remove(db=db, id=id)
    return issue
