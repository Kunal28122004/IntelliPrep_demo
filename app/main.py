"""
FastAPI application initialization for IntelliPrep.

- Creates DB tables on startup.
- Loads ML model for inference.
- Includes routers and serves static files & templates.
"""

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from .db import init_db
from .test_engine.model_loader import ModelLoader

# Routers
from .routers import auth as auth_router
from .routers import pages as pages_router
from .routers import test_api as test_api_router
from .routers import test_pages as test_pages_router

app = FastAPI(title="IntelliPrep - Adaptive Assessment")

# Mount static directory
app.mount("/static", StaticFiles(directory="app/static"), name="static")

templates = Jinja2Templates(directory="app/templates")


@app.on_event("startup")
def startup_event():
    # Initialize DB and question bank
    init_db()
    # Ensure ML model is ready for inference
    ModelLoader.load_model()  # loads or creates a lightweight inference model


# Include routers
app.include_router(auth_router.router, prefix="/auth")
app.include_router(pages_router.router, prefix="")
app.include_router(test_pages_router.router, prefix="/test")
app.include_router(test_api_router.router, prefix="/api")