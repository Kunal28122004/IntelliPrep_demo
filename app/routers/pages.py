"""
Static pages and dashboard.

Dashboard shows simple user stats and link to start test.
"""

from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates
from typing import Optional

from ..services.skill_service import SkillService
from ..services.attempt_service import AttemptService
from ..db import SessionLocal
from ..db import User

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", include_in_schema=False)
def root(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@router.get("/dashboard")
def dashboard(request: Request, user: Optional[str] = None):
    """
    Simple dashboard using query parameter 'user' for demonstration.
    In production, use secure sessions / tokens.
    """
    stats = {}
    user_obj = None
    if user:
        db = SessionLocal()
        try:
            user_obj = db.query(User).filter(User.username == user).first()
            if user_obj:
                attempts = AttemptService.get_attempts_by_user(user_obj.id)
                stats = SkillService.compute_overall_stats(attempts)
        finally:
            db.close()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user_obj, "stats": stats},
    )