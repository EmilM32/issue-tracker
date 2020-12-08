from fastapi import APIRouter

from app.api.endpoints import projects, issues

api_router = APIRouter()

api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(issues.router, prefix="/issues", tags=["issues"])
