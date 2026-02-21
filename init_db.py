# Database Initialization Script
import sys
sys.path.insert(0, 'backend')

from src.database import init_db
from src.models.user import User
from src.models.task import Task

if __name__ == "__main__":
    print("Initializing database...")
    init_db()
    print("Database tables created successfully!")
    print("\nTables created:")
    print("- users")
    print("- tasks")
    print("- Better Auth tables (auto-created by Better Auth)")
