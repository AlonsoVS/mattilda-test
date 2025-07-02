"""
Caching utilities for the application.
Provides decorators and utilities for caching API responses.
"""

import functools
import hashlib
from typing import Any, Callable, Optional, Union
from cachetools import TTLCache
from datetime import datetime, timedelta
import json
import inspect


# Global cache instances
# TTL Cache for API responses (time-to-live: 5 minutes, max size: 1000 items)
api_cache = TTLCache(maxsize=1000, ttl=300)  # 5 minutes TTL

# Longer TTL cache for less frequently changing data (30 minutes)
static_cache = TTLCache(maxsize=500, ttl=1800)  # 30 minutes TTL


def _generate_cache_key(*args, **kwargs) -> str:
    """Generate a cache key from function arguments."""
    # Only include serializable arguments
    serializable_data = []
    
    for arg in args:
        # Skip complex objects that can't be serialized
        if isinstance(arg, (str, int, float, bool, type(None))):
            serializable_data.append(arg)
        else:
            serializable_data.append(str(type(arg).__name__))
    
    for key, value in kwargs.items():
        if isinstance(value, (str, int, float, bool, type(None))):
            serializable_data.append(f"{key}:{value}")
        else:
            serializable_data.append(f"{key}:{type(value).__name__}")
    
    key_string = "|".join(str(item) for item in serializable_data)
    return hashlib.md5(key_string.encode()).hexdigest()


def simple_cache(cache_instance: TTLCache, key_prefix: str = ""):
    """
    Simple caching decorator that works with FastAPI.
    """
    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Extract simple arguments for cache key (skip dependency objects)
            simple_args = []
            simple_kwargs = {}
            
            # Get function signature to identify path and query parameters
            sig = inspect.signature(func)
            param_names = list(sig.parameters.keys())
            
            # Map positional args to parameter names
            for i, arg in enumerate(args):
                if i < len(param_names):
                    param_name = param_names[i]
                    # Only cache simple types that represent API parameters
                    if isinstance(arg, (int, str, float, bool, type(None))):
                        simple_kwargs[param_name] = arg
            
            # Add keyword arguments that are simple types
            for key, value in kwargs.items():
                if isinstance(value, (int, str, float, bool, type(None))):
                    simple_kwargs[key] = value
            
            # Generate cache key
            cache_key = f"{key_prefix}:{func.__name__}:{_generate_cache_key(**simple_kwargs)}"
            
            # Try to get from cache
            try:
                if cache_key in cache_instance:
                    cached_result = cache_instance[cache_key]
                    return cached_result
            except Exception:
                # If cache lookup fails, proceed without caching
                pass
            
            # Execute function and cache result
            result = await func(*args, **kwargs)
            
            # Store in cache (only if result is serializable)
            try:
                # Test if result can be stored (basic serialization check)
                if result is not None:
                    cache_instance[cache_key] = result
            except Exception:
                # If caching fails, still return the result
                pass
            
            return result
        
        return wrapper
    return decorator


def cache_api_response(ttl: int = 300) -> Callable:
    """
    Decorator for caching API responses with standard TTL.
    Default TTL: 5 minutes
    """
    return simple_cache(api_cache, "api")


def cache_static_data(ttl: int = 1800) -> Callable:
    """
    Decorator for caching static/semi-static data with longer TTL.
    Default TTL: 30 minutes
    """
    return simple_cache(static_cache, "static")


def invalidate_cache_pattern(pattern: str) -> int:
    """
    Invalidate cache entries matching a pattern.
    
    Args:
        pattern: Pattern to match in cache keys
        
    Returns:
        Number of entries invalidated
    """
    invalidated = 0
    
    # Invalidate from both cache instances
    for cache_instance in [api_cache, static_cache]:
        keys_to_remove = [key for key in cache_instance.keys() if pattern in key]
        for key in keys_to_remove:
            del cache_instance[key]
            invalidated += 1
    
    return invalidated


def clear_all_caches() -> int:
    """
    Clear all caches.
    
    Returns:
        Total number of entries cleared
    """
    total_cleared = len(api_cache) + len(static_cache)
    api_cache.clear()
    static_cache.clear()
    return total_cleared


def get_cache_stats() -> dict:
    """
    Get cache statistics.
    
    Returns:
        Dictionary containing cache statistics
    """
    return {
        "api_cache": {
            "size": len(api_cache),
            "maxsize": api_cache.maxsize,
            "ttl": api_cache.ttl
        },
        "static_cache": {
            "size": len(static_cache),
            "maxsize": static_cache.maxsize,
            "ttl": static_cache.ttl
        }
    }
