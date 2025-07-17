from core.unit.base import Unit

class Animal(Unit):
    def __init__(self, name, x, y, z):
        super().__init__(name, x, y, z, traits=["needs_oxygen", "animal"])

    def get_entity_type(self):
        return "animal"
