import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Connect to PostgreSQL database"""
    # Try DATABASE_URL first (common in Vercel Postgres, Neon, etc.)
    db_url = os.getenv('DATABASE_URL')
    
    if db_url:
        # Parse the URL and connect with SSL if needed
        try:
            # For services like Neon, Supabase that require SSL
            return psycopg2.connect(db_url, sslmode="require")
        except:
            # Fallback without SSL requirement
            return psycopg2.connect(db_url)
    else:
        # Fallback to individual environment variables
        return psycopg2.connect(
            host=os.getenv('DB_HOST', 'localhost'),
            port=os.getenv('DB_PORT', '5432'),
            database=os.getenv('DB_NAME', 'gutendex'),
            user=os.getenv('DB_USER', 'postgres'),
            password=os.getenv('DB_PASSWORD', '')
        )

