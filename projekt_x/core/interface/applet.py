import pygame
import time
from core.world.world import MarsWorld

TILE_SIZE = 20
VIEW_WIDTH = 40
VIEW_HEIGHT = 30
HUD_HEIGHT = 30

# Highlight-Ziele wie "mine", "selected", "build_preview", etc.
tile_highlights = {
    "mine": None,
}


def get_tile_color(symbol):
    return {
        "R": (150, 150, 150),
        "W": (0, 100, 255),
        "L": (255, 50, 0),
        "I": (100, 255, 255),
        "A": (255, 200, 100),
    }.get(symbol, (80, 80, 80))


def draw_hud(screen, font, world, z_level, tile, tx, ty):
    hud_line = f"Ebene: {world.get_logical_z(z_level)} | Tick: {world.get_tick_count()}"
    if tile:
        num_edges = len(tile.get_passable_edges())
        passable = any(tile.get_passable_edges().values())
        hud_line += f" | Tile: ({tx},{ty},{z_level}) Mat: {tile.material} | Passable: {passable} | Edges: {num_edges}"

    pygame.draw.rect(screen, (50, 50, 50), pygame.Rect(0, 0, VIEW_WIDTH * TILE_SIZE, HUD_HEIGHT))
    hud_surface = font.render(hud_line, True, (200, 200, 200))
    screen.blit(hud_surface, (10, 5))


def draw_tiles(screen, font, world, x_offset, y_offset, z_level):
    for y in range(VIEW_HEIGHT):
        for x in range(VIEW_WIDTH):
            wx, wy = x + x_offset, y + y_offset
            if not (0 <= wx < world.size_x and 0 <= wy < world.size_y): continue

            tile = world.get_tile(wx, wy, z_level)
            symbol = tile.get_symbol()
            color = get_tile_color(symbol)

            rect = pygame.Rect(x*TILE_SIZE, y*TILE_SIZE + HUD_HEIGHT, TILE_SIZE, TILE_SIZE)
            pygame.draw.rect(screen, color, rect)

            # Rote Markierung für Mining-Ziel
            if tile_highlights.get("mine") == (wx, wy, z_level):
                pygame.draw.rect(screen, (255, 0, 0), rect, 2)

            symbol_surface = font.render(symbol, True, (0, 0, 0))
            screen.blit(symbol_surface, (x*TILE_SIZE + 5, y*TILE_SIZE + HUD_HEIGHT + 2))


def draw_units(screen, font, world, x_offset, y_offset, z_level):
    for unit in world.units:
        if unit.z != z_level:
            continue
        ux, uy = unit.x - x_offset, unit.y - y_offset
        if not (0 <= ux < VIEW_WIDTH and 0 <= uy < VIEW_HEIGHT): continue

        pygame.draw.circle(screen, (255, 255, 255),
            (ux*TILE_SIZE + TILE_SIZE//2, uy*TILE_SIZE + TILE_SIZE//2 + HUD_HEIGHT), 6)
        name_surface = font.render(unit.name[0], True, (0, 0, 0))
        screen.blit(name_surface, (ux*TILE_SIZE + 4, uy*TILE_SIZE + HUD_HEIGHT + 2))


def run(world):
    global tile_highlights
    pygame.init()
    screen = pygame.display.set_mode((VIEW_WIDTH * TILE_SIZE, VIEW_HEIGHT * TILE_SIZE + HUD_HEIGHT))
    pygame.display.set_caption("MarsCraft - die Mars-Simulation")
    font = pygame.font.SysFont("consolas", 14)

    x_offset, y_offset, z_level = 0, 0, world.bottom_level
    last_tick_time = time.time()
    running = True

    while running:
        screen.fill((0, 0, 0))
        mx, my = pygame.mouse.get_pos()
        tx = mx // TILE_SIZE + x_offset
        ty = (my - HUD_HEIGHT) // TILE_SIZE + y_offset

        tile = None
        if 0 <= tx < world.size_x and 0 <= ty < world.size_y and 0 <= z_level < world.size_z:
            tile = world.get_tile(tx, ty, z_level)

        draw_hud(screen, font, world, z_level, tile, tx, ty)
        draw_tiles(screen, font, world, x_offset, y_offset, z_level)
        draw_units(screen, font, world, x_offset, y_offset, z_level)

        current_time = time.time()
        if world.is_simulation_running() and current_time - last_tick_time >= 1.0:
            world.tick_all()
            last_tick_time = current_time

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:   x_offset = max(0, x_offset - 1)
                elif event.key == pygame.K_RIGHT: x_offset = min(world.size_x - VIEW_WIDTH, x_offset + 1)
                elif event.key == pygame.K_UP:    y_offset = max(0, y_offset - 1)
                elif event.key == pygame.K_DOWN:  y_offset = min(world.size_y - VIEW_HEIGHT, y_offset + 1)
                elif event.key == pygame.K_PAGEUP:   z_level = min(z_level + 1, world.size_z - 1)
                elif event.key == pygame.K_PAGEDOWN: z_level = max(0, z_level - 1)
                elif event.key == pygame.K_SPACE:    world.toggle_simulation()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1 and tile:
                    tile_highlights["mine"] = (tx, ty, z_level)
                    if world.units:
                        world.units[0].mining_target = (tx, ty, z_level)
                elif event.button == 4:
                    z_level = max(0, z_level - 1)
                elif event.button == 5:
                    z_level = min(z_level + 1, world.size_z - 1)

    pygame.quit()
