import random
import math
import PIL.Image
from ff1features import *
from ff1filters import *

perturb_reduction = .60
minimum_rect = 1
map_size = 256
land_pct = .25
mountain_pct = 0.04
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
    def __init__(self, tile, regionid):
        self.tile = tile
        self.regionid = regionid
        self.points = set()
        self.adjacent = set()
        self.nwcorner = None
        self.secorner = None

    def addpoint(self, x, y):
        self.points.add((x, y))
        if self.nwcorner is None:
            self.nwcorner = (x, y)
        if self.secorner is None:
            self.secorner = (x, y)

        if x < self.nwcorner[0]:
            self.nwcorner = (x, self.nwcorner[1])

        if y < self.nwcorner[1]:
            self.nwcorner = (self.nwcorner[0], y)

        if x > self.secorner[0]:
            self.secorner = (x, self.secorner[1])

        if y > self.secorner[1]:
            self.secorner = (self.secorner[0], y)


    def __repr__(self):
        return "<'%s' %s %s>" % (self.tile, self.points, self.adjacent)

def find_regions(tilemap):
    regionmap = []
    for x in range(0, map_size):
        regionmap.append([None] * map_size)
    regionlist = [Region('.', 0)]

    working_stack = [(0, 0, 0)]
    pending = []

    while working_stack:
        while working_stack:
            x, y, current_region = working_stack.pop()

            if regionmap[y][x] is not None:
                continue

            regionmap[y][x] = current_region
            regionlist[current_region].addpoint(x, y)
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
                regionlist.append(Region(tilemap[y][x], len(regionlist)))
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


def remove_small_islands(tilemap, regionlist):
    candidates = []
    for r in regionlist:
        if len(r.points) > 12:
            continue
        if len(r.adjacent) == 1:
            adj = list(r.adjacent)[0]
            if regionlist[adj].tile == '.':
                candidates.append(r)

    random.shuffle(candidates)

    for r in candidates[:len(candidates)-4]:
        for p in r.points:
            tilemap[p[1]][p[0]] = '.'


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


def render_feature(tilemap, regionmap, feature, x, y):
    for y2,row in enumerate(feature):
        for x2,tile in enumerate(row):
            if feature[y2][x2] is not None:
                tilemap[y+y2][x+x2] = feature[y2][x2]
                regionmap[y+y2][x+x2] = -1

def place_feature_in_region(r, regionmap, tilemap, feature):
    h = len(feature)+2
    w = len(feature[0])+2

    candidates = set()

    for y in range(r.nwcorner[1], r.secorner[1]-h):
        for x in range(r.nwcorner[0], r.secorner[0]-w):
            fits = True
            for y2 in range(y, y+h):
                for x2 in range(x, x+w):
                    if regionmap[y2][x2] != r.regionid:
                        fits = False
                        break
                if not fits:
                    break
            if fits:
                candidates.add((x, y))

    candidates = list(candidates)

    if not candidates:
        return False

    random.shuffle(candidates)

    render_feature(tilemap, regionmap, feature, candidates[0][0]+1, candidates[0][1]+1)
    return True

def place_cave(r, regionmap, tilemap, cave):
    candidates = set()

    for y in range(r.nwcorner[1], r.secorner[1]):
        for x in range(r.nwcorner[0]+1, r.secorner[0]-1):
            if regionmap[y][x] != r.regionid:
                continue
            fits = True
            for x2 in range(x-1, x+2):
                if tilemap[y-1][x2] != MOUNTAIN:
                    fits = False
                    break
            for x2 in range(x-1, x+2):
                if tilemap[y][x2] != LAND:
                    fits = False
                    break
            if fits:
                candidates.add((x, y-1))

    candidates = list(candidates)

    if not candidates:
        return False

    random.shuffle(candidates)

    tilemap[candidates[0][1]][candidates[0][0]] = cave
    return True


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

    print("expanding mountains")
    tilemap = apply_filter(tilemap, expand_mountains, ["#", ".", "M"], False)

    print("expanding sea")
    tilemap = apply_filter(tilemap, expand_sea, ["#", ".", "M"], False)

    points = []
    for y,row in enumerate(basemap):
        for x,tile in enumerate(row):
            if tile >= (mountain_elevation + ((heightmax-mountain_elevation)*.5)):
                points.append((x,y))

    print("flowing rivers")
    random.shuffle(points)
    for p in points[:16]:
        flow_river(basemap, tilemap, [p])

    tilemap = apply_filter(tilemap, connect_diagonals, ["M", "#"], False)

    print("removing small regions")
    regionmap, regionlist = find_regions(tilemap)
    remove_small_regions(tilemap, regionlist)

    print("smoothing rivers")
    tilemap = apply_filter(tilemap, smooth_rivers, ["M", "=", "#"], True)
    tilemap = apply_filter(tilemap, fixup_mountains, ["#", "=", "."], False)

    regionmap, regionlist = find_regions(tilemap)
    remove_small_regions(tilemap, regionlist)

    regionmap, regionlist = find_regions(tilemap)
    remove_small_islands(tilemap, regionlist)

    regionmap, regionlist = find_regions(tilemap)
    small_seas_become_lakes(tilemap, regionlist)

    savemap(tilemap, colormap, "map5.png")

    tilemap = to_ffm(tilemap)

    regionmap, regionlist = find_regions(tilemap)

    features = [CONERIA_CITY, TEMPLE_OF_FIENDS, PRAVOKA_CITY, ELFLAND_TOWN_CASTLE, ASTOS_CASTLE,
                ORDEALS_CASTLE, MELMOND_TOWN, ONRAC_TOWN,
                LEIFEN_CITY, CRESCENT_LAKE_CITY, GAIA_TOWN,
                MIRAGE_TOWER, VOLCANO, OASIS,
                [[MARSH_CAVE]], [[BAHAMUTS_CAVE]], [[CARDIA_1]], [[CARDIA_2]],
                [[CARDIA_3]], [[CARDIA_4]], [[CARDIA_5]]
    ]

    random.shuffle(features)

    landregions = [r for r in regionlist if r.tile == LAND]
    landregions.sort(key=lambda r: len(r.points), reverse=True)
    total = 0
    for r in landregions:
        total += len(r.points)

    ids = list(range(0, len(regionlist)))
    random.shuffle(ids)
    i = 0
    for f in features:
        found = False
        while not found:
            val = random.randint(0, total)
            for r in landregions:
                val -= len(r.points)
                if val <= 0:
                    break
            if place_feature_in_region(r, regionmap, tilemap, f):
                found = True

    caves = [MATOYAS_CAVE, DWARF_CAVE, EARTH_CAVE, TITAN_E, TITAN_W, SARDAS_CAVE, ICE_CAVE]

    for c in caves:
        found = False
        while not found:
            val = random.randint(0, total)
            for r in landregions:
                val -= len(r.points)
                if val <= 0:
                    break
            if place_cave(r, regionmap, tilemap, c):
                found = True

    tilemap = apply_filter(tilemap, mountain_borders, [SEA, RIVER, LAND], False)
    tilemap = apply_filter(tilemap, river_borders, [SEA, LAND,
                                                       MOUNTAIN_NW, MOUNTAIN_N, MOUNTAIN_NE,
                                                       MOUNTAIN_W, MOUNTAIN, MOUNTAIN_E,
                                                       MOUNTAIN_SW, MOUNTAIN_S, MOUNTAIN_SE],
                           False)

    tilemap = apply_filter(tilemap, apply_shores1, [], False)
    tilemap = apply_filter(tilemap, apply_shores2, [], False)
    tilemap = apply_filter(tilemap, apply_shores3, [], False)


    # single tile features
    #
    # matoya's cave
    # dwarf cave
    # marsh cave
    # earth cave
    # sarda's cave
    # titan's tunnel W/E
    # ice cave
    # bahamut's cave
    # cardia 1-5
    # waterfall
    #
    # 14 complex features + 15 simple features +
    #
    # bridge
    # canal
    # airship desert

    # x = 8
    # y = 8
    # for i,_ in enumerate(features):
    #     render_feature(tilemap, features[i], x, y)
    #     x += 8
    #     if x > 255:
    #         y += 8
    #         x = 8

    saveffm(tilemap, "map5.ffm")

    #printmap(tilemap)

    return True


success = procgen()
while success is False:
    success = procgen()
