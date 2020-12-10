from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.project import ProjectDB, ProjectUpdate
from app.api import deps

from app import crud, models, schemas

router = APIRouter()


@router.post("/", response_model=schemas.ProjectDB)
def create_project(
    *,
    db: Session = Depends(deps.get_db),
    item_in: schemas.ProjectBase,
) -> Any:
    """
    Create new project.
    """

    project = crud.project.create(db=db, obj_in=item_in)
    return project


@router.get("/", response_model=List[schemas.ProjectDB])
def read_projects(db: Session = Depends(deps.get_db)) -> ProjectDB:
    """
    Retrieve projects.
    """

    projects = crud.project.get_multi(db=db)
    return projects


@router.get("/sorted/", response_model=List[schemas.ProjectDB])
def read_projects_sorted(
    db: Session = Depends(deps.get_db),
    is_asc: bool = False,
    is_created_at: bool = False,
) -> ProjectDB:
    """
    Retrieve sorted projects.
    """

    def sort_key(project):
        if is_created_at:
            return project.created_at
        else:
            return project.modified_at


    projects = crud.project.get_multi(db=db)
    projects.sort(key=sort_key,reverse=not is_asc)

    return projects


@router.put("/{id}", response_model=schemas.ProjectDB)
def update_project(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
    project_in: schemas.ProjectUpdate,
) -> ProjectDB:
    """
    Update project.
    """

    project = crud.project.get(db=db, id=id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    project = crud.project.update(db=db, db_obj=project, obj_in=project_in)
    return project


@router.delete("/{id}", response_model=schemas.ProjectDB)
def delete_project(
    *,
    db: Session = Depends(deps.get_db),
    id: int,
) -> ProjectDB:
    """
    Delete project.
    """

    project = crud.project.get(db=db, id=id)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")

    issues_for_project = crud.issue.get_issues_for_project(db=db, proj_id=id)

    issue_id_list = issues_for_project[2]
    issues_relations = issues_for_project[1]
    issue_relations_id_to_delete = [el.id for el in issues_relations]

    # delete all issue relations
    crud.issue_relations.remove_relations_for_issue(
        db=db, id_list=issue_relations_id_to_delete
    )
    # delete all issues
    crud.issue.remove_multi(db=db, issue_id_list=issue_id_list)

    # delete project
    project = crud.project.remove(db=db, id=id)
    return project
