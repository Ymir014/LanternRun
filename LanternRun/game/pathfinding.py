# A* pathfinding on the tile grid (4-directional, every step costs 1).
import heapq


def manhattan(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def neighbors(grid, p):
    x, y = p
    for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
        nx, ny = x + dx, y + dy
        if 0 <= ny < len(grid) and 0 <= nx < len(grid[0]) and grid[ny][nx] != "#":
            yield (nx, ny)


def astar(grid, start, goal):
    """Tiles from start (excluded) to goal (included), or [] when there is no route."""
    if start == goal:
        return []
    frontier = [(manhattan(start, goal), 0, start)]
    cost = {start: 0}
    came_from = {}
    while frontier:
        _, g, current = heapq.heappop(frontier)
        if current == goal:
            path = []
            while current != start:
                path.append(current)
                current = came_from[current]
            path.reverse()
            return path
        if g > cost[current]:
            continue
        for n in neighbors(grid, current):
            new_g = g + 1
            if new_g < cost.get(n, 10 ** 9):
                cost[n] = new_g
                came_from[n] = current
                heapq.heappush(frontier, (new_g + manhattan(n, goal), new_g, n))
    return []


def path_length(grid, a, b):
    if a == b:
        return 0
    path = astar(grid, a, b)
    return len(path) if path else None
