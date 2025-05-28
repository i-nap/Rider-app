from django.core.cache import cache
from django.utils import timezone
import json

def check_rate_limit(key: str, max_attempts: int = 5, window_minutes: int = 15) -> bool:
    """
    Rate limiting function using Django cache
    
    Args:
        key: Unique identifier for rate limiting
        max_attempts: Maximum attempts allowed
        window_minutes: Time window in minutes
    
    Returns:
        bool: True if request is allowed, False if rate limited
    """
    now = timezone.now().timestamp()
    window_seconds = window_minutes * 60
    
    # Get existing attempts
    cache_key = f"rate_limit_{key}"
    attempts_data = cache.get(cache_key, [])
    
    # Filter out old attempts
    recent_attempts = [
        attempt_time for attempt_time in attempts_data 
        if now - attempt_time < window_seconds
    ]
    
    # Check if we've exceeded the limit
    if len(recent_attempts) >= max_attempts:
        return False
    
    # Add current attempt
    recent_attempts.append(now)
    
    # Update cache
    cache.set(cache_key, recent_attempts, timeout=window_seconds)
    
    return True