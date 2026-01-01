# Troubleshooting: "Serverless Function has crashed" Error

## Quick Fixes

### 1. Check Vercel Logs First
The most important step is to see the actual error:
1. Go to your Vercel dashboard
2. Click on your project
3. Go to the "Deployments" tab
4. Click on the failed deployment
5. Click on "Functions" → "Logs"
6. Look for the actual error message

### 2. Common Causes and Solutions

#### Missing Environment Variables
**Error**: `KeyError: 'DATABASE_URL'` or database connection errors

**Solution**: 
- Set `DATABASE_URL` in Vercel environment variables, OR
- Set all of these: `DB_HOST`, `DB_PORT`, `DB_NAME`, `DB_USER`, `DB_PASSWORD`

**How to set:**
1. Vercel Dashboard → Your Project → Settings → Environment Variables
2. Add the variable(s)
3. Redeploy (or wait for automatic redeploy)

#### Import Errors
**Error**: `ModuleNotFoundError` or `ImportError`

**Solution**:
- Verify all packages are in `requirements.txt`
- Check that package names are correct (case-sensitive)
- Remove `gunicorn` from requirements.txt if present (not needed for Vercel)

#### Database Connection Issues
**Error**: Connection timeout or SSL errors

**Solution**:
- Ensure your database allows connections from anywhere (0.0.0.0/0)
- For Neon/Supabase: They provide connection strings with SSL - use `DATABASE_URL`
- Check firewall settings on your database

#### Path/Import Issues
**Error**: `No module named 'app'` or similar

**Solution**:
- The `api/index.py` file should handle this automatically
- Make sure your project structure matches:
  ```
  vercel/
  ├── api/
  │   └── index.py
  ├── app.py
  ├── database.py
  └── ...
  ```

### 3. Test Locally with Vercel

Before deploying, test locally:
```bash
# Install Vercel CLI
npm install -g vercel

# Run local development server
vercel dev
```

This will simulate the Vercel environment locally and help catch errors.

### 4. Verify Your Setup

Check these files exist and are correct:
- ✅ `vercel.json` - Vercel configuration
- ✅ `api/index.py` - Serverless function entry point
- ✅ `requirements.txt` - All dependencies listed
- ✅ Environment variables set in Vercel

### 5. Database Setup for Vercel Postgres

If using Vercel Postgres:
1. Go to your project → Storage → Create Database → Postgres
2. After creation, go to Settings → Environment Variables
3. You'll see `POSTGRES_URL` automatically added
4. **Important**: Also add it as `DATABASE_URL`:
   - Variable name: `DATABASE_URL`
   - Value: (copy the value from `POSTGRES_URL`)
   - This is what the code expects

### 6. Still Not Working?

1. **Check the exact error in logs** (most important!)
2. **Verify environment variables are set for Production, Preview, AND Development**
3. **Try a minimal test**: Create a simple Flask app to test if Vercel works at all
4. **Check Vercel status**: https://vercel-status.com

## Getting Help

If you're still stuck:
1. Copy the exact error from Vercel logs
2. Share your `vercel.json` and `api/index.py` files
3. Check Vercel community forums: https://github.com/vercel/vercel/discussions
