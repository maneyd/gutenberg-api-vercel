import sys
import os
from app import app  # Import your Flask app

# Add project root if needed
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Vercel expects a WSGI callable
def handler(environ, start_response):
    return app(environ, start_response)
