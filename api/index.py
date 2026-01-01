import sys
import os

# Add parent directory to path so we can import app
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# Change to parent directory to ensure relative imports work
os.chdir(parent_dir)

try:
    from app import app
    
    # Export the Flask app for Vercel
    # Vercel's Python runtime expects the app to be available as 'handler'
    handler = app
except Exception as e:
    # If there's an import error, create a minimal error handler
    from flask import Flask, jsonify
    error_app = Flask(__name__)
    
    @error_app.route('/', defaults={'path': ''})
    @error_app.route('/<path:path>')
    def error_handler(path):
        return jsonify({
            'error': 'Application failed to load',
            'message': str(e)
        }), 500
    
    handler = error_app
