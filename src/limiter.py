from slowapi import Limiter
from slowapi.util import get_remote_address
import os

# Create limiter instance using in-memory token bucket based on IP
limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[f"{os.getenv('RATE_LIMIT_PER_MINUTE', '100')}/minute"]
)
