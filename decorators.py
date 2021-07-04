import time


def profile_function(func):
    """Prints func execution time"""
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        time_taken = time.time() - start
        print('Profiler@ %s | %s: %s seconds', func.__name__, ' ' * 25,
              time_taken)
        return result
    return wrapper
