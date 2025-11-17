"""
WSGI entry point for PythonAnywhere deployment.
This wraps the FastAPI ASGI app for PythonAnywhere's WSGI server.
"""
import sys
import os

# Add the project directory to Python path
path = '/home/yourusername/presales-intel'  # Update with your PythonAnywhere username
if path not in sys.path:
    sys.path.insert(0, path)

# Set environment variables if needed
os.environ.setdefault('PYTHONUNBUFFERED', '1')

# Import the FastAPI app
from app.main import app

# PythonAnywhere uses WSGI, so we need to wrap the ASGI app
from asgiref.wsgi import WsgiToAsgi

application = WsgiToAsgi(app)

