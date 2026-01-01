import sys
import os
import traceback

# Get the project root directory (parent of api/)
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add project root to Python path
if project_root not in sys.path:
    sys.path.insert(0, project_root)

# Set working directory to project root for template/static file resolution
# But do it safely without breaking if it fails
try:
    original_cwd = os.getcwd()
    os.chdir(project_root)
except:
    pass  # If chdir fails, continue anyway

try:
    # Import Flask app from project root
    from app import app
    
    # Vercel expects the Flask app to be available as 'handler'
    # The @vercel/python builder automatically wraps it for WSGI
    handler = app
    
    # Log successful import (visible in Vercel logs)
    print("✓ Flask app imported successfully")
    
except Exception as e:
    # If import fails, create a minimal error handler
    error_msg = str(e)
    error_trace = traceback.format_exc()
    
    print(f"✗ CRITICAL: Failed to import Flask app")
    print(f"Error: {error_msg}")
    print(f"Traceback:\n{error_trace}")
    
    try:
        from flask import Flask, jsonify
        error_app = Flask(__name__)
        
        @error_app.route('/', defaults={'path': ''})
        @error_app.route('/<path:path>')
        def error_handler(path):
            return jsonify({
                'error': 'Application failed to load',
                'message': error_msg,
                'traceback': error_trace,
                'path': path
            }), 500
        
        handler = error_app
        print("✓ Error handler Flask app created")
    except Exception as e2:
        # If even Flask import fails, we're in deep trouble
        print(f"✗✗ CRITICAL: Cannot even import Flask: {str(e2)}")
        # Return None - Vercel will show an error, but at least we logged it
        handler = None
