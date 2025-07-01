from sqlmodel import create_engine, SQLModel, Session
from app.core.config import settings

# Create engine
engine = create_engine(settings.DATABASE_URL, echo=settings.DB_ECHO)


def create_db_and_tables():
    """Create database tables"""
    SQLModel.metadata.create_all(bind=engine)


def get_session():
    """Dependency to get database session"""
    with Session(engine) as session:
        yield session
