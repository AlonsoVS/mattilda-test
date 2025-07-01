from fastapi import APIRouter
from app.api.routes.school import school_router
from app.api.routes.student import student_router
from app.api.routes.invoice import invoice_router

api_router = APIRouter()

# Include all routers
api_router.include_router(school_router)
api_router.include_router(student_router)
api_router.include_router(invoice_router)
