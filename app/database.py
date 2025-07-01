import os
from sqlmodel import create_engine, SQLModel, Session

# Database URL from environment variable with default for development
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://postgres:Post12.gres@localhost:5432/mattilda_db"
)

# Create engine
engine = create_engine(DATABASE_URL, echo=True)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
