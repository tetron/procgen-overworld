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
    [None,           None,             DOCK_S,       DOCK_S,             DOCK_S,          None, None],
    [OCEAN,       OCEAN,              OCEAN,        OCEAN,              OCEAN,           OCEAN, OCEAN]
]


ELFLAND_CASTLE = [
    [SMALL_CASTLE_TOP_W, SMALL_CASTLE_TOP_W],
    [ELFLAND_CASTLE_W, ELFLAND_CASTLE_E],
]

ASTOS_CASTLE = [
    [SMALL_CASTLE_TOP_W, SMALL_CASTLE_TOP_W],
    [ASTOS_CASTLE_W, ASTOS_CASTLE_E],
]

ORDEALS_CASTLE = [
    [SMALL_CASTLE_TOP_W, SMALL_CASTLE_TOP_W],
    [ORDEALS_CASTLE_W, ORDEALS_CASTLE_E],
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
    [MELMOND, None],
    [MELMOND, MELMOND]
]

ONRAC_TOWN = [
    [None, None, None],
    [None, ONRAC, ONRAC],
    [None, ONRAC, ONRAC],
    [None, None, None],
]

LEIFEN_CITY = [
    [None, None, CITY_WALL_NW, CITY_WALL_N, CITY_WALL_NE, None, None],
    [None, CITY_WALL_W1, CITY_WALL_W2, LEIFEN, CITY_WALL_E2, CITY_WALL_E1, None],
    [None, CITY_WALL_W3, LEIFEN, LEIFEN, LEIFEN, CITY_WALL_E3, None],
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
    [None, GAIA, GAIA],
    [GAIA, GAIA, None],
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
    [None, DESERT_NW, DESERT_NE],
    [DESERT_NW, CARAVAN_DESERT, DESERT_SE],
    [DESERT_SW, DESERT_SE, None]
]

NS_DOCK = [
    [DOCK_W, OCEAN],
    [DOCK_W, OCEAN],
    [DOCK_W, OCEAN],
]

EW_DOCK = [
    [DOCK_S, DOCK_S, DOCK_S],
    [OCEAN,   OCEAN,  OCEAN],
]
