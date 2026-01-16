"""
HTML flows for starting tests, viewing questions, and completion.
"""

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ..services.session_service import SessionService
from ..services.attempt_service import AttemptService
from ..db import SessionLocal, User, Question

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/start")
def start_test(request: Request, user: str = None):
    """
    Start a new test session for a user.
    For diagnostic test we will use baseline generator via API endpoints.
    """
    if not user:
        return RedirectResponse(url="/auth/login")
    # Create a session id (simple integer) and redirect to first question
    session_id = SessionService.create_session(user)
    # Include the username in the redirect query string so the question page's JS can pick it up.
    return RedirectResponse(url=f"/test/question/{session_id}?user={user}", status_code=303)


@router.get("/question/{session_id}")
def show_question(request: Request, session_id: int):
    """
    Renders question page which will fetch the actual question content via API.
    The template uses simple JS or form to post answers.
    """
    return templates.TemplateResponse(
        "test/question.html", {"request": request, "session_id": session_id}
    )


@router.get("/complete/{session_id}")
def complete(request: Request, session_id: int):
    """
    Show a simple completion page with session summary.
    """
    summary = SessionService.end_session(session_id)
    return templates.TemplateResponse(
        "test/complete.html", {"request": request, "summary": summary}
    )