from datetime import datetime, timedelta, timezone
from functools import lru_cache, wraps


def timed_lru_cache(
    seconds: int = 300,
    maxsize: int = 128,
):
    def wrapped_cache(f):
        f = lru_cache(maxsize=maxsize)(f)
        lifetime = timedelta(seconds=seconds)
        expiration = datetime.now(timezone.utc) + lifetime

        @wraps(f)
        def wrapped_func(*args, **kwargs):
            nonlocal expiration
            now = datetime.now(timezone.utc)
            if now >= expiration:
                f.cache_clear()
                expiration = now + lifetime
            return f(*args, **kwargs)

        return wrapped_func

    return wrapped_cache
