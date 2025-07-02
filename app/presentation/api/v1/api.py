from fastapi import APIRouter
from app.presentation.api.v1.school_controller import router as school_router
from app.presentation.api.v1.student_controller import router as student_router
from app.presentation.api.v1.invoice_controller import router as invoice_router
from app.presentation.api.v1.cache_controller import router as cache_router
from app.presentation.api.v1.auth_controller import router as auth_router

api_router = APIRouter()

# Include all routers
api_router.include_router(auth_router)
api_router.include_router(school_router)
api_router.include_router(student_router)
api_router.include_router(invoice_router)
api_router.include_router(cache_router)
