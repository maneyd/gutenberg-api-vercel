# Gutenberg Books REST API

A Flask REST API for querying Project Gutenberg books from a PostgreSQL database.

## Setup

### Prerequisites

- Python 3.8+
- PostgreSQL 12+
- pip

## Local Installation

1. **Navigate to the project directory:**
   ```bash
   cd /home/tank/Desktop/vercel
   ```

2. **Create a virtual environment:**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**

   **Create the database:**
   ```bash
   createdb gutendex
   ```

   **Restore from dump file:**
   ```bash
   psql gutendex < gutendex.dump
   ```

5. **Create and configure `.env` file:**
   ```bash
   touch .env
   ```

   Edit `.env` with your database credentials:
   ```
   DATABASE_URL=postgresql://user:password@localhost:5432/gutendex
   ```
   OR
   ```
   DB_HOST=localhost
   DB_PORT=5432
   DB_NAME=gutendex
   DB_USER=postgres
   DB_PASSWORD=your_password
   ```

6. **Run the Flask application:**
   ```bash
   python app.py
   ```
   Or with gunicorn:
   ```bash
   gunicorn app:app
   ```

   The API will be available at `http://localhost:5000`

## Deployment to Render

See [RENDER_DEPLOYMENT.md](RENDER_DEPLOYMENT.md) for detailed instructions on deploying to Render.

Quick steps:
1. Push your code to GitHub/GitLab/Bitbucket
2. Create a PostgreSQL database on Render
3. Create a new Web Service on Render
4. Set `DATABASE_URL` environment variable
5. Deploy!

## API Endpoints

- `GET /` - Homepage with search interface
- `GET /api/books` - Search books with filters
- `GET /health` - Health check endpoint
- `GET /test` - Simple test endpoint
