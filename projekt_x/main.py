# main.py
from core.world.world import MarsWorld
from core.interface.applet import run
from core.unit.colonist import Colonist   


def main():
    world = MarsWorld(30, 30, 150)
    colonist = Colonist("Bob", 5, 5, world.bottom_level+1)
    world.add_unit(colonist)
    run(world)
    print(f"Generierte Tiles: {len(world.tiles)} von maximal {world.size_x * world.size_y * world.size_z}")

if __name__ == "__main__":
    main()

