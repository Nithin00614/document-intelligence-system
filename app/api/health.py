"""
Health Check API

Provides a simple endpoint to verify that the
application is running.
"""

from fastapi import APIRouter

router = APIRouter(
    prefix="/health",
    tags=["Health"],
)


@router.get("/")
async def health_check():
    """
    Health check endpoint.
    """

    return {
    "status": "healthy",
    "service": "Document Intelligence System",
    "version": "1.0.0"
}