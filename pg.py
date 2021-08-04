import random
import math
import PIL.Image
from ff1features import *

perturb_reduction = .60
minimum_rect = 1
map_size = 256
land_pct = .20
mountain_pct = 0.03
midp_rand = 0

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

apply_shores = [
    [["*", SEA, LAND,
      "*", SEA, LAND,
      "*", SEA, LAND],
     SHORE_W],
    [[LAND, SEA, "*",
      LAND, SEA, "*",
      LAND, SEA, "*"],
     SHORE_E],
    [["*", "*", "*",
      SEA, SEA, SEA,
      LAND, LAND, LAND],
     SHORE_N],
    [[LAND, LAND, LAND,
       SEA, SEA, SEA,
       "*", "*", "*",],
     SHORE_S],
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
            newtilemap.append([tilemap[0][0]] * map_size)

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
    with open(name, "wb") as f:
        for y,row in enumerate(tilemap):
            for x,tile in enumerate(row):
                f.write(bytes([tilemap[y][x]]))


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


def to_ffm(tilemap):
    to_tileid = {
        ".": SEA,
        "#": LAND,
        "M": MOUNTAIN,
        "=": RIVER,
    }
    for y,row in enumerate(tilemap):
        for x,tile in enumerate(row):
            tilemap[y][x] = to_tileid[tilemap[y][x]]
    return tilemap


def render_feature(tilemap, feature, x, y):
    for y2,row in enumerate(feature):
        for x2,tile in enumerate(row):
            if feature[y2][x2] is not None:
                tilemap[y+y2][x+x2] = feature[y2][x2]

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

    tilemap = to_ffm(tilemap)

    #render_feature(tilemap, VANILLA_CORNERIA, 8, 8)

    tilemap = apply_filter(tilemap, apply_shores, [], False)

    saveffm(tilemap, "map5.ffm")

    #printmap(tilemap)

    return True


success = procgen()
while success is False:
    success = procgen()
