#Base Class : Entity


class Entity:
    """Entity has world cordinates"""
    def __init__(self, arg):
        self.arg = arg

    def __str__(self):
        return "An Entity"
