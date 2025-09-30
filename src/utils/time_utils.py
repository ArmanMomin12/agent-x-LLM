# src/utils/time_utils.py

import time
from datetime import datetime, timedelta

def get_current_timestamp():
    """Returns the current timestamp as a formatted string."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def format_duration(seconds: float) -> str:
    """Formats elapsed time in seconds to a human-readable form."""
    return str(timedelta(seconds=int(seconds)))

class Timer:
    """Context manager for timing code execution."""
    def __init__(self, task_name="Task"):
        self.task_name = task_name
        self.start_time = None

    def __enter__(self):
        self.start_time = time.time()
        print(f"⏳ {self.task_name} started at {get_current_timestamp()}")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        elapsed = time.time() - self.start_time
        print(f"✅ {self.task_name} finished in {format_duration(elapsed)}")

def measure_time(func):
    """Decorator to measure execution time of a function."""
    def wrapper(*args, **kwargs):
        start = time.time()
        print(f"⏱️ Running: {func.__name__}")
        result = func(*args, **kwargs)
        end = time.time()
        print(f"✅ {func.__name__} completed in {format_duration(end - start)}")
        return result
    return wrapper


