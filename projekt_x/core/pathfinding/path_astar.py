# Datei: core/pathfinding.py

import heapq

def heuristic(a, b):
    # Manhattan-Distanz als einfache Heuristik
    return abs(a[0] - b[0]) + abs(a[1] - b[1]) + abs(a[2] - b[2])

def find_path(world, start, goal):
    open_set = []
    heapq.heappush(open_set, (0, start))

    came_from = {}  # für Pfadrekonstruktion
    g_score = {start: 0}

    while open_set:
        _, current = heapq.heappop(open_set)

        if current == goal:
            return reconstruct_path(came_from, current)

        cx, cy, cz = current
        current_tile = world.get_tile(cx, cy, cz)

        for (dx, dy, dz), passable in current_tile.passable_edges.items():
            if not passable:
                continue
            neighbor = (cx + dx, cy + dy, cz + dz)

            if not (0 <= neighbor[0] < world.size_x and 0 <= neighbor[1] < world.size_y and 0 <= neighbor[2] < world.size_z):
                continue

            tentative_g = g_score[current] + 1  # Gewicht pro Schritt, später anpassbar
            if neighbor not in g_score or tentative_g < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = tentative_g
                f_score = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_set, (f_score, neighbor))

    return None  # kein Pfad gefunden

def reconstruct_path(came_from, current):
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    path.reverse()
    return path
    