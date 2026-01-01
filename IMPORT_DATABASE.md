# Import Database to Render

## Step 1: Get Your Render Database Connection String

1. Go to your Render dashboard
2. Click on your PostgreSQL database
3. Go to the "Connect" tab
4. Copy the **External Connection String** (or Internal if you're on Render's network)
   - It looks like: `postgresql://user:password@hostname:5432/database_name`

## Step 2: Import the Database Dump

### Option A: Using psql directly (Recommended)

From your terminal, run:

```bash
# Navigate to your project directory
cd /home/tank/Desktop/vercel

# Import the dump file
psql <YOUR_RENDER_DATABASE_URL> < gutendex.dump
```

**Example:**
```bash
psql postgresql://user:password@dpg-xxxxx-a.oregon-postgres.render.com:5432/gutendex_db < gutendex.dump
```

### Option B: Using pg_restore (if dump is in custom format)

If the dump is in custom format, use:
```bash
pg_restore -d <YOUR_RENDER_DATABASE_URL> gutendex.dump
```

### Option C: Using environment variable

You can also set the connection string as an environment variable:

```bash
export DATABASE_URL="postgresql://user:password@hostname:5432/database_name"
psql $DATABASE_URL < gutendex.dump
```

## Step 3: Verify the Import

After importing, verify the data:

```bash
# Connect to your database
psql <YOUR_RENDER_DATABASE_URL>

# Check if tables exist
\dt

# Check a sample table
SELECT COUNT(*) FROM books_book;

# Exit
\q
```

## Troubleshooting

### If you get "connection refused" or timeout:
- Make sure you're using the **External Connection String** (not Internal)
- Check that your IP is allowed (Render databases allow all IPs by default on free tier)
- Verify the connection string is correct

### If you get "permission denied":
- Make sure you're using the correct user credentials from Render
- Check that the database name matches

### If the import is slow:
- The dump file is 42MB, so it may take a few minutes
- Be patient and let it complete

### If you get "database does not exist":
- The database should be created automatically by Render
- Check the database name in your connection string

## Quick Command Reference

```bash
# 1. Get your connection string from Render dashboard
# 2. Replace <YOUR_CONNECTION_STRING> with actual connection string

# Import database
psql <YOUR_CONNECTION_STRING> < gutendex.dump

# Verify (optional)
psql <YOUR_CONNECTION_STRING> -c "\dt"
psql <YOUR_CONNECTION_STRING> -c "SELECT COUNT(*) FROM books_book;"
```

## After Import

Once the database is imported:
1. Go to your Render Web Service
2. Set the `DATABASE_URL` environment variable to the same connection string
3. Your Flask app should now be able to connect to the database!
