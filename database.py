import os
import psycopg2
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv()

def get_db_connection():
    db_url = os.environ["DATABASE_URL"]  # must exist in Vercel env vars

    # Neon requires SSL
    return psycopg2.connect(db_url, sslmode="require")

