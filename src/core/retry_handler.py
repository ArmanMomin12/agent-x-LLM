# src/utils/retry_handler.py

import time
import functools

def retry_on_exception(
    retries: int = 3,
    delay: float = 2.0,
    backoff: float = 2.0,
    allowed_exceptions: tuple = (Exception,),
    verbose: bool = True
):
    """
    A decorator that retries a function on exception.

    Args:
        retries (int): Total retry attempts.
        delay (float): Initial delay between retries (in seconds).
        backoff (float): Multiplier for delay.
        allowed_exceptions (tuple): Exceptions to catch and retry.
        verbose (bool): Whether to print retry messages.

    Usage:
        @retry_on_exception(retries=3, delay=1)
        def unreliable_function():
            ...
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            _retries = retries
            _delay = delay
            while _retries > 0:
                try:
                    return func(*args, **kwargs)
                except allowed_exceptions as e:
                    _retries -= 1
                    if verbose:
                        print(f"⚠️ Retryable error: {e}. Retries left: {_retries}. Retrying in {_delay}s...")
                    time.sleep(_delay)
                    _delay *= backoff
            if verbose:
                print("❌ All retries failed.")
            raise Exception(f"Function `{func.__name__}` failed after {retries} retries.")
        return wrapper
    return decorator


