from core.unit.base import Unit

class Colonist(Unit):
    def __init__(self, name, x, y, z):
        super().__init__(name, x, y, z, traits=["needs_oxygen", "can_build"])

    def get_entity_type(self):
        return "colonist"
