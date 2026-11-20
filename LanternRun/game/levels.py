# Level data for Lantern Run (12 x 9 grid).
# '#' wall, '.' floor, 'K' key, 'O' oil drop, 'E' exit, 'P' player start, 'W' wisp start.
LEVEL = [
    "############",
    "#P...#.....#",
    "#.##.#.###.#",
    "#.#K...#K#.#",
    "#.#.####.#.#",
    "#...#O...#.#",
    "#.#.#.##.#.#",
    "#E#...#W..K#",
    "############",
]


def find(ch):
    for y, row in enumerate(LEVEL):
        for x, c in enumerate(row):
            if c == ch:
                return (x, y)


PLAYER_START = find("P")
WISP_START = find("W")
EXIT = find("E")

# Fixed waypoints the wisp walks between while patrolling.
PATROL = [(10, 7), (6, 5), (3, 7), (8, 5)]
