def make_person(name, age, **kwargs):
    """Create a person dictionary with extra fields."""
    person = {"name": name, "age": age}
    person.update(kwargs)
    return person
