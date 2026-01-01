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
        # Render databases typically require SSL
        # Try with SSL first, fallback without if needed
        try:
            return psycopg2.connect(db_url, sslmode="require")
        except Exception as e:
            # Fallback: try without SSL requirement
            try:
                return psycopg2.connect(db_url)
            except:
                # If both fail, raise the original error
                raise e
    else:
        # Fallback to individual environment variables
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'gutendex'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )

