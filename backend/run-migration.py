"""
Script to migrate tasks table user_id from INTEGER to TEXT
"""
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def run_migration():
    """Run the user_id conversion migration"""
    database_url = os.getenv('DATABASE_URL')

    if not database_url:
        print("ERROR: DATABASE_URL not found in environment variables")
        return False

    try:
        # Read the SQL file
        with open('migrations/convert-user-id-to-text.sql', 'r') as f:
            sql = f.read()

        # Connect to database
        print("Connecting to database...")
        conn = psycopg2.connect(database_url)
        cursor = conn.cursor()

        # Execute migration
        print("Running user_id conversion migration...")
        print("WARNING: This will delete all existing tasks!")
        print("Press Ctrl+C to cancel, or Enter to continue...")
        input()

        cursor.execute(sql)
        conn.commit()

        print("SUCCESS: Migration completed successfully!")
        print("\nVerifying migration...")

        # Verify the change
        cursor.execute("""
            SELECT column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_name = 'tasks' AND column_name = 'user_id';
        """)
        result = cursor.fetchone()
        if result:
            print(f"Column: {result[0]}, Type: {result[1]}, Nullable: {result[2]}")
        else:
            print("ERROR: user_id column not found!")

        # Close connection
        cursor.close()
        conn.close()

        return True

    except Exception as e:
        print(f"ERROR: Migration failed: {e}")
        return False

if __name__ == "__main__":
    print("=" * 50)
    print("Tasks Table Migration")
    print("Convert user_id from INTEGER to TEXT")
    print("=" * 50)
    run_migration()
