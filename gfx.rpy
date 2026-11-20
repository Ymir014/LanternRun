# Graphics: 2D transforms, ATL dynamic visuals and color matrices.

# 1) 2D coordinate transformation: the player hops, scales and tilts on every step.
transform hop(px, py, a=0, t=0):
    pos (px, py)
    anchor (.5, .5)
    rotate a
    zoom 1.0
    yoffset 0
    ease .08 zoom 1.3 yoffset -10
    ease .08 zoom 1.0 yoffset 0

# 2) ATL dynamic visuals: flickering lantern glow, floating wisp and the flash ring.
transform lantern_glow(px, py, s=1.0):
    pos (px, py)
    anchor (.5, .5)
    zoom s
    alpha .22
    block:
        choice:
            ease .15 alpha .30
        choice:
            ease .20 alpha .16
        choice:
            ease .10 alpha .25
        repeat

transform wisp_bob(px, py, a=1.0):
    pos (px, py)
    anchor (.5, .5)
    alpha a
    block:
        ease .8 yoffset -6
        ease .8 yoffset 6
        repeat

transform flash_ring(px, py):
    pos (px, py)
    anchor (.5, .5)
    zoom .3
    alpha 1.0
    linear .35 zoom 1.0 alpha 0.0

# 3) Color space: the board darkens as oil drops, desaturates at 1 heart and flashes red on a hit.
transform board_fx(b=0.0, s=1.0, c="#ffffff"):
    matrixcolor TintMatrix(c) * SaturationMatrix(s) * BrightnessMatrix(b)
