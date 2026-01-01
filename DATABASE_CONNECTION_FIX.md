# Fix: "Could not translate host name" Database Connection Error

## Problem
```
could not translate host name "dpg-d5b4vire5dus73fesh1g-a" to address: Name or service not known
```

This error means the database hostname in your `DATABASE_URL` is incomplete or incorrect.

## Solution

### Step 1: Get the Correct Connection String from Render

1. Go to your Render Dashboard
2. Click on your **PostgreSQL Database** (not the web service)
3. Go to the **"Connect"** tab
4. You'll see connection strings. Make sure you're using the **complete** connection string

The hostname should look like one of these formats:
- `dpg-xxxxx-a.oregon-postgres.render.com` (External)
- `dpg-xxxxx-a.oregon-postgres.render.com:5432` (with port)
- Full format: `postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com:5432/database_name`

**Important**: The hostname must include the full domain (`.oregon-postgres.render.com` or similar), not just `dpg-xxxxx-a`.

### Step 2: Check Your DATABASE_URL Format

Your `DATABASE_URL` should be in this format:
```
postgresql://username:password@dpg-xxxxx-a.oregon-postgres.render.com:5432/database_name
```

**NOT**:
```
postgresql://username:password@dpg-xxxxx-a:5432/database_name  ❌ (missing domain)
```

### Step 3: Update Environment Variable in Render

1. Go to your **Web Service** (not the database)
2. Click **"Environment"** tab
3. Find `DATABASE_URL` variable
4. Make sure it has the **complete** connection string with full hostname
5. Click **"Save Changes"**
6. Service will automatically redeploy

### Step 4: If Using Internal Database URL

If your web service and database are in the same region, you can use the **Internal Database URL** which might be faster:

1. Go to Database → Connect tab
2. Copy the **Internal Database URL**
3. Use that in your `DATABASE_URL` environment variable

## Common Mistakes

❌ **Wrong**: `postgresql://user:pass@dpg-xxxxx-a:5432/db`
✅ **Correct**: `postgresql://user:pass@dpg-xxxxx-a.oregon-postgres.render.com:5432/db`

❌ **Wrong**: Missing `.render.com` domain
✅ **Correct**: Full hostname with domain

## Verify Connection String

You can test the connection string format:
```bash
# The hostname should resolve
ping dpg-xxxxx-a.oregon-postgres.render.com

# Or test with psql
psql postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com:5432/database_name
```

## Quick Fix Checklist

- [ ] Go to Render Dashboard → Your Database → Connect tab
- [ ] Copy the **complete** External or Internal Database URL
- [ ] Go to Your Web Service → Environment tab
- [ ] Update `DATABASE_URL` with the complete connection string
- [ ] Save and wait for redeploy
- [ ] Check logs to verify connection works

## After Fix

Once you update the connection string, your app should connect successfully. Check the logs to see:
- ✅ No more "could not translate host name" errors
- ✅ Database connection successful
- ✅ API endpoints working
