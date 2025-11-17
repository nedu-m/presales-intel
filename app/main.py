from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import os
from pathlib import Path

from app.routers import briefs
from app.database import engine, Base
from app.templates_config import templates

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PrepCall", version="0.1.0")

# Setup static files
BASE_DIR = Path(__file__).resolve().parent
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Include routers
app.include_router(briefs.router)


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Landing page with form to generate brief"""
    return templates.TemplateResponse(
        "index.html",
        {"request": request}
    )


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}

