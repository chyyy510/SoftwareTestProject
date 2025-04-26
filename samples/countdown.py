def countdown(n):
    """Yield countdown numbers."""
    while n > 0:
        yield n
        n -= 1
