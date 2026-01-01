# Deploying to Render

This guide will walk you through deploying your Flask application to Render.

## Prerequisites

1. A Render account (sign up at https://render.com)
2. Your code pushed to GitHub/GitLab/Bitbucket
3. A PostgreSQL database (you can create one on Render)

## Step 1: Set Up PostgreSQL Database on Render

1. **Create a PostgreSQL Database:**
   - Go to your Render dashboard
   - Click "New +" → "PostgreSQL"
   - Choose a name (e.g., "gutendex-db")
   - Select a plan (Free tier available)
   - Click "Create Database"

2. **Get Connection Details:**
   - After creation, go to your database dashboard
   - You'll see:
     - **Internal Database URL** (for services in the same region)
     - **External Connection String** (for external connections)
   - Copy the connection string - it looks like:
     ```
     postgresql://user:password@hostname:5432/database_name
     ```

3. **Import Your Database:**
   - Go to your database dashboard → "Connect" tab
   - Use the "psql" command or "Connection Pooling" URL
   - Import your database dump:
     ```bash
     psql <connection_string> < gutendex.dump
     ```
   - Or use Render's Shell feature to run the import

## Step 2: Deploy Your Web Service

### Option A: Deploy via Render Dashboard (Recommended)

1. **Connect Your Repository:**
   - Go to Render dashboard
   - Click "New +" → "Web Service"
   - Connect your GitHub/GitLab/Bitbucket repository
   - Select your repository

2. **Configure Your Service:**
   - **Name**: Choose a name (e.g., "gutenberg-books-api")
   - **Environment**: Python 3
   - **Python Version**: Set to **3.12.0** (important: psycopg2-binary doesn't support Python 3.13 yet)
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python -m gunicorn app:app`
   - **Plan**: Choose Free or Starter plan

3. **Set Environment Variables:**
   - Go to "Environment" tab
   - Add your database connection:
     - **Option 1**: Add `DATABASE_URL` with your full connection string
     - **Option 2**: Add individual variables:
       - `DB_HOST` - Your database host
       - `DB_PORT` - Usually `5432`
       - `DB_NAME` - Your database name
       - `DB_USER` - Your database user
       - `DB_PASSWORD` - Your database password

4. **Link to Database (Optional but Recommended):**
   - In the "Environment" tab, find "Link Database"
   - Select your PostgreSQL database
   - Render will automatically add `DATABASE_URL` environment variable

5. **Deploy:**
   - Click "Create Web Service"
   - Render will automatically build and deploy your app

### Option B: Deploy via render.yaml

If you have a `render.yaml` file (already created), you can:

1. Go to Render dashboard
2. Click "New +" → "Blueprint"
3. Connect your repository
4. Render will automatically detect `render.yaml` and create services

## Step 3: Verify Deployment

After deployment, Render will provide you with a URL like:
- `https://your-service-name.onrender.com`

Test your endpoints:
- Homepage: `https://your-service-name.onrender.com/`
- Health check: `https://your-service-name.onrender.com/health`
- API: `https://your-service-name.onrender.com/api/books`

## Step 4: Configure Custom Domain (Optional)

1. Go to your service dashboard
2. Click "Settings" → "Custom Domain"
3. Add your domain name
4. Follow DNS configuration instructions

## Environment Variables

### Required Variables:

- **DATABASE_URL** (recommended) - Full PostgreSQL connection string
  OR
- **DB_HOST**, **DB_PORT**, **DB_NAME**, **DB_USER**, **DB_PASSWORD** - Individual database credentials

### How to Set:

1. Go to your service dashboard
2. Click "Environment" tab
3. Add variables:
   - Key: `DATABASE_URL`
   - Value: `postgresql://user:password@host:port/database`
4. Click "Save Changes"
5. Service will automatically redeploy

## Project Structure

```
vercel/
├── app.py              # Flask application
├── database.py          # Database connection
├── requirements.txt     # Python dependencies
├── Procfile            # Process file (gunicorn command)
├── render.yaml         # Render configuration (optional)
├── static/             # Static files (CSS, JS)
└── templates/          # HTML templates
```

## Troubleshooting

### Common Issues:

1. **Database Connection Errors:**
   - Verify `DATABASE_URL` is set correctly
   - Check that your database allows connections
   - Ensure you're using the correct connection string format
   - For Render databases, use the "Internal Database URL" if service is in same region

2. **Build Failures / Python Version Issues:**
   - **Python 3.13 Error**: If you see `undefined symbol: _PyInterpreterState_Get`, use Python 3.12.0
   - Set Python version to 3.12.0 in Render settings or use `runtime.txt` file
   - Check that all dependencies are in `requirements.txt`
   - Verify Python version compatibility (psycopg2-binary requires Python ≤ 3.12)
   - Check build logs in Render dashboard

3. **Application Crashes / "gunicorn: command not found":**
   - Use `python -m gunicorn app:app` as the start command instead of just `gunicorn app:app`
   - Ensure `gunicorn` is in `requirements.txt`
   - Check logs in Render dashboard → "Logs" tab
   - Verify all environment variables are set

4. **Static Files Not Loading:**
   - Verify `static/` directory structure
   - Check Flask app configuration for static folder path

### Viewing Logs:

1. Go to your service dashboard
2. Click "Logs" tab
3. View real-time logs and errors

## Render Features

- **Auto-Deploy**: Automatically deploys on git push (if enabled)
- **Health Checks**: Render monitors your service health
- **SSL**: Automatic HTTPS for all services
- **Scaling**: Easy to scale up/down based on traffic
- **Database Backups**: Automatic backups for paid plans

## Next Steps

After successful deployment:
1. Set up automatic deployments from your Git repository
2. Configure custom domain (if needed)
3. Set up monitoring and alerts
4. Consider upgrading plan for better performance

## Support

- Render Documentation: https://render.com/docs
- Render Community: https://community.render.com
- Support: support@render.com
