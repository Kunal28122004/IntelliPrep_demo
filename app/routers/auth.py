"""
Authentication router - simple register & login.

Uses forms for demonstration and session-less responses.
This is intentionally minimal to keep focus on adaptive engine.
"""

from fastapi import APIRouter, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates

from ..services.auth_service import AuthService

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/register")
def register_page(request: Request):
    return templates.TemplateResponse("auth/register.html", {"request": request})


@router.post("/register")
def register(request: Request, username: str = Form(...), password: str = Form(...)):
    success, msg = AuthService.register_user(username, password)
    if success:
        # Redirect to login page after registration
        return RedirectResponse(url="/auth/login", status_code=303)
    return templates.TemplateResponse(
        "auth/register.html", {"request": request, "error": msg}
    )


@router.get("/login")
def login_page(request: Request):
    return templates.TemplateResponse("auth/login.html", {"request": request})


@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...)):
    ok, user_or_msg = AuthService.authenticate_user(username, password)
    if ok:
        # For simplicity we redirect to dashboard with ?user={username}
        return RedirectResponse(url=f"/dashboard?user={user_or_msg.username}", status_code=303)
    return templates.TemplateResponse(
        "auth/login.html", {"request": request, "error": user_or_msg}
    )