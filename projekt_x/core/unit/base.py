from core.pathfinding.path_astar import find_path

class Unit:
    def __init__(self, name, x, y, z, traits=None):
        self.name = name
        self.x = x
        self.y = y
        self.z = z
        self.traits = traits if traits else []
        self.mining_target = None
        self.path = []

    def position(self):
        return (self.x, self.y, self.z)

    def has_trait(self, trait):
        return trait in self.traits

    def can_move_to(self, tile):
        if hasattr(tile, "passable_for"):
            return tile.passable_for.get(self.get_entity_type(), False)
        return False

    def get_entity_type(self):
        return "colonist"

    def move_to(self, tile):
        if self.can_move_to(tile):
            self.x, self.y, self.z = tile.x, tile.y, tile.z
            print(f"{self.name} moved to ({tile.x}, {tile.y}, {tile.z})")
        else:
            print(f"{self.name} cannot move to Tile ({tile.x}, {tile.y}, {tile.z})")

    def _is_adjacent(self, a, b):
        dx, dy, dz = abs(a[0] - b[0]), abs(a[1] - b[1]), abs(a[2] - b[2])
        return max(dx, dy, dz) == 1

    def tick(self, world):
        if self.mining_target:
          self._tick_mining(world)

    def tick(self, world):
        if not self.mining_target:
            return

        # === Mining-Logik ===
        tx, ty, tz = self.mining_target
        target_tile = world.get_tile(tx, ty, tz)

        # Bereits benachbart? Dann abbauen!
        for (dx, dy, dz), passable in target_tile.passable_edges.items():
            nx, ny, nz = tx + dx, ty + dy, tz + dz
            if (self.x, self.y, self.z) == (nx, ny, nz):
                if target_tile.material != "air":
                    target_tile.material = "air"
                    target_tile.symbol = target_tile._get_symbol()
                    target_tile.calc_passable_edges
                    print(f"{self.name} mined tile at {tx}, {ty}, {tz}")
                self.mining_target = None
                self.path = []
                return

        # Kein Pfad vorhanden? Finde einen zu einem passierbaren Nachbar des Ziels
        if not self.path:
            for (dx, dy, dz), passable in target_tile.passable_edges.items():
                if not passable:
                    continue
                neighbor_pos = (tx + dx, ty + dy, tz + dz)
                path = find_path(world, self.position(), neighbor_pos)
                if path:
                    self.path = path[1:]  # Startknoten weglassen
                    break
            if not self.path:
                print(f"{self.name} cannot reach tile at {tx},{ty},{tz}")
                self.mining_target = None
                return

        # Wegschritt ausführen
        if self.path:
            next_pos = self.path.pop(0)
            tile = world.get_tile(*next_pos)
            if self.can_move_to(tile):
                self.move_to(tile)
            else:
                print(f"{self.name} blocked at {self.x},{self.y},{self.z}, clearing path")
                self.path = []
                self.mining_target = None