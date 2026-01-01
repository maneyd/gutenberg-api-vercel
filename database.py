import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Connect to PostgreSQL database"""
    # Try DATABASE_URL first (Render, Heroku, etc. use this format)
    db_url = os.getenv('DATABASE_URL')
    
    if db_url:
        # Fix postgres:// to postgresql:// if needed
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        
        # Connect with SSL (required for Render databases)
        try:
            return psycopg2.connect(db_url, sslmode="require")
        except Exception:
            # Fallback without SSL requirement
            return psycopg2.connect(db_url)
    else:
        # Fallback to individual environment variables
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        database = os.getenv('DB_NAME', 'gutendex')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', '')
        
        try:
            return psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
                sslmode="require"
            )
        except Exception:
            # Fallback without SSL
            return psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )
