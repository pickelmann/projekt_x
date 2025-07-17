# Datei: core/tile_viewer.py

import pygame
import time
from core.mars_world import MarsWorld

TILE_SIZE = 20
VIEW_WIDTH = 40
VIEW_HEIGHT = 30
HUD_HEIGHT = 30

def run_tile_viewer(world):
    pygame.init()
    screen = pygame.display.set_mode((VIEW_WIDTH * TILE_SIZE, VIEW_HEIGHT * TILE_SIZE + HUD_HEIGHT))
    pygame.display.set_caption("Mars Tile Viewer")
    font = pygame.font.SysFont("consolas", 14)

    x_offset, y_offset, z_level = 0, 0, world.bottom_level
    running = True
    last_tick_time = time.time()

    while running:
        screen.fill((0, 0, 0))

        # HUD
        logical_z = world.get_logical_z(z_level)
        hud_text = font.render(
            f"Ebene: {logical_z} (Index z={z_level}) | Tick: {world.get_tick_count()}",
            True, (0, 255, 0)
        )
        screen.blit(hud_text, (10, 5))

        # Tiles
        for y in range(VIEW_HEIGHT):
            for x in range(VIEW_WIDTH):
                world_x = x + x_offset
                world_y = y + y_offset
                if 0 <= world_x < world.size_x and 0 <= world_y < world.size_y and 0 <= z_level < world.size_z:
                    tile = world.get_tile(world_x, world_y, z_level)
                    symbol = tile.get_symbol()

                    if symbol == "R":
                        color = (150, 150, 150)
                    elif symbol == "W":
                        color = (0, 100, 255)
                    elif symbol == "L":
                        color = (255, 50, 0)
                    elif symbol == "I":
                        color = (100, 255, 255)
                    elif symbol == "A":
                        color = (255, 200, 100)
                    else:
                        color = (80, 80, 80)

                    rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE + HUD_HEIGHT, TILE_SIZE, TILE_SIZE)
                    pygame.draw.rect(screen, color, rect)

                    symbol_surface = font.render(symbol, True, (0, 0, 0))
                    screen.blit(symbol_surface, (x*TILE_SIZE + 5, y*TILE_SIZE + HUD_HEIGHT + 2))

        # Units
        for unit in world.units:
            if unit.z == z_level:
                ux = unit.x - x_offset
                uy = unit.y - y_offset
                if 0 <= ux < VIEW_WIDTH and 0 <= uy < VIEW_HEIGHT:
                    pygame.draw.circle(screen, (255, 255, 255),
                        (ux*TILE_SIZE + TILE_SIZE//2, uy*TILE_SIZE + TILE_SIZE//2 + HUD_HEIGHT), 6)
                    name_surface = font.render(unit.name[0], True, (0, 0, 0))
                    screen.blit(name_surface, (ux*TILE_SIZE + 4, uy*TILE_SIZE + HUD_HEIGHT + 2))

        # Simulation tick alle 1 Sekunde
        current_time = time.time()
        if world.is_simulation_running() and current_time - last_tick_time >= 1.0:
            world.tick_all()
            last_tick_time = current_time

        pygame.display.flip()

        # Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_offset = max(0, x_offset - 1)
                elif event.key == pygame.K_RIGHT:
                    x_offset = min(world.size_x - VIEW_WIDTH, x_offset + 1)
                elif event.key == pygame.K_UP:
                    y_offset = max(0, y_offset - 1)
                elif event.key == pygame.K_DOWN:
                    y_offset = min(world.size_y - VIEW_HEIGHT, y_offset + 1)
                elif event.key == pygame.K_PAGEUP:
                    z_level = min(z_level + 1, world.size_z - 1)
                elif event.key == pygame.K_PAGEDOWN:
                    z_level = max(0, z_level - 1)
                elif event.key == pygame.K_SPACE:
                    world.toggle_simulation()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    z_level = max(0, z_level - 1)
                elif event.button == 5:
                    z_level = min(z_level + 1, world.size_z - 1)
                elif event.button == 1:  # Linksklick
                    mx, my = pygame.mouse.get_pos()
                    tx = mx // TILE_SIZE + x_offset
                    ty = (my - HUD_HEIGHT) // TILE_SIZE + y_offset
                    if 0 <= tx < world.size_x and 0 <= ty < world.size_y:
                        mine_tile_pos = (tx, ty, z_level)
                        tile = world.get_tile(tx, ty, z_level)
                        print("=== TILE INFO ===")
                        tile.print_debug()
                        # Erste Unit bekommt Mining-Ziel
                        if world.units:
                            world.units[0].mining_target = mine_tile_pos
    pygame.quit()
