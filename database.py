import os
import psycopg2
from urllib.parse import urlparse, urlunparse
from dotenv import load_dotenv

load_dotenv()

def get_db_connection():
    """Connect to PostgreSQL database with robust error handling"""
    # Try DATABASE_URL first (Render, Heroku, etc. use this format)
    db_url = os.getenv('DATABASE_URL')
    
    if db_url:
        # Fix common issues with DATABASE_URL
        # Some providers use postgres:// instead of postgresql://
        if db_url.startswith('postgres://'):
            db_url = db_url.replace('postgres://', 'postgresql://', 1)
        
        # Parse and validate the connection string
        try:
            parsed = urlparse(db_url)
            hostname = parsed.hostname
            
            # Check if hostname is incomplete (missing domain)
            if hostname and '.' not in hostname:
                # Try to fix incomplete Render hostnames
                # Render hostnames should have .oregon-postgres.render.com or similar
                print(f"WARNING: Incomplete hostname detected: {hostname}")
                print("Attempting to fix by appending Render domain...")
                
                # Try common Render database domains
                possible_domains = [
                    '.oregon-postgres.render.com',
                    '.frankfurt-postgres.render.com',
                    '.singapore-postgres.render.com',
                    '.postgres.render.com'
                ]
                
                fixed = False
                for domain in possible_domains:
                    try:
                        fixed_hostname = hostname + domain
                        # Reconstruct the URL with fixed hostname
                        fixed_url = urlunparse((
                            parsed.scheme,
                            f"{parsed.username}:{parsed.password}@{fixed_hostname}:{parsed.port or '5432'}",
                            parsed.path,
                            parsed.params,
                            parsed.query,
                            parsed.fragment
                        ))
                        print(f"Trying fixed hostname: {fixed_hostname}")
                        conn = psycopg2.connect(fixed_url, sslmode="require")
                        print("SUCCESS: Connection established with fixed hostname!")
                        return conn
                    except Exception as fix_error:
                        continue
                
                if not fixed:
                    # If auto-fix failed, provide clear error and try individual variables
                    print("\n" + "="*70)
                    print("ERROR: Incomplete database hostname cannot be auto-fixed")
                    print("="*70)
                    print(f"Current hostname: {hostname}")
                    print("Expected format: dpg-xxxxx-a.oregon-postgres.render.com")
                    print("\nFalling back to individual DB_* environment variables...")
                    print("="*70 + "\n")
                    # Fall through to individual variables
                    db_url = None
            else:
                # Hostname looks complete, try to connect
                try:
                    return psycopg2.connect(db_url, sslmode="require")
                except Exception as e:
                    # Try without SSL requirement
                    try:
                        return psycopg2.connect(db_url)
                    except Exception as e2:
                        print(f"Database connection failed: {str(e2)}")
                        print("Falling back to individual DB_* environment variables...")
                        db_url = None
                        
        except Exception as parse_error:
            print(f"Error parsing DATABASE_URL: {str(parse_error)}")
            print("Falling back to individual DB_* environment variables...")
            db_url = None
    
    # Fallback to individual environment variables
    host = os.getenv('DB_HOST', 'localhost')
    port = os.getenv('DB_PORT', '5432')
    database = os.getenv('DB_NAME', 'gutendex')
    user = os.getenv('DB_USER', 'postgres')
    password = os.getenv('DB_PASSWORD', '')
    
    # If we have individual variables, use them
    if host and host != 'localhost' and user and password:
        print(f"Using individual DB_* variables (host: {host})")
        try:
            return psycopg2.connect(
                host=host,
                port=port,
                database=database,
                user=user,
                password=password,
                sslmode="require"
            )
        except Exception as e:
            # Try without SSL
            try:
                return psycopg2.connect(
                    host=host,
                    port=port,
                    database=database,
                    user=user,
                    password=password
                )
            except Exception as e2:
                error_msg = (
                    f"Failed to connect using individual variables. "
                    f"Error: {str(e2)}\n\n"
                    f"Please ensure:\n"
                    f"1. DATABASE_URL has complete hostname (with .render.com domain), OR\n"
                    f"2. All DB_* variables are set correctly:\n"
                    f"   - DB_HOST (with full domain: dpg-xxxxx-a.oregon-postgres.render.com)\n"
                    f"   - DB_PORT (usually 5432)\n"
                    f"   - DB_NAME\n"
                    f"   - DB_USER\n"
                    f"   - DB_PASSWORD"
                )
                raise ValueError(error_msg)
    else:
        # No valid connection method available
        error_msg = (
            "No valid database connection configuration found.\n\n"
            "Please set either:\n"
            "1. DATABASE_URL with complete connection string (hostname must include .render.com domain), OR\n"
            "2. All of: DB_HOST, DB_PORT, DB_NAME, DB_USER, DB_PASSWORD\n\n"
            "To get the correct connection string:\n"
            "1. Go to Render Dashboard → Your PostgreSQL Database\n"
            "2. Click 'Connect' tab\n"
            "3. Copy the COMPLETE External or Internal Database URL\n"
            "4. Go to Your Web Service → Environment tab\n"
            "5. Set DATABASE_URL with the complete connection string"
        )
        raise ValueError(error_msg)
