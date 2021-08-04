import random
import math
import PIL.Image

perturb_reduction = .60
minimum_rect = 1
map_size = 256
land_pct = .20
mountain_pct = 0.03
midp_rand = 0

LAND = 0x00
CORNERIA_CASTLE_ENTRANCE_W = 0x01
CORNERIA_CASTLE_ENTRANCE_E = 0x02
FOREST_NW = 0x03
FOREST_N = 0x04
FOREST_NE = 0x05
SHORE_SE = 0x06
SHORE_S = 0x07
SHORE_SW = 0x08
CORNERIA_CASTLE_TOP_W = 0x09
CORNERIA_CASTLE_TOP_E = 0x0A
SMALL_CASTLE_TOP_W = 0x0B
SMALL_CASTLE_TOP_E = 0x0C
MIRAGE_TOP = 0x0D
EARTH_CAVE = 0x0E
DOCK_W = 0x0F
MOUNTAIN_NW = 0x10
MOUNTAIN_N = 0x11
MOUNTAIN_NE = 0x12
FOREST_W = 0x13
FOREST = 0x14
FOREST_E = 0x15
SHORE_E = 0x16
SEA = 0x17
SHORE_W = 0x18
CORNERIA_CASTLE_MID_W = 0x19
CORNERIA_CASTLE_MID_E = 0x1A
ELFLAND_CASTLE_W = 0x1B
ELFLAND_CASTLE_W = 0x1C
MIRAGE_BOTTOM = 0x1D
MIRAGE_SHADOW = 0x1E
DOCK_E = 0x1F
MOUNTAIN_W = 0x20
MOUNTAIN = 0x21
MOUNTAIN_E = 0x22
FOREST_SW = 0x23
FOREST_S = 0x24
FOREST_SE = 0x25
SHORE_NE = 0x26
SHORE_N = 0x27
SHORE_NW = 0x28
ASTOS_CASTLE_W = 0x29
ASTOS_CASTLE_E = 0x2A
ICE_CAVE = 0x2B
CITY_WALL_NW = 0x2C
CITY_WALL_N = 0x2D
CITY_WALL_NE = 0x2E
DWARF_CAVE = 0x2F
MOUNTAIN_SW = 0x30
MOUNTAIN_S = 0x31
MATOYAS_CAVE = 0x32
MOUNTAIN_SE = 0x33
TITAN_E = 0x34
TITAN_W = 0x35
CARAVAN_DESERT = 0x36
AIRSHIP_DESERT = 0x37
ORDEALS_CASTLE_W = 0x38
ORDEALS_CASTLE_E = 0x39
SARDAS_CAVE = 0x3A
CITY_WALL_W1 = 0x3B
CITY_WALL_W2 = 0x3C
CITY_PAVED = 0x3D
CITY_WALL_E2 = 0x3E
CITY_WALL_E1 = 0x3F
RIVER_NW = 0x40
RIVER_NE = 0x41
DESERT_NW = 0x42
DESERT_NE = 0x43
RIVER = 0x44
DESERT = 0x45
WATERFALL = 0x46
TOF_TOP_W = 0x47
TOF_TOP_E = 0x48
CONERIA = 0x49
PRAVOKA = 0x4A
CITY_WALL_W3 = 0x4B
ELFLAND = 0x4C
MELMOND = 0x4D
CRESCENT_LAKE = 0x4E
CITY_WALL_E3 = 0x4F
RIVER_SW = 0x50
RIVER_SE = 0x51
DESERT_SW = 0x52
DESERT_SE = 0x53
GRASS = 0x54
MARSH = 0x55
TOF_BOTTOM_W = 0x56
TOF_ENTRANCE_W = 0x57
TOF_ENTRANCE_E = 0x58
TOF_BOTTOM_E = 0x59
GAIA = 0x5A
CITY_WALL_W4 = 0x5B
CITY_WALL_SW1 = 0x5C
ONRAC = 0x5D
CITY_WALL_SE1 = 0x5E
CITY_WALL_E4 = 0x5F
GRASS_NW = 0x60
GRASS_NE = 0x61
MARSH_NW = 0x62
MARSH_NE = 0x63
VOLCANO_TOP_W = 0x64
VOLCANO_TOP_E = 0x65
CARDIA_2 = 0x66
CARDIA_3 = 0x67
CARDIA_4 = 0x68
CARDIA_5 = 0x69
CARDIA_1 = 0x6A
CITY_WALL_W5 = 0x6B
BAHAMUTS_CAVE = 0x6C
LEIFEN = 0x6D
MARSH_CAVE = 0x6E
CITY_WALL_E5 = 0x6F
GRASS_SW = 0x70
GRASS_SE = 0x71
MARSH_SW = 0x72
MARSH_SE = 0x73
VOLCANO_BASE_W = 0x74
VOLCANO_BASE_E = 0x75
LAND_NO_FIGHT = 0x76
DOCK_SE = 0x77
DOCK_S = 0x78
DOCK_SW = 0x79
DOCK_SQ = 0x7A
CITY_WALL_SW2 = 0x7B
CITY_WALL_S = 0x7C
CITY_WALL_GATE_W = 0x7D
CITY_WALL_GATE_E = 0x7E
CITY_WALL_SE2 = 0x7F



def perturb_point(basemap, x0, y0, x1, y1, r0):
    #print((x0, y0), (x1, y1), (abs(x0 - x1), abs(y0 - y1)), r0)
    if abs(x0 - x1) <= minimum_rect and abs(y0 - y1) <= minimum_rect:
        return

    if x0+1 == x1-1:
        x2 = x0+1
    elif x0 == x1:
        x2 = x0
    elif x0+1 == x1:
        x2 = x0
    else:
        n = int((x1-x0) * (1-midp_rand) * .5)
        if n == 0:
            n = 1
        x2 = random.randint(x0+n, x1-n)

    # (37, 11) (37, 14) (0, 3) 2.4308653429145085e-63
    # (37, 11)

    if y0+1 == y1-1:
        y2 = y0+1
    elif y0 == y1:
        y2 = y0
    elif y0+1 == y1:
        y2 = y0
    else:
        n = int((y1-y0) * (1-midp_rand) * .5)
        if n == 0:
            n = 1
        y2 = random.randint(y0+n, y1-n)

    #print((x2, y2))

    #x2 = int((x0+x1)/2)
    #y2 = int((y0+y1)/2)

    # middle
    if basemap[y2][x2] is None:
        midp0 = (basemap[y0][x0]+basemap[y1][x0]+basemap[y0][x1]+basemap[y1][x1])/4.0
        basemap[y2][x2] = midp0 + random.uniform(-r0, r0)

    # left middle
    if basemap[y2][x0] is None:
        midp1 = (basemap[y0][x0]+basemap[y1][x0])/2.0
        basemap[y2][x0] = midp1 + random.uniform(-r0, r0)

    # right middle
    if basemap[y2][x1] is None:
        midp2 = (basemap[y0][x1]+basemap[y1][x1])/2.0
        basemap[y2][x1] = midp2 + random.uniform(-r0, r0)

    # top middle
    if basemap[y0][x2] is None:
        midp3 = (basemap[y0][x0]+basemap[y0][x1])/2.0
        basemap[y0][x2] = midp3 + random.uniform(-r0, r0)

    # bottom middle
    if basemap[y1][x2] is None:
        midp4 = (basemap[y1][x0]+basemap[y1][x1])/2.0
        basemap[y1][x2] = midp4 + random.uniform(-r0, r0)

    r0 *= perturb_reduction
    #print("pp0", (x0, y0, x2, y2), (x2, y0, x1, y2), (x0, y2, x2, y1), (x2, y2, x1, y1))
    perturb_point(basemap, x0, y0, x2, y2, r0)
    perturb_point(basemap, x2, y0, x1, y2, r0)
    perturb_point(basemap, x0, y2, x2, y1, r0)
    perturb_point(basemap, x2, y2, x1, y1, r0)

eliminate_tiny_islands = [
    ["_.."
     ".#."
     "...",
     "."],
    ["._."
     ".#."
     "...",
     "."],
    [".._"
     ".#."
     "...",
     "."],
    ["..."
     "_#."
     "...",
     "."],
    ["..."
     ".#_"
     "...",
     "."],
    ["..."
     ".#."
     "_..",
     "."],
    ["..."
     ".#."
     "._.",
     "."],
    ["..."
     ".#."
     ".._",
     "."]]

eliminate_puddles = [
    ["_##"
     "#.#"
     "###",
     "#"],
    ["##_"
     "#.#"
     "###",
     "#"],
    ["###"
     "#.#"
     "_##",
     "#"],
    ["###"
     "#.#"
     "##_",
     "#"],
    ["_#_"
     "#.#"
     "_#_",
     "#"]]

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

expand_shores = [
    ["###"
     "_._"
     "___",
     "#"],
    ["#__"
     "#._"
     "#__",
     "#"],
    ["___"
     "_._"
     "###",
     "#"],
    ["__#"
     "_.#"
     "__#",
     "#"]
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

def check_rule(tilemap, rule, x, y, multi):
    for j in range(0, 3):
        for i in range(0, 3):
            ruletile = rule[0][j*3 + i]
            checktile = tilemap[y+(j-1)][x+(i-1)]
            if checktile == ruletile or (ruletile == "_" and checktile in multi) or ruletile == "*":
                pass
            else:
                return False
    return rule[1]


def apply_filter(tilemap, rules, multi, repeat):
    recur = True
    while recur:
        newtilemap = []
        for x in range(0, map_size):
            newtilemap.append(['.'] * map_size)

        any_rule_matched = False
        for y,row in enumerate(tilemap):
            if y == 0 or y == (map_size-1):
                continue
            for x,tile in enumerate(row):
                if x == 0 or x == (map_size-1):
                    continue
                rep = tilemap[y][x]
                for rule in rules:
                    check = check_rule(tilemap, rule, x, y, multi)
                    if check is not False:
                        rep = check
                        any_rule_matched = True
                        break
                newtilemap[y][x] = rep
        tilemap = newtilemap
        recur = repeat and any_rule_matched

    return tilemap

def savemap(tilemap, colormap, filename):
    img = PIL.Image.new("RGB", (map_size, map_size))

    for y,row in enumerate(tilemap):
        for x,tile in enumerate(row):
            img.putpixel((x, y), colormap[tilemap[y][x]])

    img.save(filename)


def saveffm(tilemap, name):
    tobytes = {
        ".": 0x17,
        "#": 0x00,
        "=": 0x44,
        "M": 0x21,
    }

    with open(name, "wb") as f:
        for y,row in enumerate(tilemap):
            for x,tile in enumerate(row):
                print(tobytes[tilemap[y][x]], end='')
                f.write(bytes([tobytes[tilemap[y][x]]]))


def printmap(tilemap):
    for y,row in enumerate(tilemap):
        for x,tile in enumerate(row):
            print(tilemap[y][x], end='')
        print("")

class Region:
    def __init__(self, tile):
        self.tile = tile
        self.points = []
        self.adjacent = set()

    def __repr__(self):
        return "<'%s' %s %s>" % (self.tile, self.points, self.adjacent)

def find_regions(tilemap):
    regionmap = []
    for x in range(0, map_size):
        regionmap.append([None] * map_size)
    regionlist = [Region('.')]

    working_stack = [(0, 0, 0)]
    pending = []

    while working_stack:
        while working_stack:
            x, y, current_region = working_stack.pop()

            if regionmap[y][x] is not None:
                continue

            regionmap[y][x] = current_region
            regionlist[current_region].points.append((x, y))
            curtile = tilemap[y][x]

            adjacent = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
            for ab in adjacent:
                if ab[0] >= 0 and ab[0] <= (map_size-1) and ab[1] >= 0 and ab[1] <= (map_size-1):
                    next_tile = tilemap[ab[1]][ab[0]]
                    if next_tile == curtile:
                        working_stack.append((ab[0], ab[1], current_region))
                    else:
                        pending.append((ab[0], ab[1], current_region))

        while pending and not working_stack:
            x, y, current_region = pending.pop(0)
            if regionmap[y][x] is None:
                regionlist.append(Region(tilemap[y][x]))
                next_region = len(regionlist)-1
                working_stack.append((x, y, next_region))
            elif regionmap[y][x] != current_region:
                next_region = regionmap[y][x]
            regionlist[current_region].adjacent.add(next_region)
            regionlist[next_region].adjacent.add(current_region)


    #printmap(regionmap)
    #print(regionlist)

    colormap = {}
    for i,_ in enumerate(regionlist):
        colormap[i] = (random.randint(5, 250), random.randint(5, 250), random.randint(5, 250))

    savemap(regionmap, colormap, "map6.png")

    return (regionmap, regionlist)

def remove_small_regions(tilemap, regionlist):
    for r in regionlist:
        if len(r.points) > 5:
            continue

        repl = [regionlist[adj].tile for adj in r.adjacent]
        random.shuffle(repl)
        for p in r.points:
            tilemap[p[1]][p[0]] = repl[0]


def small_seas_become_lakes(tilemap, regionlist):
    for r in regionlist:
        if r.tile != '.':
            continue
        if len(r.points) > 40:
            continue
        for p in r.points:
            tilemap[p[1]][p[0]] = '='

def flow_river(basemap, tilemap, pending):
    volume = 256

    while pending and volume > 0:
        x, y = pending.pop()

        if tilemap[y][x] == '.':
            break

        volume -= 1

        if tilemap[y][x] == '=':
            continue

        tilemap[y][x] = '='

        pending.extend([(x+1, y), (x, y+1), (x-1, y), (x, y-1)])
        pending.sort(key=lambda ab: basemap[ab[1]][ab[0]], reverse=True)
        #print([(ab[0], ab[1], basemap[ab[1]][ab[0]]) for ab in pending])


def procgen():
    basemap = []
    for x in range(0, map_size):
        basemap.append([None] * map_size)

    border = 8
    for b in range(0, border+1):
        for i in range(0, map_size):
            basemap[b][i] = 0
            basemap[map_size-1-b][i] = 0
            basemap[i][b] = 0
            basemap[i][map_size-1-b] = 0
    basemap[map_size//2-1][map_size//2-1] = 0

    perturb_point(basemap, border, border, map_size-1-border, map_size-1-border, 1)

    tilemap = []
    for x in range(0, map_size):
        tilemap.append(['.'] * map_size)

    heightmin = 100
    heightmax = -100
    avg = 0

    for y,row in enumerate(basemap):
        for x,tile in enumerate(row):
            if basemap[y][x] < heightmin:
                heightmin = basemap[y][x]
            if basemap[y][x] > heightmax:
                heightmax = basemap[y][x]
            avg += basemap[y][x]

    avg = avg / (map_size*map_size)

    mountain_elevation = 1-mountain_pct
    sea_elevation = 1-land_pct

    mountain_count = 0
    land_count = 0
    min_land_tiles = (map_size*map_size)*land_pct
    min_mtn_tiles = (map_size*map_size)*mountain_pct

    print("min_land_tiles", min_land_tiles)
    print("min_mtn_tiles", min_mtn_tiles)

    lowering_iter = 0
    while land_count < min_land_tiles or mountain_count < min_mtn_tiles:
        lowering_iter += 1
        mountain_count = 0
        land_count = 0
        for y,row in enumerate(basemap):
            for x,tile in enumerate(row):
                if tile > mountain_elevation:
                    tilemap[y][x] = 'M'
                    mountain_count += 1
                elif tile > sea_elevation:
                    tilemap[y][x] = '#'
                    land_count += 1
                else:
                    tilemap[y][x] = '.'
        if land_count < min_land_tiles:
            sea_elevation -= .005
        if mountain_count < min_mtn_tiles:
            mountain_elevation -= .005
        if sea_elevation <= 0:
            return False

    print("sea_elevation", sea_elevation)
    print("mountain_elevation", mountain_elevation)

    print("Lowering iterations", lowering_iter)

    colormap = {".": (101, 183, 255),
                "=": (178, 229, 255),
                "#": (52, 176, 0),
                "M": (255, 255, 255)}

    savemap(tilemap, colormap, "map1.png")

    # print("filtering islands")
    # tilemap = apply_filter(tilemap, eliminate_tiny_islands, ["#", "."], True)

    print("expanding mountains")
    tilemap = apply_filter(tilemap, expand_mountains, ["#", ".", "M"], False)

    #print("expanding shores")
    #tilemap = apply_filter(tilemap, expand_shores, ["#", "."], False)
    # print("filtering puddles")
    # tilemap = apply_filter(tilemap, eliminate_puddles, ["#", "."], True)

    print("expanding sea")
    tilemap = apply_filter(tilemap, expand_sea, ["#", ".", "M"], False)

    # tilemap = apply_filter(tilemap, eliminate_tiny_islands, ["#", "."], True)

    points = []
    for y,row in enumerate(basemap):
        for x,tile in enumerate(row):
            if tile >= (mountain_elevation + ((heightmax-mountain_elevation)*.5)):
                points.append((x,y))

    random.shuffle(points)
    for p in points[:16]:
        flow_river(basemap, tilemap, [p])

    tilemap = apply_filter(tilemap, connect_diagonals, ["M", "#"], False)

    regionmap, regionlist = find_regions(tilemap)
    remove_small_regions(tilemap, regionlist)

    #tilemap = apply_filter(tilemap, smooth_lakes, ["#", "=", "M"], False)
    tilemap = apply_filter(tilemap, smooth_rivers, ["M", "=", "#"], True)

    regionmap, regionlist = find_regions(tilemap)
    remove_small_regions(tilemap, regionlist)

    savemap(tilemap, colormap, "map4.png")

    regionmap, regionlist = find_regions(tilemap)
    small_seas_become_lakes(tilemap, regionlist)

    savemap(tilemap, colormap, "map5.png")
    saveffm(tilemap, "map5.ffm")

    #printmap(tilemap)

    return True


success = procgen()
while success is False:
    success = procgen()
