"""
Vercel Python Serverless Function Handler
This file exports the Flask app for Vercel's serverless runtime.
"""
import sys
import os

# Add parent directory to path for imports
_current_dir = os.path.dirname(os.path.abspath(__file__))
_parent_dir = os.path.dirname(_current_dir)
if _parent_dir not in sys.path:
    sys.path.insert(0, _parent_dir)

# Import the Flask application
# This must be a clean import at module level
from app import app as flask_app

# Export as 'handler' - Vercel's @vercel/python builder expects this
handler = flask_app
