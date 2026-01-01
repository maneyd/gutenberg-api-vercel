"""
Vercel Python Serverless Function Handler
"""
import sys
import os

# Add parent directory to Python path
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Import the Flask app
from app import app

# Ensure app is a proper Flask WSGI application
# Vercel's @vercel/python builder expects a Flask app instance
# Make sure we're exporting the app itself, not a wrapper
if not hasattr(app, 'wsgi_app'):
    raise RuntimeError("Exported object is not a valid Flask application")

# Export as handler - Vercel expects this name
handler = app
