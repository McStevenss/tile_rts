TILE_ATLAS = {
    (0,0,0): (10,3),
    (1,1,1): [(0,1),(4,1)],


    "default": (3,13),
    "human_village": (1,13),
    "orc_village": (11,13),
    "mine": (3,12),
    "tree_base": (3,5),
    "tree_mid": (3,4),
    "tree_top": (3,3),
}

GRUNT = {
    "idle": (0,7),
    "down": (24,31),
    "left": (8,15),
    "right": (8,15),
    "up": (16,23),
    "a_left": (32,39),
    "a_right": (32,39),
    "die":(40,43),
}

GOLDMINE = {
    "idle": (0,3)
}

ANIMATION_ATLAS = {
    "grunt": GRUNT,
    "goldmine": GOLDMINE,
}

MAP_SIZE = (64,64)
DIAGONAL_PATHING = True

