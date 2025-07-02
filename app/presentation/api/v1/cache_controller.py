"""
Cache management endpoints for monitoring and controlling cache behavior.
"""

from fastapi import APIRouter, HTTPException, Depends
from app.core.cache import get_cache_stats, clear_all_caches, invalidate_cache_pattern
from app.core.dependencies import get_current_superuser
from app.domain.models.user import User

router = APIRouter(prefix="/cache", tags=["cache-management"])


@router.get("/stats")
async def get_cache_statistics(
    current_user: User = Depends(get_current_superuser)
):
    """Get current cache statistics including size and configuration."""
    try:
        stats = get_cache_stats()
        return {
            "status": "success",
            "data": stats
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving cache stats: {str(e)}")


@router.delete("/clear")
async def clear_caches(
    current_user: User = Depends(get_current_superuser)
):
    """Clear all caches."""
    try:
        cleared_count = clear_all_caches()
        return {
            "status": "success",
            "message": f"Cleared {cleared_count} cache entries",
            "entries_cleared": cleared_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error clearing caches: {str(e)}")


@router.delete("/invalidate/{pattern}")
async def invalidate_cache_by_pattern(
    pattern: str,
    current_user: User = Depends(get_current_superuser)
):
    """Invalidate cache entries matching a specific pattern."""
    try:
        invalidated_count = invalidate_cache_pattern(pattern)
        return {
            "status": "success",
            "message": f"Invalidated {invalidated_count} cache entries matching pattern '{pattern}'",
            "pattern": pattern,
            "entries_invalidated": invalidated_count
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error invalidating cache pattern: {str(e)}")


@router.get("/health")
async def cache_health_check(
    current_user: User = Depends(get_current_superuser)
):
    """Health check endpoint for cache system."""
    try:
        stats = get_cache_stats()
        return {
            "status": "healthy",
            "cache_system": "operational",
            "stats": stats
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "cache_system": "error",
            "error": str(e)
        }
