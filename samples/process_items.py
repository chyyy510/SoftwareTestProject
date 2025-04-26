def process_items(items=None):
    if items is None:
        items = []
    return [item.upper() for item in items if isinstance(item, str)]
