from ff1tiles import *

expand_mountains = [
    [[MOUNTAIN, "_", "_",
      "_", "_", "_",
      "_", "_", "_"],
     MOUNTAIN],
    [["_", MOUNTAIN, "_",
      "_", "_", "_",
      "_", "_", "_"],
     MOUNTAIN],
    [["_", "_", MOUNTAIN,
      "_", "_", "_",
      "_", "_", "_"],
     MOUNTAIN],

    [["_", "_", "_",
      MOUNTAIN, "_", "_",
      "_", "_", "_"],
     MOUNTAIN],
    [["_", "_", "_",
      "_", MOUNTAIN, "_",
      "_", "_", "_"],
     MOUNTAIN],
    [["_", "_", "_",
      "_", "_", MOUNTAIN,
      "_", "_", "_"],
     MOUNTAIN],

    [["_", "_", "_",
      "_", "_", "_",
      MOUNTAIN, "_", "_"],
     MOUNTAIN],
    [["_", "_", "_",
      "_", "_", "_",
      "_", MOUNTAIN, "_"],
     MOUNTAIN],
    [["_", "_", "_",
      "_", "_", "_",
      "_", "_", MOUNTAIN],
     MOUNTAIN],
]

expand_oceans = [
    [[OCEAN, "_", "_",
      "_", "_", "_",
      "_", "_", "_"],
     OCEAN],
    [["_", OCEAN, "_",
      "_", "_", "_",
      "_", "_", "_"],
     OCEAN],
    [["_", "_", OCEAN,
      "_", "_", "_",
      "_", "_", "_"],
     OCEAN],

    [["_", "_", "_",
      OCEAN, "_", "_",
      "_", "_", "_"],
     OCEAN],
    [["_", "_", "_",
      "_", OCEAN, "_",
      "_", "_", "_"],
     OCEAN],
    [["_", "_", "_",
      "_", "_", OCEAN,
      "_", "_", "_"],
     OCEAN],

    [["_", "_", "_",
      "_", "_", "_",
      OCEAN, "_", "_"],
     OCEAN],
    [["_", "_", "_",
      "_", "_", "_",
      "_", OCEAN, "_"],
     OCEAN],
    [["_", "_", "_",
      "_", "_", "_",
      "_", "_", OCEAN],
     OCEAN],
]

connect_diagonals = [
    [["*", RIVER, "_",
     "*", "_", RIVER,
     "*", "*", "*"],
     RIVER],
    [["_", RIVER, "*",
     RIVER, "_", "*",
     "*", "*", "*"],
     RIVER],
    [["*", OCEAN, "_",
     "*", "_", OCEAN,
     "*", "*", "*"],
     OCEAN],
    [["_", OCEAN, "*",
     OCEAN, "_", "*",
     "*", "*", "*"],
     OCEAN],
    [["*", MOUNTAIN, "_",
     "*", "_", MOUNTAIN,
     "*", "*", "*"],
     MOUNTAIN],
    [["_", MOUNTAIN, "*",
     MOUNTAIN, "_", "*",
     "*", "*", "*"],
     MOUNTAIN],
]

# smooth_rivers = [
#     [["_",      RIVER,    "_",
#      MOUNTAIN, RIVER,    MOUNTAIN,
#      MOUNTAIN, MOUNTAIN, MOUNTAIN],
#      MOUNTAIN],
#     [[MOUNTAIN, MOUNTAIN, "_",
#      MOUNTAIN, RIVER,    RIVER,
#      MOUNTAIN, MOUNTAIN, "_"],
#      MOUNTAIN],
#     [[MOUNTAIN, MOUNTAIN, MOUNTAIN,
#      MOUNTAIN, RIVER,    MOUNTAIN,
#      "_",      RIVER,    "_"],
#      MOUNTAIN],
#     [["_",   MOUNTAIN, MOUNTAIN,
#      RIVER, RIVER,    MOUNTAIN,
#      "_",   MOUNTAIN, MOUNTAIN],
#      MOUNTAIN],
#     [["_",  RIVER, "_",
#      LAND, RIVER, LAND,
#      LAND, LAND,  LAND],
#      LAND],
#     [[LAND, LAND, "_",
#      LAND, RIVER, RIVER,
#      LAND, LAND, "_"],
#      LAND],
#     [[LAND, LAND,  LAND,
#      LAND, RIVER, LAND,
#      "_",  RIVER, "_"],
#      LAND],
#     [["_",   LAND,  LAND,
#      RIVER, RIVER, LAND,
#      "_",   LAND,  LAND],
#      LAND],
#     [["_",   MOUNTAIN, "_",
#      RIVER, MOUNTAIN, RIVER,
#      RIVER, RIVER,    RIVER],
#      RIVER],
#     [[RIVER, RIVER,    "_",
#      RIVER, MOUNTAIN, MOUNTAIN,
#      RIVER, RIVER,    "_"],
#      RIVER],
#     [[RIVER, RIVER,    RIVER,
#      RIVER, MOUNTAIN, RIVER,
#      "_",   MOUNTAIN, "_"],
#      RIVER],
#     [["_",      RIVER,    RIVER,
#      MOUNTAIN, MOUNTAIN, RIVER,
#      "_",      RIVER,    RIVER],
#      RIVER],
# ]

# fixup_mountains = [
#     [["*", "_",      "*",
#       "_", MOUNTAIN, "_",
#       "*", "*",      "*"],
#      LAND],
#     [["*", "_",      "*",
#       "*", MOUNTAIN, "_",
#       "*", "_",      "*"],
#      LAND],
#     [["*", "*",      "*",
#       "_", MOUNTAIN, "_",
#       "*", "_",      "*"],
#      LAND],
#     [["*", "_",      "*",
#       "_", MOUNTAIN, "*",
#       "*", "_",      "*"],
#      LAND],
# ]


apply_shores1 = [
    [["*", "*",   "*",
      "*", OCEAN, "_",
      "*", "_",  MOUNTAIN],
     OCEAN],

    [["*", "*",    "*",
      "_", OCEAN, "*",
      MOUNTAIN, "_",   "*"],
     OCEAN],

    [[MOUNTAIN,  "_",  "*",
      "_", OCEAN, "*",
      "*",  "*",   "*"],
     OCEAN],

    [["*", "_",    MOUNTAIN,
      "*", OCEAN,  "_",
      "*",  "*",   "*"],
     OCEAN],

    [["*",   OCEAN,   "*",
      OCEAN, OCEAN, "_",
      "*",      "_",  "*"],
     SHORE_NW],

    [["*", OCEAN,    "*",
      "_", OCEAN, OCEAN,
      "*", "_",   "*"],
     SHORE_NE],

    [["*",  "_",  "*",
      "_", OCEAN, OCEAN,
      "*", OCEAN,   "*"],
     SHORE_SE],

    [["*",     "_",  "*",
      OCEAN, OCEAN,  "_",
      "*",   OCEAN,  "*"],
     SHORE_SW],
]

apply_shores2 = [
    # [["*", OCEAN,  "*",
    #   "*", "_",   OCEAN,
    #   "*", OCEAN,  "*"],
    #  LAND],

    # [["*", "*",    "*",
    #   OCEAN, "_", OCEAN,
    #   "*", OCEAN,  "*"],
    #  LAND],

    # [["*", OCEAN,  "*",
    #   OCEAN, "_", "*",
    #   "*", OCEAN,  "*"],
    #  LAND],

    # [["*", OCEAN,  "*",
    #   OCEAN, "_", OCEAN,
    #   "*", "*",    "*"],
    #  LAND],

    [["*", "*",   "*",
      "*", "_",  OCEAN,
      "*", OCEAN, "*"],
     SHORE_SE],

    [["*", "*",    "*",
      OCEAN, "_", "*",
      "*", OCEAN,  "*"],
     SHORE_SW],

    [["*", OCEAN,  "*",
      OCEAN, "_", "*",
      "*", "*",    "*"],
     SHORE_NW],

    [["*", OCEAN,  "*",
      "*", "_",   OCEAN,
      "*", "*",    "*"],
     SHORE_NE],
]

apply_shores3 = [
    [["*", "*",   "*",
      "*", OCEAN, "_",
      "*", "*",   "*"],
     SHORE_W],
    [["*",  "*",   "*",
      "_", OCEAN, "*",
      "*",  "*",   "*"],
     SHORE_E],
    [["*", "*",   "*",
      "*", OCEAN, "*",
      "*", "_",  "*"],
     SHORE_N],
    [["*", "_",   "*",
      "*", OCEAN,  "*",
      "*", "*",    "*",],
     SHORE_S],
]

apply_shores4 = [
    [["*", "*",   "*",
      "*", OCEAN, "*",
      "*", DOCK_S,  "*"],
     SHORE_N],
    [["*", "*",   "*",
      "*", OCEAN, "*",
      "*", DOCK_SE,  "*"],
     SHORE_N],
    [["*", "*",   "*",
      "*", OCEAN, DOCK_E,
      "*", "*",   "*"],
     SHORE_W],
    [["*",  "*",   "*",
      DOCK_W, OCEAN, "*",
      "*",  "*",   "*"],
     SHORE_E],
]

mountain_borders = [
    [["*", "*",       "*",
      "*", MOUNTAIN,  "_",
      "*",       "_", "*"],
     MOUNTAIN_SE],

    [["*", "*",       "*",
      "_", MOUNTAIN,  "*",
      "*",       "_", "*"],
     MOUNTAIN_SW],

    [["*", "_",       "*",
      "_", MOUNTAIN,  "*",
      "*",       "*", "*"],
     MOUNTAIN_NW],

    [["*", "_",       "*",
      "*", MOUNTAIN,  "_",
      "*",       "*", "*"],
     MOUNTAIN_NE],


    [["*", "*",       "*",
      "*", MOUNTAIN,  "_",
      "*",       "*", "*"],
     MOUNTAIN_E],

    [["*", "*",       "*",
      "_", MOUNTAIN,  "*",
      "*",       "*", "*"],
     MOUNTAIN_W],

    [["*", "_",       "*",
      "*", MOUNTAIN,  "*",
      "*",       "*", "*"],
     MOUNTAIN_N],

    [["*", "*",       "*",
      "*", MOUNTAIN,  "*",
      "*",       "_", "*"],
     MOUNTAIN_S],
]

river_borders = [
    [["*", "_",   "*",
     "_", RIVER, RIVER,
     "*", RIVER,   "*"],
     RIVER_NW],

    [["*", "_",   "*",
     RIVER, RIVER, "_",
       "*", RIVER,   "*"],
     RIVER_NE],

    [["*",  RIVER,   "*",
     RIVER, RIVER, "_",
       "*", "_",   "*"],
     RIVER_SE],

    [["*",  RIVER,   "*",
      "_",  RIVER, RIVER,
      "*", "_",   "*"],
     RIVER_SW],
]

desert_borders = [
    [[   "*", DESERT, "*",
      DESERT, DESERT, DESERT,
         "*", DESERT, "C"],
     DESERT_SE],

    [["*",    DESERT, "*",
      DESERT, DESERT, DESERT,
         "*",     "C", "*"],
     DESERT_SW],

    [["*",    DESERT, "*",
      DESERT, DESERT, "C",
      "*",    DESERT, "*"],
     DESERT_NE],

    [["*",    DESERT, "*",
      "C",    DESERT, DESERT,
      "*",    DESERT, "*"],
     DESERT_SW],

    [["*",    DESERT, "*",
      "C",    DESERT, DESERT,
      "*",    DESERT, "*"],
     DESERT_NW],

    [["*",    "C",    "*",
      DESERT, DESERT, DESERT,
      "*",    DESERT, "*"],
     DESERT_NE],

    [["C",    DESERT, "*",
      DESERT, DESERT, DESERT,
      "*",    DESERT, "*"],
     DESERT_NW],


    [["*",   "_",  "*",
      "_", DESERT,  "_",
      "*", DESERT,  "*"],
     LAND],

    [["*",  "_",   "*",
      "_", DESERT, DESERT,
      "*",  "_",   "*"],
     LAND],

    [["*", DESERT, "*",
      "_", DESERT, "_",
      "*",  "_",  "*"],
     LAND],

    [["*",   "_",   "*",
      DESERT, DESERT, "_",
      "*",   "_",   "*"],
     LAND],


    [["*", "_",   "*",
     "_", DESERT, DESERT,
     "*", DESERT,   "*"],
     DESERT_NW],

    [["*", "_",   "*",
     DESERT, DESERT, "_",
       "*", DESERT,   "*"],
     DESERT_NE],

    [["*",  DESERT,   "*",
     DESERT, DESERT, "_",
       "*", "_",   "*"],
     DESERT_SE],

    [["*",  DESERT,   "*",
      "_",  DESERT, DESERT,
      "*", "_",   "*"],
     DESERT_SW],
]

marsh_borders = [
    [["*", "_",   "*",
     "_", MARSH, MARSH,
     "*", MARSH,   "*"],
     MARSH_NW],

    [["*", "_",   "*",
     MARSH, MARSH, "_",
       "*", MARSH,   "*"],
     MARSH_NE],

    [["*",  MARSH,   "*",
     MARSH, MARSH, "_",
       "*", "_",   "*"],
     MARSH_SE],

    [["*",  MARSH,   "*",
      "_",  MARSH, MARSH,
      "*", "_",   "*"],
     MARSH_SW],
]

grass_borders = [
    [["*",   "_",  "*",
      "_", GRASS,  "_",
      "*", GRASS,  "*"],
     LAND],

    [["*",  "_",   "*",
      "_", GRASS, GRASS,
      "*",  "_",   "*"],
     LAND],

    [["*", GRASS, "*",
      "_", GRASS, "_",
      "*",  "_",  "*"],
     LAND],

    [["*",   "_",   "*",
      GRASS, GRASS, "_",
      "*",   "_",   "*"],
     LAND],


    [["*", "_",   "*",
     "_", GRASS, GRASS,
     "*", GRASS,   "*"],
     GRASS_NW],

    [["*", "_",   "*",
     GRASS, GRASS, "_",
       "*", GRASS,   "*"],
     GRASS_NE],

    [["*",  GRASS,   "*",
     GRASS, GRASS, "_",
       "*", "_",   "*"],
     GRASS_SE],

    [["*",  GRASS,   "*",
      "_",  GRASS, GRASS,
      "*", "_",   "*"],
     GRASS_SW],
]

forest_borders = [
    [["*", "*",       "*",
      "*", FOREST,  "_",
      "*",       "_", "*"],
     FOREST_SE],

    [["*", "*",       "*",
      "_", FOREST,  "*",
      "*",       "_", "*"],
     FOREST_SW],

    [["*", "_",       "*",
      "_", FOREST,  "*",
      "*",       "*", "*"],
     FOREST_NW],

    [["*", "_",       "*",
      "*", FOREST,  "_",
      "*",       "*", "*"],
     FOREST_NE],


    [["*", "*",       "*",
      "*", FOREST,  "_",
      "*",       "*", "*"],
     FOREST_E],

    [["*", "*",       "*",
      "_", FOREST,  "*",
      "*",       "*", "*"],
     FOREST_W],

    [["*", "_",       "*",
      "*", FOREST,  "*",
      "*",       "*", "*"],
     FOREST_N],

    [["*", "*",       "*",
      "*", FOREST,  "*",
      "*",       "_", "*"],
     FOREST_S],
]
