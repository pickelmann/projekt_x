# Datei: core/mars_world.py

from core.world.world_tile import MarsTile
import random

BOTTOM_LEVEL = 100  # Meeresboden liegt bei z = 100, darunter = Untergrund

class MarsWorld:
    def __init__(self, size_x, size_y, size_z, planet = "Mars"):
        self.size_x = size_x
        self.size_y = size_y
        self.size_z = size_z
        self.tiles = [[[None for _ in range(size_z)] for _ in range(size_y)] for _ in range(size_x)]
        self.units = []  # Liste aller aktiven Einheiten
        self.planet = planet

        self.tick_counter = 0
        self.simulation_running = False

        self._create_tiles()
        self._link_neighbors()
        self.update_all_edge_passabilities()


    def _create_tiles(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                for z in range(self.size_z):
                    # Logisches Z-Level berechnen (z.B. z=0 bedeutet Ebene -BOTTOM_LEVEL)
                    logical_z = z - BOTTOM_LEVEL
                    if logical_z > 0:
                        material = "air"
                    elif logical_z <= 0 and random.random() < 0.2:
                        material = "ice"
                    else:
                        material = "regolith"
                    self.tiles[x][y][z] = MarsTile(x, y, z, material=material)

    def _link_neighbors(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                for z in range(self.size_z):
                    self.tiles[x][y][z].compute_neighbors(self, mode='26')

    def update_all_edge_passabilities(self):
        for x in range(self.size_x):
            for y in range(self.size_y):
                for z in range(self.size_z):
                    self.tiles[x][y][z].calc_passable_edges()


#Simulationsticker und -steuerung
    def tick_all(self):
        """Zentraler Tick: Aktualisiert Tiles und Units."""
        for x in range(self.size_x):
            for y in range(self.size_y):
                for z in range(self.size_z):
                    self.tiles[x][y][z].tick_tile()

        for unit in self.units:
            unit.tick(self)

        self.tick_counter += 1

    def get_tick_count(self):
      return self.tick_counter
    
    def start_simulation(self):  
        self.simulation_running = True  

    def pause_simulation(self):
        self.simulation_running = False

    def toggle_simulation(self):
        self.simulation_running = not self.simulation_running
        print("SIMULATION:", "RUNNING" if self.simulation_running else "PAUSED")
        
    def is_simulation_running(self):
        return self.simulation_running
# Getter-Methoden für Tiles und Z-Werte
    def get_tile(self, x, y, z):
        return self.tiles[x][y][z]

    def get_logical_z(self, z):
        """Gibt den logischen Z-Wert zurück, z. B. Ebene 0 = Meeresboden."""
        return z - BOTTOM_LEVEL

    def get_physical_z(self, logical_z):
        """Wandelt logischen Z-Wert (z. B. 0 = Boden) in physikalischen Index um."""
        return logical_z + BOTTOM_LEVEL
        

# Units
    def add_unit(self, unit):
        self.units.append(unit)
    @property
    def bottom_level(self):
        return BOTTOM_LEVEL
