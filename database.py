import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Connect to PostgreSQL database"""
    # Try DATABASE_URL first (Render, Heroku, etc. use this format)
    db_url = os.getenv('DATABASE_URL')
    
    if db_url:
        # Fix common issues with DATABASE_URL
        # Some providers use postgres:// instead of postgresql://
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        
        # Render databases typically require SSL
        # Try with SSL first, fallback without if needed
        try:
            return psycopg2.connect(db_url, sslmode="require")
        except Exception as e:
            # Fallback: try without SSL requirement
            try:
                return psycopg2.connect(db_url)
            except Exception as e2:
                # Log the error for debugging
                print(f"Database connection error: {str(e2)}")
                print(f"Connection string format check: {'postgresql://' in db_url or 'postgres://' in db_url}")
                # If both fail, raise the original error
                raise e
    else:
        # Fallback to individual environment variables
        # Build connection string from individual variables
        host = os.getenv('DB_HOST', 'localhost')
        port = os.getenv('DB_PORT', '5432')
        database = os.getenv('DB_NAME', 'gutendex')
        user = os.getenv('DB_USER', 'postgres')
        password = os.getenv('DB_PASSWORD', '')
        
        # Render databases require SSL
        try:
            return psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
                sslmode="require"
            )
        except:
            # Fallback without SSL
            return psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password
            )

