# The game board and HUD. Buttons and keys hand a command tuple back to the script loop.
screen board():
    default hover = None

    $ prev = pathfinding.astar(levels.LEVEL, player_pos, hover) if hover else []
    $ dark = -0.5 * (1.0 - oil / 30.0)
    $ sat = 0.35 if hearts == 1 else 1.0
    $ tint = "#ff7a7a" if hit else "#ffffff"
    $ ppx = player_pos[0] * TILE + TILE // 2
    $ ppy = player_pos[1] * TILE + TILE // 2
    $ wpx = wisp["pos"][0] * TILE + TILE // 2
    $ wpy = wisp["pos"][1] * TILE + TILE // 2

    add Solid("#0d0a14")

    if not busy:
        key "K_UP" action Return(("move", 0, -1))
        key "K_DOWN" action Return(("move", 0, 1))
        key "K_LEFT" action Return(("move", -1, 0))
        key "K_RIGHT" action Return(("move", 1, 0))
        key "K_w" action Return(("move", 0, -1))
        key "K_s" action Return(("move", 0, 1))
        key "K_a" action Return(("move", -1, 0))
        key "K_d" action Return(("move", 1, 0))
        key "K_f" action Return(("flash",))
        key "K_SPACE" action Return(("flash",))
        key "K_r" action Return(("restart",))

    fixed:
        xysize (12 * TILE, 9 * TILE)
        align (0.5, 0.58)
        xoffset shake_x
        at board_fx(dark, sat, tint)

        for y, row in enumerate(levels.LEVEL):
            for x, ch in enumerate(row):
                $ c = tile_at((x, y))
                $ col = "#1b1626" if ch == "#" else ("#4b4268" if (x, y) in prev else "#2d2740")
                add Solid(col) pos (x * TILE + 1, y * TILE + 1) xysize (TILE - 2, TILE - 2)
                if c == "K":
                    text "K" size 34 bold True color "#ffd36b" pos (x * TILE + TILE // 2, y * TILE + TILE // 2) anchor (.5, .5)
                elif c == "O":
                    text "O" size 30 color "#ff9d4d" pos (x * TILE + TILE // 2, y * TILE + TILE // 2) anchor (.5, .5)
                elif c == "E":
                    text "E" size 34 bold True color ("#7dff9b" if keys_found >= 3 else "#6b6580") pos (x * TILE + TILE // 2, y * TILE + TILE // 2) anchor (.5, .5)
                if ch != "#" and not busy:
                    button:
                        pos (x * TILE, y * TILE)
                        xysize (TILE, TILE)
                        background None
                        action Return(("walk", x, y))
                        hovered SetScreenVariable("hover", (x, y))
                        unhovered SetScreenVariable("hover", None)

        add Text("●", size=170, color="#ffcf70") at lantern_glow(ppx, ppy, 0.5 + oil / 60.0)
        add Solid("#8fe3ff", xysize=(26, 26)) at wisp_bob(wpx, wpy, 0.35 if wisp["state"] == "stunned" else 1.0)
        add Solid("#ffd36b", xysize=(26, 26)) at hop(ppx, ppy, player_angle, step_count)
        if flash_on:
            add Text("○", size=280, color="#fff2b0") at flash_ring(ppx, ppy)

    vbox:
        pos (60, 30)
        spacing 8
        text "Oil" size 26
        bar value StaticValue(oil, 30) xsize 300 ysize 20
        text ("Hearts: " + "♥ " * hearts) size 26

    vbox:
        align (1.0, 0.0)
        xoffset -60
        yoffset 30
        spacing 8
        text ("Keys: " + str(keys_found) + "/3") size 26
        text ("Wisp: " + wisp["state"]) size 26
        if hover and prev:
            text ("Path preview: " + str(len(prev)) + " oil") size 22

    text hint size 28 color "#ffd36b" align (0.5, 0.06)
    text "Move: arrows or WASD   Walk: click a tile   Flash: F or Space (3 oil)   Restart: R" size 20 align (0.5, 0.98)
