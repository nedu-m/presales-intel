"""Shared templates configuration with custom filters"""

from fastapi.templating import Jinja2Templates
from pathlib import Path
import markdown


# Setup templates directory
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


# Add markdown filter
def markdown_filter(text):
    """Convert markdown to HTML"""
    if not text:
        return ""
    return markdown.markdown(text, extensions=['extra', 'nl2br', 'sane_lists'])


templates.env.filters['markdown'] = markdown_filter

