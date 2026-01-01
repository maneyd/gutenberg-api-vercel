"""
Minimal test handler to isolate the issubclass error
"""
from flask import Flask

# Create minimal Flask app
app = Flask(__name__)

@app.route('/')
def hello():
    return {'message': 'Hello from minimal app'}

# Export handler
handler = app
