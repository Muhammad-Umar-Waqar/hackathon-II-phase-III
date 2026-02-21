"""
Script to run Better Auth database migrations
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def run_migration():
    """Run the Better Auth schema migration"""
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print("ERROR: DATABASE_URL not found in environment variables")
        return False

    try:
        # Read the SQL file
        with open('migrations/better-auth-schema.sql', 'r') as f:
            sql = f.read()

        # Connect to database
        print("Connecting to database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Execute migration
        print("Running Better Auth schema migration...")
        cursor.execute(sql)
        conn.commit()

        print("SUCCESS: Migration completed successfully!")

        # Close connection
        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"ERROR: Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Better Auth Database Migration")
    print("=" * 50)
    run_migration()
