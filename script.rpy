# Lantern Run, Milestone 2 technical MVP.
define config.rollback_enabled = False
define config.window_title = "Lantern Run"

init -2 python:
    import levels
    import pathfinding
    import wisp_fsm

    TILE = 64

    def tile_at(p):
        c = levels.LEVEL[p[1]][p[0]]
        if c in "PW" or p in taken:
            return "."
        return c

    def can_walk(p):
        x, y = p
        return 0 <= y < len(levels.LEVEL) and 0 <= x < len(levels.LEVEL[0]) and levels.LEVEL[y][x] != "#"

    def pause(t):
        renpy.pause(t, hard=True)

    def reset_game():
        global player_pos, player_angle, step_count, oil, hearts, keys_found
        global turn, taken, wisp, busy, flash_on, hit, shake_x, hint
        player_pos = levels.PLAYER_START
        player_angle = 0
        step_count = 0
        oil = 30
        hearts = 3
        keys_found = 0
        turn = 0
        taken = set()
        wisp = wisp_fsm.new_wisp(levels.WISP_START)
        busy = False
        flash_on = False
        hit = False
        shake_x = 0
        hint = ""

    def end_state():
        if hearts <= 0 or oil <= 0:
            return "lose"
        if keys_found >= 3 and player_pos == levels.EXIT:
            return "win"
        return None

    def shake():
        global shake_x, hit
        hit = True
        for i in range(8):
            shake_x = (8 - i) * (-1 if i % 2 else 1)
            pause(0.03)
        shake_x = 0
        hit = False

    def touch_check():
        global hearts
        if wisp["pos"] == player_pos:
            hearts -= 1
            wisp["pos"] = levels.WISP_START
            wisp_fsm.stun(wisp, 2)
            shake()

    def wisp_turn():
        wisp_fsm.wisp_step(levels.LEVEL, wisp, player_pos, levels.PATROL)
        touch_check()

    def do_step(dest):
        global player_pos, player_angle, step_count, oil, keys_found, turn, hint
        player_angle = 12 * (dest[0] - player_pos[0])
        step_count += 1
        turn += 1
        oil -= 1
        player_pos = dest
        c = tile_at(dest)
        if c == "K":
            taken.add(dest)
            keys_found += 1
        elif c == "O":
            taken.add(dest)
            oil = min(30, oil + 5)
        elif c == "E" and keys_found < 3:
            hint = "The door is locked. Find all 3 keys."
        pause(0.14)
        touch_check()
        if end_state() is None:
            wisp_turn()

    def do_flash():
        global oil, turn, flash_on
        oil -= 3
        turn += 1
        flash_on = True
        pause(0.4)
        flash_on = False
        d = pathfinding.path_length(levels.LEVEL, wisp["pos"], player_pos)
        if d is not None and d <= 2:
            wisp_fsm.stun(wisp, 2)
        if end_state() is None:
            wisp_turn()

    def handle_command(cmd):
        global busy, hint
        busy = True
        hint = ""
        renpy.show_screen("board")
        kind = cmd[0]
        if kind == "move":
            dest = (player_pos[0] + cmd[1], player_pos[1] + cmd[2])
            if can_walk(dest):
                do_step(dest)
        elif kind == "walk":
            for p in pathfinding.astar(levels.LEVEL, player_pos, (cmd[1], cmd[2])):
                do_step(p)
                if end_state() or wisp["state"] == "chase":
                    break
        elif kind == "flash":
            if oil >= 3:
                do_flash()
            else:
                hint = "Not enough oil for a flash."
        elif kind == "restart":
            reset_game()
        busy = False
        return end_state()

default player_pos = levels.PLAYER_START
default player_angle = 0
default step_count = 0
default oil = 30
default hearts = 3
default keys_found = 0
default turn = 0
default taken = set()
default wisp = wisp_fsm.new_wisp(levels.WISP_START)
default busy = False
default flash_on = False
default hit = False
default shake_x = 0
default hint = ""

label start:
    scene black
    "You wake up inside a dark manor with nothing but a small lantern."
    "Find the three keys and reach the exit before the oil runs out. Something pale is drifting through the halls, and it wants your light."
    $ reset_game()

label turn_loop:
    $ cmd = renpy.call_screen("board")
    $ result = handle_command(cmd)
    if result == "win":
        jump escaped
    if result == "lose":
        jump lost
    jump turn_loop

label escaped:
    $ renpy.hide_screen("board")
    scene black
    "The door swings open and cool night air rushes in. You escaped with [oil] oil and [hearts] hearts left."
    return

label lost:
    $ renpy.hide_screen("board")
    scene black
    "The light fades and the manor swallows you whole."
    return
