from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.core.config import settings
from app.infrastructure.database.connection import create_db_and_tables
from app.infrastructure.database.seed_data import seed_data
from app.presentation.api.v1.api import api_router

# Import persistence entities so SQLModel can register them
from app.infrastructure.persistence.school_entity import SchoolEntity
from app.infrastructure.persistence.student_entity import StudentEntity
from app.infrastructure.persistence.invoice_entity import InvoiceEntity


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    create_db_and_tables()
    await seed_data()
    yield
    # Shutdown (if needed)


def create_app() -> FastAPI:
    """Create FastAPI application"""
    app = FastAPI(
        title=settings.PROJECT_NAME,
        description=settings.PROJECT_DESCRIPTION,
        version=settings.VERSION,
        debug=settings.DEBUG,
        lifespan=lifespan
    )

    # Include API routes
    app.include_router(api_router, prefix=settings.API_V1_STR)

    @app.get("/health")
    async def health_check():
        """Health check endpoint for Docker health checks"""
        return {"status": "healthy", "service": "mattilda-backend"}

    return app


app = create_app()
