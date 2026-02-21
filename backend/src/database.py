from sqlmodel import create_engine, Session, SQLModel
from sqlalchemy.pool import QueuePool
import os
from dotenv import load_dotenv

load_dotenv()

# Database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://username:password@localhost/todo_db")

# Create engine with optimized connection pooling
engine = create_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=3600,
    pool_pre_ping=True,
    echo=False,
    connect_args={
        "options": "-c timezone=utc"
    }
)

def get_db():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session

def init_db():
    """Initialize database tables"""
    SQLModel.metadata.create_all(engine)

def close_db():
    """Close database connections"""
    engine.dispose()
