import os
import sys
from flask import Flask, jsonify
import psycopg2

# Add project root so we can import app if it's in another file
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app import app  # your Flask app
from vercel_wsgi import handle_request

def handler(environ, start_response):
    # Wrap the Flask app for Vercel serverless
    return handle_request(app, environ, start_response)
