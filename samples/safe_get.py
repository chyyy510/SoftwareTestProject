def safe_get(d: dict, key, default=None):
    """Safely get a value from a dict."""
    return d.get(key, default)
