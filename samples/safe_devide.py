def safe_divide(a, b):
    """Safely divide two numbers, return None if error."""
    try:
        return a / b
    except ZeroDivisionError:
        return None
