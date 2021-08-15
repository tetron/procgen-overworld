from ff1tiles import *

CONERIA_CITY = [
    [None, None, None,                 None,                None,  None, None, None],
    [None, None, None, CONERIA_CASTLE_TOP_W, CONERIA_CASTLE_TOP_E, None, None, None],
    [None, None, CITY_WALL_NW, CONERIA_CASTLE_MID_W, CONERIA_CASTLE_MID_E, CITY_WALL_NE, None, None],
    [None, CITY_WALL_W1, CITY_WALL_W2, CONERIA_CASTLE_ENTRANCE_W, CONERIA_CASTLE_ENTRANCE_E, CITY_WALL_E2, CITY_WALL_E1, None],
    [None, CITY_WALL_W3, CONERIA, CITY_PAVED, CITY_PAVED, CONERIA, CITY_WALL_E3, None],
    [None, CITY_WALL_W4, CONERIA, CITY_PAVED, CITY_PAVED, CONERIA, CITY_WALL_E4, None],
    [None, CITY_WALL_W5, CONERIA, CITY_PAVED, CITY_PAVED, CONERIA, CITY_WALL_E5, None],
    [None, CITY_WALL_SW2, CITY_WALL_GATE_W, CITY_PAVED, CITY_PAVED, CITY_WALL_GATE_E, CITY_WALL_SE2, None],
    [None, None, LAND,                 LAND,                LAND,  LAND, None, None],
    ]

TEMPLE_OF_FIENDS = [
    [None, None,      None,      None, None, None],
    [None, None, TOF_TOP_W, TOF_TOP_E, None, None],
    [None, TOF_BOTTOM_W, TOF_ENTRANCE_W, TOF_ENTRANCE_E, TOF_BOTTOM_E, None],
    [None, None,      LAND,      LAND, None, None],
]

# PRAVOKA_CITY = [
#     [None, None, CITY_WALL_NW, CITY_WALL_N, CITY_WALL_NE, None, None],
#     [None, CITY_WALL_W1, CITY_WALL_W2, PRAVOKA, CITY_WALL_E2, CITY_WALL_E1, None],
#     [None, CITY_WALL_W3, PRAVOKA, CITY_PAVED, PRAVOKA, CITY_WALL_E3, None],
#     [None, CITY_WALL_SW1, CITY_WALL_GATE_W, CITY_PAVED, CITY_WALL_GATE_E, CITY_WALL_SE1, None],
#     [None,          None,             DOCK_S,       DOCK_S,             DOCK_S,          None, None]
# ]


PRAVOKA_CITY = [
    [None, None, None, None, None, None, None],
    [None, None, CITY_WALL_NW, CITY_WALL_N, CITY_WALL_NE, None, None],
    [None, CITY_WALL_W1, CITY_WALL_W2, PRAVOKA, CITY_WALL_E2, CITY_WALL_E1, None],
    [None, CITY_WALL_W3, PRAVOKA, CITY_PAVED, PRAVOKA, CITY_WALL_E3, None],
    [None, CITY_WALL_SW1, CITY_WALL_GATE_W, CITY_PAVED, CITY_WALL_GATE_E, CITY_WALL_SE1, None],
    [None,          LAND,             DOCK_S,       DOCK_S,             DOCK_S,          LAND, None],
    [OCEAN,       OCEAN,              OCEAN,        OCEAN,              OCEAN,           OCEAN, OCEAN]
]


PRAVOKA_CITY_MOAT = [
    [None, None, None,         None,        None,         None, None, None, None, None, None],
    [None, OCEAN, OCEAN,       OCEAN,              OCEAN,        OCEAN,              OCEAN,           OCEAN, OCEAN, OCEAN, None],
    [None, OCEAN, None, None,         None,        None,         None, None, None, OCEAN, None],
    [None, OCEAN, None, None, CITY_WALL_NW, CITY_WALL_N, CITY_WALL_NE, None, None, OCEAN, None],
    [None, OCEAN, None, CITY_WALL_W1, CITY_WALL_W2, PRAVOKA, CITY_WALL_E2, CITY_WALL_E1, None, OCEAN, None],
    [None, OCEAN, None, CITY_WALL_W3, PRAVOKA, CITY_PAVED, PRAVOKA, CITY_WALL_E3, None, OCEAN, None],
    [None, OCEAN, None, CITY_WALL_SW1, CITY_WALL_GATE_W, CITY_PAVED, CITY_WALL_GATE_E, CITY_WALL_SE1, None, OCEAN, None],
    [None, OCEAN, None,          LAND,             DOCK_S,       DOCK_S,             DOCK_S,          LAND, None, OCEAN, None],
    [OCEAN, OCEAN, OCEAN,       OCEAN,              OCEAN,        OCEAN,              OCEAN,           OCEAN, OCEAN, OCEAN, OCEAN]
]


ELFLAND_CASTLE = [
    [SMALL_CASTLE_TOP_W, SMALL_CASTLE_TOP_W],
    [ELFLAND_CASTLE_W, ELFLAND_CASTLE_E],
]

ASTOS_CASTLE = [
    [None, SMALL_CASTLE_TOP_W, SMALL_CASTLE_TOP_W, None],
    [None, ASTOS_CASTLE_W, ASTOS_CASTLE_E, None],
    [None, None, None, None],
]

ORDEALS_CASTLE = [
    [None, SMALL_CASTLE_TOP_W, SMALL_CASTLE_TOP_W, None],
    [None, ORDEALS_CASTLE_W, ORDEALS_CASTLE_E, None],
    [None, None, None, None],
]

ELFLAND_TOWN = [
    [ELFLAND, None, None, ELFLAND],
    [ELFLAND, None, None, ELFLAND],
]

ELFLAND_TOWN_CASTLE = [
    [None, LAND, LAND, LAND, LAND, None],
    [LAND, LAND, SMALL_CASTLE_TOP_W, SMALL_CASTLE_TOP_W, LAND, LAND],
    [LAND, ELFLAND, ELFLAND_CASTLE_W, ELFLAND_CASTLE_E, ELFLAND, LAND],
    [LAND, ELFLAND, LAND, LAND, ELFLAND, LAND],
    [LAND, LAND, LAND, LAND, LAND, LAND],
]


MELMOND_TOWN = [
    [None, MELMOND, None,    None],
    [None, MELMOND, MELMOND, None],
    [None, None, None,    None],
]

ONRAC_TOWN = [
    [None, None, None],
    [None, ONRAC, ONRAC],
    [None, ONRAC, ONRAC],
    [None, None, None],
]

LEFEIN_CITY = [
    [None, None, CITY_WALL_NW, CITY_WALL_N, CITY_WALL_NE, None, None],
    [None, CITY_WALL_W1, CITY_WALL_W2, LEFEIN, CITY_WALL_E2, CITY_WALL_E1, None],
    [None, CITY_WALL_W3, LEFEIN, LEFEIN, LEFEIN, CITY_WALL_E3, None],
    [None, CITY_WALL_SW1, CITY_WALL_GATE_W, CITY_PAVED, CITY_WALL_GATE_E, CITY_WALL_SE1, None],
]

CRESCENT_LAKE_CITY = [
    [None, None, None,         None,        None,         None, None],
    [None, None, CITY_WALL_NW, CITY_WALL_N, CITY_WALL_NE, None, None],
    [None, CITY_WALL_W1, CITY_WALL_W2, CITY_PAVED, CITY_WALL_E2, CITY_WALL_E1, None],
    [None, CITY_WALL_W3, CITY_PAVED, CRESCENT_LAKE, CRESCENT_LAKE, CITY_WALL_E3, None],
    [None, CITY_WALL_W4, CRESCENT_LAKE, CITY_PAVED, CRESCENT_LAKE, CITY_WALL_E4, None],
    [None, CITY_WALL_W5, CRESCENT_LAKE, CITY_PAVED, CITY_PAVED, CITY_WALL_E5, None],
    [None, CITY_WALL_SW2, CITY_WALL_GATE_W, CITY_PAVED, CITY_WALL_GATE_E, CITY_WALL_SE2, None],
    [None,          None,             LAND,       LAND,             LAND, None, None],
    ]

GAIA_TOWN = [
    [LAND, GAIA, GAIA],
    [GAIA, GAIA, LAND],
    [LAND, LAND, None],
]

MIRAGE_TOWER = [
    [None, None, None, None],
    [None, MIRAGE_TOP, DESERT, None, ],
    [None, MIRAGE_BOTTOM, MIRAGE_SHADOW, None, ],
    [None, None, None, None],
    ]

VOLCANO = [
    [None,  RIVER, RIVER,                   RIVER, RIVER, None],
    [RIVER, RIVER, LAND,                     LAND, RIVER, RIVER],
    [RIVER, LAND,  VOLCANO_TOP_W,   VOLCANO_TOP_E, LAND,  RIVER],
    [RIVER, LAND,  VOLCANO_BASE_W, VOLCANO_BASE_E, LAND,  RIVER],
    [RIVER, RIVER, LAND,                     LAND, RIVER, RIVER],
    [None,  RIVER, RIVER,                   RIVER, RIVER, None],
]

OASIS = [
    [DESERT_SE, DESERT_NW,      DESERT_NE, FOREST, FOREST],
    [DESERT_NW, CARAVAN_DESERT, DESERT_SE, FOREST, FOREST],
    [DESERT_SW, DESERT_SE,      FOREST, FOREST, FOREST],
    [DESERT_NE,                 FOREST, FOREST, FOREST],
    [     None,                 FOREST, FOREST, None]
]

N_DOCK_STRUCTURE = [
    [DOCK_E,  OCEAN, None],
    [DOCK_E,  OCEAN, None],
    [DOCK_E,  OCEAN, None],
]

S_DOCK_STRUCTURE = [
    [DOCK_S, DOCK_S, DOCK_S],
    [OCEAN,   OCEAN,  OCEAN],
]

W_DOCK_STRUCTURE = [
    [DOCK_S, DOCK_S,  DOCK_SW],
    [OCEAN,   OCEAN,  DOCK_W],
]

E_DOCK_STRUCTURE = [
    [DOCK_SE, DOCK_S, DOCK_S],
    [DOCK_E,   OCEAN,  OCEAN],
]

E_CANAL_STRUCTURE = [
    [DOCK_SE, DOCK_S, DOCK_S, None, None,    None],
    [DOCK_E,   OCEAN,  OCEAN, OCEAN, OCEAN, OCEAN],
    [None,     None,   None,  None,  None,  None],
]

W_CANAL_STRUCTURE = [
    [None, None,    None, DOCK_S, DOCK_S,  DOCK_SW],
    [OCEAN,   OCEAN,  OCEAN, OCEAN, OCEAN, DOCK_W],
    [None,     None,   None,  None,  None,  None],
]

ICE_CAVE_FEATURE = [
    [None, None, None, None, None],
    [None, None, ICE_CAVE, None, None],
    [None, GRASS, GRASS, GRASS, None],
    [None, GRASS, GRASS, GRASS, None],
]

AIRSHIP_FEATURE = [
    [None,        None,      None,         None,           None,         None,        None,        None, None],
    [None, MOUNTAIN, MOUNTAIN, MOUNTAIN, MOUNTAIN, MOUNTAIN, MOUNTAIN, MOUNTAIN, None],
    [None, MOUNTAIN,  MOUNTAIN,   MOUNTAIN, MOUNTAIN, MOUNTAIN, MOUNTAIN, MOUNTAIN, None],
    [None, MOUNTAIN, MOUNTAIN,  DESERT_NW,  AIRSHIP_DESERT, DESERT_NE, MOUNTAIN, MOUNTAIN, None],
    [None, MOUNTAIN, MOUNTAIN,  DESERT_SW,  AIRSHIP_DESERT, DESERT_SE, MOUNTAIN, MOUNTAIN, None],
    [None, MOUNTAIN, MOUNTAIN,  MOUNTAIN,  AIRSHIP_DESERT, MOUNTAIN, MOUNTAIN, MOUNTAIN, None],
    [None, MOUNTAIN, MOUNTAIN,  MOUNTAIN,  AIRSHIP_DESERT, MOUNTAIN, MOUNTAIN, MOUNTAIN, None],
    [None,        None,      None,         None,           None,         None,        None,        None],
]
