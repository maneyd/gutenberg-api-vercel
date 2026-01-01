# Fix: "gunicorn: command not found" on Render

## Problem
Render shows error: `bash: line 1: gunicorn: command not found`

## Solution

The issue is that `gunicorn` needs to be called using Python's module syntax on Render.

### Update Your Start Command

In your Render dashboard:
1. Go to your Web Service
2. Click "Settings"
3. Scroll to "Start Command"
4. Change from: `gunicorn app:app`
5. Change to: `python -m gunicorn app:app`
6. Click "Save Changes"
7. Render will automatically redeploy

### Alternative: Update Files

I've already updated these files for you:
- ✅ `Procfile` - Changed to `python -m gunicorn app:app`
- ✅ `render.yaml` - Changed to `python -m gunicorn app:app`

If you're using these files, just commit and push:
```bash
git add Procfile render.yaml
git commit -m "Fix gunicorn command for Render"
git push
```

Render will automatically redeploy with the fix.

## Why This Happens

On Render, sometimes the `gunicorn` executable isn't in the PATH, but using `python -m gunicorn` ensures Python finds it in the installed packages.

## Verify It Works

After redeploying, check the logs:
- Should see: `[INFO] Starting gunicorn...`
- Should see: `[INFO] Listening at: http://0.0.0.0:XXXX`
- No more "command not found" errors

Your app should now start successfully! 🎉
