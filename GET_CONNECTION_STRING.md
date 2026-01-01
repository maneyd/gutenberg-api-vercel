# How to Get Your Render Database Connection String

## Step-by-Step Instructions

### Step 1: Go to Render Dashboard
1. Log in to https://dashboard.render.com
2. You should see your services and databases

### Step 2: Find Your PostgreSQL Database
1. Look for a service with type **"PostgreSQL"** (not "Web Service")
2. Click on it to open the database dashboard

### Step 3: Get the Connection String
1. In the database dashboard, click on the **"Connect"** tab (or "Info" tab)
2. You'll see several connection options:
   - **Internal Database URL** - Use this if your web service is in the same region
   - **External Connection String** - Use this for connections from outside Render

### Step 4: Copy the Complete Connection String

The connection string should look like this:
```
postgresql://username:password@dpg-xxxxx-a.oregon-postgres.render.com:5432/database_name
```

**Important parts:**
- Starts with `postgresql://` or `postgres://`
- Has `username:password@`
- Has the **full hostname** with `.oregon-postgres.render.com` (or similar domain)
- Has `:5432` (port)
- Ends with `/database_name`

### Example of Correct Format:
```
postgresql://gutendex_user:abc123xyz@dpg-d5b4vire5dus73fesh1g-a.oregon-postgres.render.com:5432/gutendex_db
```

## What You Need to Do

1. **Copy the ENTIRE connection string** from Render (not just parts of it)
2. Go to your **Web Service** (not the database)
3. Click **"Environment"** tab
4. Find or create `DATABASE_URL` variable
5. Paste the **complete** connection string
6. Save and redeploy

## Common Mistakes to Avoid

❌ **Don't use**: Just the hostname part (`dpg-xxxxx-a`)
❌ **Don't use**: GitHub tokens or API keys
✅ **Do use**: The complete `postgresql://...` connection string from Render

## If You Can't Find the Connection String

1. Make sure you're looking at the **PostgreSQL Database** service (not Web Service)
2. Check the **"Connect"** or **"Info"** tab
3. Look for "Connection String", "Database URL", or "External Connection"
4. If you see individual fields (host, port, user, etc.), you can construct it:
   ```
   postgresql://USER:PASSWORD@HOST:PORT/DATABASE
   ```

## Security Note

The connection string contains your database password. Keep it secure and don't share it publicly!
