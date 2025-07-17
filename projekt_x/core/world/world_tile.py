
class MarsTile:
    def __init__(self, x, y, z, material="regolith"):
        self.x = x
        self.y = y
        self.z = z
        self.material = material
        self.symbol = self._get_symbol()
        self.tile_passable_for = {}
        self.passable_edges = {} 
        self.neighbors = []  

        self.add_tile_passability_for()

    def _get_symbol(self):
        return {
            "regolith": "R",
            "water": "W",
            "lava": "L",
            "ice": "I",
            "air": "A"
        }.get(self.material, "?")

    def add_tile_passability_for(self, entity_type="colonist"):
        self.passable_for = {
            "colonist": self.material == "air",
            "robot": self.material in ["air", "regolith"],
            "monster": self.material != "lava",
            "animal": self.material != "lava"
        }
    def remove_tile_passability_for(self):
        self.passable_for.clear()

    def remove_tile_passability_for(self, entity_type):
        """Entfernt die Passierbarkeit für einen bestimmten Entity-Typ."""
        del self.passable_for[entity_type]



    def compute_neighbors(self, world, mode='26'):
        self.neighbors = self.get_neighbors(world, mode)

    def get_neighbors(self, world, mode='26'):
        """Gibt benachbarte Tiles je nach Modus zurück ('6', '18', '26')."""
        offsets = []
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                for dz in [-1, 0, 1]:
                    if dx == dy == dz == 0:
                        continue
                    if mode == '6' and sum(abs(v) for v in (dx, dy, dz)) != 1:
                        continue
                    if mode == '18' and sum(abs(v) for v in (dx, dy, dz)) > 2:
                        continue
                    offsets.append((dx, dy, dz))

        neighbors = []
        for dx, dy, dz in offsets:
            nx, ny, nz = self.x + dx, self.y + dy, self.z + dz
            if 0 <= nx < world.size_x and 0 <= ny < world.size_y and 0 <= nz < world.size_z:
                neighbors.append(world.tiles[nx][ny][nz])
        return neighbors

    def calc_passable_edges(self):
        """Berechnet gerichtete Passierbarkeiten zu allen Nachbarn (pro Entity-Typ)."""
        self.passable_edges.clear()
        for neighbor in self.neighbors:
            dx = neighbor.x - self.x
            dy = neighbor.y - self.y
            dz = neighbor.z - self.z
            direction = (dx, dy, dz)
            self.passable_edges[direction] = {}

            for entity_type in self.passable_for:
                self_to_neighbor = self.passable_for.get(entity_type, False)
                neighbor_to_self = neighbor.passable_for.get(entity_type, False)
                is_passable = self_to_neighbor and neighbor_to_self
                self.passable_edges[direction][entity_type] = is_passable

    def get_passable_edges(self):
        """Gibt alle validen benachbarten Edges eines Tiles zurück, und zwar für alle Entrity-Typen, die in passable_for definiert sind"""
        return {direction: passable for direction, passable in self.passable_edges.items() if any(passable.values())}
    def get_passable_edges_for(self, entity_type):
        """Gibt alle  validen benachbarten Edges eines Tiles zurück, die für den angegebenen Entity-Typ passierbar sind."""
        return {direction: passable for direction, passable in self.passable_edges.items() if passable.get(entity_type, False)}


    def tick_tile(self):
        """
        Wird pro Spiel-Tick einmal aufgerufen. Hier können tile-eigene Prozesse ablaufen,
        wie z. B. Temperaturveränderung, Gasdiffusion, Pflanzenwachstum etc.
        """
        #self._simulate_temperature()
        #self._simulate_gas_exchange()
        # Später z. B. Pflanzenwachstum, Lavafluss etc.

#
    

    def get_symbol(self):
      return self.symbol 
    
    def __repr__(self):     
        return f"MarsTile({self.x}, {self.y}, {self.z}, material={self.material}, symbol={self.symbol}, passable_for={self.passable_for}, passable_edges={self.passable_edges}, neighbors={self.neighbors})"   