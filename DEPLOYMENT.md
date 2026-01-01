# Vercel Deployment Guide

This guide will walk you through deploying your Flask application to Vercel.

## Prerequisites

1. A Vercel account (sign up at https://vercel.com)
2. Vercel CLI installed (optional, for CLI deployment)
3. A PostgreSQL database (you can use Vercel Postgres, Neon, Supabase, or any other PostgreSQL service)

## Step 1: Install Vercel CLI (Optional but Recommended)

```bash
npm install -g vercel
```

Or use npx without installing:
```bash
npx vercel
```

## Step 2: Set Up Your Database

Since Vercel doesn't provide a built-in PostgreSQL database, you'll need to set up an external database:

### Option A: Vercel Postgres (Recommended)
1. Go to your Vercel dashboard
2. Navigate to your project → Storage → Create Database → Postgres
3. Copy the connection string

### Option B: External Database Services
- **Neon** (https://neon.tech) - Free tier available
- **Supabase** (https://supabase.com) - Free tier available
- **Railway** (https://railway.app) - Free tier available
- **Any PostgreSQL database** you have access to

### Import Your Database

Once you have a database, you'll need to import your data:

```bash
# If you have the database dump file
psql <your_connection_string> < gutendex.dump
```

Or restore using the connection string:
```bash
PGPASSWORD=your_password psql -h your_host -U your_user -d your_database -f gutendex.dump
```

## Step 3: Configure Environment Variables

You'll need to set the following environment variables in Vercel:

1. **DB_HOST** - Your PostgreSQL host
2. **DB_PORT** - Your PostgreSQL port (usually 5432)
3. **DB_NAME** - Your database name
4. **DB_USER** - Your database user
5. **DB_PASSWORD** - Your database password

### Setting Environment Variables in Vercel:

#### Via Vercel Dashboard:
1. Go to your project on Vercel
2. Navigate to Settings → Environment Variables
3. Add each variable:
   - `DB_HOST`
   - `DB_PORT`
   - `DB_NAME`
   - `DB_USER`
   - `DB_PASSWORD`

#### Via Vercel CLI:
```bash
vercel env add DB_HOST
vercel env add DB_PORT
vercel env add DB_NAME
vercel env add DB_USER
vercel env add DB_PASSWORD
```

## Step 4: Deploy to Vercel

### Option A: Deploy via Vercel Dashboard

1. **Push your code to GitHub/GitLab/Bitbucket:**
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin <your-repo-url>
   git push -u origin main
   ```

2. **Import project in Vercel:**
   - Go to https://vercel.com/new
   - Import your Git repository
   - Vercel will automatically detect the Python project
   - Add environment variables (if not done already)
   - Click "Deploy"

### Option B: Deploy via Vercel CLI

1. **Login to Vercel:**
   ```bash
   vercel login
   ```

2. **Deploy:**
   ```bash
   vercel
   ```

3. **For production deployment:**
   ```bash
   vercel --prod
   ```

## Step 5: Verify Deployment

After deployment, Vercel will provide you with a URL like:
- `https://your-project-name.vercel.app`

Test your endpoints:
- Homepage: `https://your-project-name.vercel.app/`
- API: `https://your-project-name.vercel.app/api/books`

## Troubleshooting

### Common Issues:

1. **Database Connection Errors:**
   - Verify all environment variables are set correctly
   - Check that your database allows connections from Vercel's IP addresses
   - Ensure SSL is enabled if required by your database provider

2. **Module Not Found Errors:**
   - Ensure all dependencies are in `requirements.txt`
   - Check that Python version is compatible (Vercel uses Python 3.9 by default)

3. **Static Files Not Loading:**
   - Verify the `vercel.json` routes configuration
   - Check that static files are in the `static/` directory

4. **Function Timeout:**
   - Vercel has execution time limits (10s for Hobby, 60s for Pro)
   - Optimize database queries if needed

### Viewing Logs:

```bash
vercel logs
```

Or view logs in the Vercel dashboard under your deployment → Functions → Logs

## Project Structure

```
vercel/
├── api/
│   └── index.py          # Vercel serverless function entry point
├── static/               # Static files (CSS, JS)
├── templates/            # HTML templates
├── app.py               # Flask application
├── database.py          # Database connection
├── vercel.json          # Vercel configuration
├── requirements.txt     # Python dependencies
└── .vercelignore        # Files to ignore during deployment
```

## Additional Notes

- Vercel automatically handles Python dependencies from `requirements.txt`
- The `api/index.py` file serves as the entry point for serverless functions
- Static files are served directly by Vercel
- Database connections should use connection pooling for better performance
- Consider using Vercel's Edge Functions for better performance if needed

## Next Steps

After successful deployment:
1. Set up a custom domain (optional)
2. Configure automatic deployments from your Git repository
3. Set up monitoring and alerts
4. Consider implementing caching for better performance
