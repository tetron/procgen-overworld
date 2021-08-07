from ff1tiles import *

expand_mountains = [
    ["M__"
     "___"
     "___",
     "M"],
    ["_M_"
     "___"
     "___",
     "M"],
    ["__M"
     "___"
     "___",
     "M"],
    ["___"
     "M__"
     "___",
     "M"],
    ["___"
     "__M"
     "___",
     "M"],
    ["___"
     "___"
     "M__",
     "M"],
    ["___"
     "___"
     "_M_",
     "M"],
    ["___"
     "___"
     "__M",
     "M"]
]


expand_sea = [
    [".__"
     "___"
     "___",
     "."],
    ["_._"
     "___"
     "___",
     "."],
    ["__."
     "___"
     "___",
     "."],
    ["___"
     ".__"
     "___",
     "."],
    ["___"
     "__."
     "___",
     "."],
    ["___"
     "___"
     ".__",
     "."],
    ["___"
     "___"
     "_._",
     "."],
    ["___"
     "___"
     "__.",
     "."]
]

smooth_rivers = [
    ["_=_"
     "M=M"
     "MMM",
     "M"],
    ["MM_"
     "M=="
     "MM_",
     "M"],
    ["MMM"
     "M=M"
     "_=_",
     "M"],
    ["_MM"
     "==M"
     "_MM",
     "M"],
    ["_=_"
     "#=#"
     "###",
     "#"],
    ["##_"
     "#=="
     "##_",
     "#"],
    ["###"
     "#=#"
     "_=_",
     "#"],
    ["_##"
     "==#"
     "_##",
     "#"],
    ["_M_"
     "=M="
     "===",
     "="],
    ["==_"
     "=MM"
     "==_",
     "="],
    ["==="
     "=M="
     "_M_",
     "="],
    ["_=="
     "MM="
     "_==",
     "="],
]

fixup_mountains = [
    [["*", "_", "*",
      "_", "M", "_",
      "*", "*", "*"],
     "#"],
    [["*", "_", "*",
      "*", "M", "_",
      "*", "_", "*"],
     "#"],
    [["*", "*", "*",
      "_", "M", "_",
      "*", "_", "*"],
     "#"],
    [["*", "_", "*",
      "_", "M", "*",
      "*", "_", "*"],
     "#"],
]

connect_diagonals = [
    ["*=_"
     "*_="
     "***",
     "="],
    ["_=*"
     "=_*"
     "***",
     "="],
    ["*._"
     "*_."
     "***",
     "."],
    ["_.*"
     "._*"
     "***",
     "."],
    ["*M_"
     "*_M"
     "***",
     "M"],
    ["_M*"
     "M_*"
     "***",
     "M"],
]

apply_shores1 = [
    [["*", "*", "*",
      "*", SEA, LAND,
      "*", LAND, "*"],
     SHORE_NW],

    [["*", "*",  "*",
      LAND, SEA, "*",
      "*", LAND, "*"],
     SHORE_NE],

    [["*",  LAND,  "*",
      LAND, SEA, "*",
      "*",  "*", "*"],
     SHORE_SE],

    [["*", LAND, "*",
      "*", SEA,  LAND,
      "*",  "*", "*"],
     SHORE_SW],
]

apply_shores2 = [
    [["*", SEA,  "*",
      "*", LAND, SEA,
      "*", SEA, "*"],
     LAND],

    [["*", "*",  "*",
      SEA, LAND, SEA,
      "*", SEA, "*"],
     LAND],

    [["*", SEA,  "*",
      SEA, LAND, "*",
      "*", SEA, "*"],
     LAND],

    [["*", SEA,  "*",
      SEA, LAND, SEA,
      "*", "*", "*"],
     LAND],

    [["*", "*",  "*",
      "*", LAND, SEA,
      "*", SEA, "*"],
     SHORE_SE],

    [["*", "*",  "*",
      SEA, LAND, "*",
      "*", SEA, "*"],
     SHORE_SW],

    [["*", SEA,  "*",
      SEA, LAND, "*",
      "*", "*", "*"],
     SHORE_NW],

    [["*", SEA,  "*",
      "*", LAND, SEA,
      "*", "*", "*"],
     SHORE_NE],
]

apply_shores3 = [
    [["*", "*", "*",
      "*", SEA, LAND,
      "*", "*", "*"],
     SHORE_W],
    [["*",  "*", "*",
      LAND, SEA, "*",
      "*",  "*", "*"],
     SHORE_E],
    [["*", "*", "*",
      "*", SEA, "*",
      "*", LAND, "*"],
     SHORE_N],
    [["*", LAND, "*",
      "*", SEA,  "*",
      "*", "*",  "*",],
     SHORE_S],
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
