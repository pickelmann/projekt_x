from core.unit.base import Unit

class robot(Unit):
    def __init__(self, name, x, y, z):
        super().__init__(name, x, y, z, traits=["can_dig"])

    def get_entity_type(self):
        return "robot"
