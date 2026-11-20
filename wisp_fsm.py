# Finite state machine for the wisp: patrol -> chase -> search -> patrol, plus stunned.
import pathfinding

SIGHT = 5          # tiles of walking distance the wisp can see
SEARCH_TURNS = 3   # turns spent waiting at the last seen tile


def new_wisp(start):
    return dict(pos=start, state="patrol", stun=0, last_seen=None, timer=0, wp=0)


def stun(w, turns=2):
    w["state"] = "stunned"
    w["stun"] = turns


def wisp_step(grid, w, player, patrol):
    """Advance the wisp by one turn. Mutates the dict w."""
    if w["state"] == "stunned":
        w["stun"] -= 1
        if w["stun"] <= 0:
            w["state"] = "search"
            w["timer"] = SEARCH_TURNS
        return

    d = pathfinding.path_length(grid, w["pos"], player)
    if d is not None and d <= SIGHT:
        w["state"] = "chase"
        w["last_seen"] = player
    elif w["state"] == "chase":
        w["state"] = "search"
        w["timer"] = SEARCH_TURNS

    if w["state"] == "chase":
        target = player
    elif w["state"] == "search":
        target = w["last_seen"] or w["pos"]
        if w["pos"] == target:
            w["timer"] -= 1
            if w["timer"] <= 0:
                w["state"] = "patrol"
    else:
        target = patrol[w["wp"]]
        if w["pos"] == target:
            w["wp"] = (w["wp"] + 1) % len(patrol)
            target = patrol[w["wp"]]

    path = pathfinding.astar(grid, w["pos"], target)
    if path:
        w["pos"] = path[0]
