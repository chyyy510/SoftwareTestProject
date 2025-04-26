def min_max(numbers):
    """Return both min and max from a list."""
    if not numbers:
        return None, None
    return min(numbers), max(numbers)
