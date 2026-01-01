# Setting Environment Variables in Render (NOT .env file!)

## Important: .env Files Don't Work on Render!

⚠️ **The `.env` file is ONLY for local development. Render does NOT read `.env` files.**

You **MUST** set environment variables in the Render Dashboard for them to work in production.

## Step-by-Step: Set DATABASE_URL in Render

### Step 1: Get Your Complete Render Database Connection String

1. Go to **https://dashboard.render.com**
2. Click on your **PostgreSQL Database** (not the web service)
3. Click the **"Connect"** tab
4. You'll see connection strings. Copy the **COMPLETE** one:

**Look for:**
- **External Database URL** (for connections from outside Render)
- **Internal Database URL** (if your web service is in the same region)

**The connection string should look like:**
```
postgresql://username:password@dpg-d5b4vire5dus73fesh1g-a.oregon-postgres.render.com:5432/database_name
```

**IMPORTANT:** The hostname MUST include the full domain:
- ✅ Correct: `dpg-d5b4vire5dus73fesh1g-a.oregon-postgres.render.com`
- ❌ Wrong: `dpg-d5b4vire5dus73fesh1g-a` (missing domain)

### Step 2: Set DATABASE_URL in Your Web Service

1. Go to your **Web Service** dashboard (e.g., `gutenberg-api-vercel`)
2. Click the **"Environment"** tab (in the left sidebar)
3. Scroll down to **"Environment Variables"** section
4. Look for `DATABASE_URL`:
   - If it exists: Click **"Edit"** or the pencil icon
   - If it doesn't exist: Click **"Add Environment Variable"**

5. **Set the variable:**
   - **Key**: `DATABASE_URL`
   - **Value**: Paste the **COMPLETE** connection string from Step 1
   - Make sure it includes the full hostname with `.oregon-postgres.render.com` (or similar)

6. Click **"Save Changes"**
7. Render will automatically redeploy your service

### Step 3: Verify It's Set Correctly

After redeploying:
1. Go to your service → **"Logs"** tab
2. Look for the connection attempt
3. Visit `/health` endpoint to see diagnostic info
4. The error should be gone!

## Alternative: Use Individual Variables

If you prefer, you can set individual variables instead of `DATABASE_URL`:

1. In your Web Service → Environment tab
2. Add these variables:
   - `DB_HOST` = `dpg-d5b4vire5dus73fesh1g-a.oregon-postgres.render.com` (with full domain!)
   - `DB_PORT` = `5432`
   - `DB_NAME` = your database name
   - `DB_USER` = your database username
   - `DB_PASSWORD` = your database password

The code will automatically use these if `DATABASE_URL` is not set.

## Common Mistakes

❌ **Mistake 1**: Only setting it in `.env` file
- ✅ **Fix**: Set it in Render Dashboard → Environment tab

❌ **Mistake 2**: Incomplete hostname (missing domain)
- ✅ **Fix**: Use the complete connection string from Render's Connect tab

❌ **Mistake 3**: Using connection string from a different service (Neon, etc.)
- ✅ **Fix**: Use the connection string from YOUR Render database

## Quick Checklist

- [ ] Go to Render Dashboard → Your PostgreSQL Database
- [ ] Click "Connect" tab
- [ ] Copy the COMPLETE External or Internal Database URL
- [ ] Go to Your Web Service → Environment tab
- [ ] Add/Edit `DATABASE_URL` variable
- [ ] Paste the COMPLETE connection string (with full hostname)
- [ ] Save changes
- [ ] Wait for redeploy
- [ ] Check logs to verify connection works

## Why .env Doesn't Work on Render

- `.env` files are for **local development only**
- Render runs your code in a **serverless/container environment**
- Environment variables must be set in **Render's dashboard**
- This is a security feature - secrets shouldn't be in code files

## After Setting in Render

Once you set `DATABASE_URL` in Render dashboard:
- ✅ It will be available to your app at runtime
- ✅ It will persist across deployments
- ✅ It's secure (not in your code repository)
- ✅ You can update it anytime in the dashboard

Your `.env` file is fine for local development, but for Render, you MUST set it in the dashboard!
