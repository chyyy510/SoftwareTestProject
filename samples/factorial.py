def factorial(n: int) -> int:
    """Return the factorial of n."""
    if n == 0:
        return 1
    return n * factorial(n - 1)
