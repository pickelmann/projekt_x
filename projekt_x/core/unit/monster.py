from core.NPC.base import Unit

class Monster(Unit):
    def __init__(self, name, x, y, z):
        super().__init__(name, x, y, z, traits=["needs_oxygen", "hostile"])

    def get_entity_type(self):
        return "monster"
