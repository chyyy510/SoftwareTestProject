def read_file(filepath):
    """Read content from a file."""
    try:
        with open(filepath, "r") as file:
            return file.read()
    except FileNotFoundError:
        return None
