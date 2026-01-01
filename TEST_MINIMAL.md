# Test with Minimal Flask App

The `issubclass()` error persists. Let's test with a minimal Flask app to see if the issue is with:
1. Vercel's runtime itself
2. Our app configuration
3. Dependencies

## Step 1: Test Minimal App

I've created `api/index_minimal.py` with a bare-bones Flask app.

**To test:**
1. Temporarily rename `api/index.py` to `api/index_backup.py`
2. Rename `api/index_minimal.py` to `api/index.py`
3. Update `vercel.json` to point to the minimal handler
4. Deploy and test

If the minimal app works, the issue is in our app configuration.
If it still fails, the issue is with Vercel's runtime or our setup.

## Step 2: Check Python Version

Vercel might be using an incompatible Python version. Check:
- Vercel Dashboard → Your Project → Settings → General
- Look for Python version settings

## Step 3: Alternative Approach

If the error persists, we might need to:
1. Use a different serverless framework adapter
2. Deploy Flask differently (maybe as a regular serverless function)
3. Consider using Vercel's newer Python runtime if available

## Current Status

The error `TypeError: issubclass() arg 1 must be a class` in Vercel's internal code (`vc__handler__python.py:463`) suggests Vercel is trying to introspect the handler and getting confused.

Possible causes:
- Flask-CORS wrapping the app
- Some import or initialization issue
- Vercel runtime bug or incompatibility
- Python version mismatch
