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
        
        # Check if hostname is incomplete (missing domain)
        # Render hostnames should have .render.com or similar domain
        if 'postgresql://' in db_url or 'postgres://' in db_url:
            try:
                parsed = urlparse(db_url)
                hostname = parsed.hostname
                # Check if hostname is incomplete (no dots = no domain)
                if hostname and '.' not in hostname:
                    error_msg = (
                        f"ERROR: Incomplete database hostname '{hostname}'. "
                        f"The hostname is missing the domain part. "
                        f"Expected format: 'dpg-xxxxx-a.oregon-postgres.render.com' "
                        f"or similar. Please update DATABASE_URL in Render dashboard "
                        f"with the complete connection string from your database's Connect tab."
                    )
                    print(error_msg)
                    raise ValueError(error_msg)
            except Exception as parse_error:
                # If parsing fails, continue anyway - let psycopg2 handle it
                pass
        
        # Render databases typically require SSL
        # Try with SSL first, fallback without if needed
        try:
            return psycopg2.connect(db_url, sslmode="require")
        except Exception as e:
            # Fallback: try without SSL requirement
            try:
                return psycopg2.connect(db_url)
            except Exception as e2:
                # Log detailed error for debugging
                error_msg = str(e2)
                print(f"Database connection error: {error_msg}")
                
                # Check for common issues
                if "could not translate host name" in error_msg.lower():
                    print("\n" + "="*60)
                    print("FIX REQUIRED: Incomplete database hostname detected!")
                    print("="*60)
                    print("Your DATABASE_URL has an incomplete hostname.")
                    print("Expected format: postgresql://user:pass@hostname.render.com:5432/db")
                    print("Current hostname appears to be missing the domain (.render.com)")
                    print("\nTo fix:")
                    print("1. Go to Render Dashboard → Your PostgreSQL Database")
                    print("2. Click 'Connect' tab")
                    print("3. Copy the COMPLETE External or Internal Database URL")
                    print("4. Go to Your Web Service → Environment tab")
                    print("5. Update DATABASE_URL with the complete connection string")
                    print("="*60 + "\n")
                
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

