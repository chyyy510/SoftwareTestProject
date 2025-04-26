def merge_dicts(dict1: dict, dict2: dict) -> dict:
    """Merge two dictionaries."""
    result = dict1.copy()
    result.update(dict2)
    return result
