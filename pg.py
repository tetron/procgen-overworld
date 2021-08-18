import random
import math
import json
import functools
import copy
import collections
import PIL.Image
from ff1features import *
from ff1filters import *

perturb_reduction = .63
minimum_rect = 1
map_size = 256
land_pct = .26
mountain_pct = 0.055
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
            if (checktile == ruletile) or (ruletile in multi and checktile in multi[ruletile]):
                pass
            else:
                return False
    return rule[1]


def check_salient(tile_region_type, tilemap, rule, x, y, multi):
    tile = tile_region_type[tilemap[y][x]]

    if tile in (LAND_REGION, OCEAN_REGION, MISC_REGION):
        return False

    counts = {}
    for t in [(x, y-1), (x, y+1), (x-1, y), (x+1, y)]:
        tile = tile_region_type[tilemap[t[1]][t[0]]]
        if tile in counts:
            counts[tile] += 1
        else:
            counts[tile] = 1

    tile = tile_region_type[tilemap[y][x]]

    for k,v in counts.items():
        if (v == 3 or v == 4) and k != tile:
            # Surrounded on 3 or 4 sides, convert to the tile type
            # surrounding it
            if k == OCEAN_REGION:
                return LAND
            if k == MISC_REGION:
                return False
            return pre_shore_region_types[k][0]

    if tile in (MOUNTAIN_REGION, FOREST_REGION):
        if counts.get(tile, 0) < 2:
            return LAND

    return False


def apply_filter(tilemap, rules, multi, repeat, matcher=check_rule):
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
                    check = matcher(tilemap, rule, x, y, multi)
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


def find_regions(tilemap, tile_region_type):
    regionmap = []
    for x in range(0, map_size):
        regionmap.append([None] * map_size)
    regionlist = [Region(tile_region_type[OCEAN], 0)]

    working_stack = [(0, 0, 0)]
    pending = collections.deque()

    while working_stack:
        while working_stack:
            x, y, current_region = working_stack.pop()

            if regionmap[y][x] is not None:
                continue

            regionmap[y][x] = current_region
            regionlist[current_region].addpoint(x, y)
            curtile = tile_region_type[tilemap[y][x]]

            adjacent = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
            for ab in adjacent:
                if ab[0] >= 0 and ab[0] <= (map_size-1) and ab[1] >= 0 and ab[1] <= (map_size-1):
                    next_tile = tile_region_type[tilemap[ab[1]][ab[0]]]
                    if next_tile == curtile:
                        working_stack.append((ab[0], ab[1], current_region))
                    else:
                        pending.append((ab[0], ab[1], current_region))

        while pending and not working_stack:
            x, y, current_region = pending.popleft()
            if regionmap[y][x] is None:
                regionlist.append(Region(tile_region_type[tilemap[y][x]], len(regionlist)))
                next_region = len(regionlist)-1
                working_stack.append((x, y, next_region))
            elif regionmap[y][x] != current_region:
                next_region = regionmap[y][x]
            regionlist[current_region].adjacent.add(next_region)
            regionlist[next_region].adjacent.add(current_region)

    colormap = {}
    for i,_ in enumerate(regionlist):
        colormap[i] = (random.randint(5, 250), random.randint(5, 250), random.randint(5, 250))

    savemap(regionmap, colormap, "map6.png")

    return (regionmap, regionlist)

def remove_small_regions(tilemap, regionlist):
    for r in regionlist:
        if len(r.points) > 5:
            continue

        repl = [pre_shore_region_types[regionlist[adj].tile][0] for adj in r.adjacent]
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
            if regionlist[adj].tile == OCEAN_REGION:
                candidates.append(r)

    random.shuffle(candidates)

    for r in candidates[:len(candidates)-4]:
        for p in r.points:
            tilemap[p[1]][p[0]] = OCEAN


def small_seas_become_lakes(tilemap, regionlist):
    for r in regionlist:
        if r.tile != OCEAN_REGION:
            continue
        if len(r.points) > 40:
            continue
        for p in r.points:
            tilemap[p[1]][p[0]] = RIVER

def flow_river(basemap, tilemap, pending):
    volume = 256

    while pending and volume > 0:
        x, y = pending.pop()

        if tilemap[y][x] == OCEAN:
            break

        volume -= 1

        if tilemap[y][x] == RIVER:
            continue

        tilemap[y][x] = RIVER

        pending.extend([(x+1, y), (x, y+1), (x-1, y), (x, y-1)])
        pending.sort(key=lambda ab: basemap[ab[1]][ab[0]], reverse=True)
        #print([(ab[0], ab[1], basemap[ab[1]][ab[0]]) for ab in pending])

def flow_rivers(basemap, tilemap, lower_elev, upper_elev, count):
    points = []
    for y,row in enumerate(basemap):
        for x,tile in enumerate(row):
            if tile >= lower_elev and tile <= upper_elev:
                points.append((x,y))

    random.shuffle(points)
    for p in points[:count]:
        flow_river(basemap, tilemap, [p])


def render_feature(tilemap, weightmap, feature, x, y):
    for y2,row in enumerate(feature):
        for x2,tile in enumerate(row):
            if feature[y2][x2] is not None:
                tilemap[y+y2][x+x2] = feature[y2][x2]

    y += len(feature)//2
    x += len(feature[0])//2

    radius = 20
    for y2 in range(y-radius, y+radius+1):
        for x2 in range(x-radius, x+radius+1):
            if x2<0 or x2>(map_size-1) or y2<0 or y2>(map_size-1):
                continue
            dist = int(math.sqrt((x-x2)*(x-x2) + (y-y2)*(y-y2)))
            if dist <= radius:
                weightmap[y2][x2] += (radius - dist)

def check_fit(regionmap, r, x, y, h, w):
    fits = True
    for y2 in range(y, y+h):
        for x2 in range(x, x+w):
            if regionmap[y2][x2] != r.regionid:
                fits = False
                break
        if not fits:
            break
    return fits

def place_feature_in_region(self, r, regionmap, maxweight, feature, place_at=None):
    h = len(feature)
    w = len(feature[0])

    candidate = None
    if place_at is not None:
        if check_fit(regionmap, r, place_at[0], place_at[1], h, w):
            candidate = place_at
    else:
        #for y in range(r.nwcorner[1], r.secorner[1]-h):
        #    for x in range(r.nwcorner[0], r.secorner[0]-w):
        points = list(r.points)
        random.shuffle(points)

        maxweight = 10
        weight = 0
        while candidate is None and weight < maxweight:
            for p in points:
                if self.weightmap[p[1]+(h//2)][p[0]+(w//2)] > weight:
                    continue
                if check_fit(regionmap, r, p[0], p[1], h, w):
                    candidate = p
                    break
            weight += 1

    if not candidate:
        return False

    render_feature(self.tilemap, self.weightmap, feature, candidate[0], candidate[1])
    fix_regionmap(self.traversable_regionmap, feature, candidate[0], candidate[1], -1)
    fix_regionmap(self.biome_regionmap, feature, candidate[0], candidate[1], -1)
    return candidate

def fix_regionmap(regionmap, feature, x, y, new_region):
    for y2,row in enumerate(feature):
        for x2,tile in enumerate(row):
            if feature[y2][x2] is not None:
                regionmap[y+y2][x+x2] = new_region

def place_cave(r, regionmap, tilemap, weightmap, maxweight, cave):
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
            if tilemap[y][x] not in (LAND, MARSH, FOREST, DESERT, GRASS):
                fits = False
            if fits:
                candidates.add((x, y-1))

    candidates = list(candidates)

    if not candidates:
        return False

    random.shuffle(candidates)
    candidates.sort(key=lambda n: weightmap[n[1]][n[0]])
    if weightmap[candidates[0][1]][candidates[0][0]] > maxweight:
        return False

    render_feature(tilemap, weightmap, [[cave]], candidates[0][0], candidates[0][1])
    return (candidates[0][0], candidates[0][1])


def splat(tilemap, x, y, biometype):
    sz = random.randint(200, 400)

    pending = [(x, y)]

    while sz > 0 and pending:
        x, y = pending.pop(random.randint(0, len(pending)-1))

        if tilemap[y][x] not in [LAND, RIVER, RIVER_NW, RIVER_NE, RIVER_SW, RIVER_SE]:
            continue

        if tilemap[y][x] == LAND:
            tilemap[y][x] = biometype
        sz -= 1

        pending.append((x-1, y))
        pending.append((x+1, y))
        pending.append((x, y-1))
        pending.append((x, y+1))


def add_biomes(tilemap, landregions):
    biomes = [FOREST, FOREST, GRASS, MARSH, DESERT]
    for r in landregions:
        for i in range(0, len(r.points)//100 + 1):
            b = random.randint(0, len(biomes)-1)
            pts = list(r.points)
            p = random.randint(0, len(pts)-1)
            splat(tilemap, pts[p][0], pts[p][1], biomes[b])

    return tilemap

def apply_shores(tilemap):
    all_tiles = set(ALL_TILES)
    non_water_tiles = all_tiles.difference([OCEAN, RIVER, SHORE_N, SHORE_E, SHORE_S, SHORE_W,
                                            DOCK_W, DOCK_E, DOCK_SE, DOCK_S, DOCK_SW, DOCK_SQ
    ])
    non_ocean_shore_tiles = all_tiles.difference([OCEAN, RIVER, SHORE_NW, SHORE_NE, SHORE_SW, SHORE_SE,
                                                  DOCK_W, DOCK_E, DOCK_SE, DOCK_S, DOCK_SW, DOCK_SQ])
    tilemap = apply_filter(tilemap, apply_shores1, {"*": all_tiles, "_": non_water_tiles}, False)
    tilemap = apply_filter(tilemap, apply_shores2, {"*": all_tiles, "_": non_water_tiles}, False)
    tilemap = apply_filter(tilemap, apply_shores3, {"*": all_tiles, "_": non_ocean_shore_tiles}, False)
    tilemap = apply_filter(tilemap, apply_shores4, {"*": all_tiles, "_": non_ocean_shore_tiles}, False)

    return tilemap

def apply_borders(tilemap):
    all_tiles = set(ALL_TILES)

    non_desert_tiles = all_tiles.difference([DESERT, DESERT_NW, DESERT_NE, DESERT_SW, DESERT_SE, MIRAGE_TOP, MIRAGE_BOTTOM, MIRAGE_SHADOW])
    non_marsh_tiles = all_tiles.difference([MARSH, MARSH_NW, MARSH_NE, MARSH_SW, MARSH_SE])
    non_grass_tiles = all_tiles.difference([GRASS, GRASS_NW, GRASS_NE, GRASS_SW, GRASS_SE])
    non_forest_tiles = all_tiles.difference([FOREST_NW, FOREST_N, FOREST_NE, FOREST_W, FOREST,
                                             FOREST_E, FOREST_SW, FOREST_S, FOREST_SE])
    non_mountain_tiles = all_tiles.difference([MOUNTAIN, EARTH_CAVE, ICE_CAVE, DWARF_CAVE, MATOYAS_CAVE, SARDAS_CAVE, TITAN_CAVE_E, TITAN_CAVE_W])
    non_water_tiles = all_tiles.difference([OCEAN, RIVER, SHORE_N, SHORE_E, SHORE_S, SHORE_W])
    pit_caves = [BAHAMUTS_CAVE, CARDIA_1, CARDIA_2, CARDIA_3, CARDIA_4, CARDIA_5]

    tilemap = apply_filter(tilemap, mountain_borders, {"_": non_mountain_tiles, "*": all_tiles}, False)
    tilemap = apply_filter(tilemap, river_borders, {"_": non_water_tiles,
                                                    "*": all_tiles},
                           False)

    tilemap = apply_filter(tilemap, desert_borders, {"_": non_desert_tiles, "*": all_tiles, "C": pit_caves}, False)
    tilemap = apply_filter(tilemap, marsh_borders,  {"_": non_marsh_tiles, "*": all_tiles}, False)
    tilemap = apply_filter(tilemap, grass_borders,  {"_": non_grass_tiles, "*": all_tiles}, False)
    tilemap = apply_filter(tilemap, forest_borders, {"_": non_forest_tiles, "*": all_tiles}, False)

    return tilemap

def airship_accessible(region, tilemap, regionlist, checked=None):
    if checked is None:
        checked = []
    if region.regionid in checked:
        return False
    checked.append(region.regionid)
    for p in region.points:
        if tilemap[p[1]][p[0]] in (LAND, GRASS):
            return True
    for adj in region.adjacent:
        if regionlist[adj].tile == CANOE_REGION:
            if airship_accessible(regionlist[adj], tilemap, regionlist, checked):
                return True

    return False

def pit_cave_feature(cave):
    return [[None, None, None],
            [None, cave, None],
            [None, None, None]]

def dup_tilemap(tilemap):
    newtilemap = []
    for y,row in enumerate(tilemap):
        newtilemap.append(list(tilemap[y]))
    return newtilemap

def get_subregions(region, other_regionmap):
    subregions = set()
    for p in region.points:
        oth = other_regionmap[p[1]][p[0]]
        if oth != -1:
            subregions.add(oth)
    return subregions

def place_in_random_region(self, subregions, biome_regionmap, weight, feature):
    random.shuffle(subregions)
    for sr in subregions:
        loc = place_feature_in_region(self, sr, biome_regionmap, weight, feature)
        if loc is not False:
            return (loc, sr.regionid)
    return False

def place_dock_accessible_feature(self, name, tiles, biome, place_func, extra=(0,0)):
    candidate_regions = []
    total = 0
    for a in self.traversable_regionlist[0].adjacent:
        if a in self.dock_exclude:
            continue
        rg = self.traversable_regionlist[a]
        if rg.tile != WALKABLE_REGION:
            continue
        candidate_regions.append(rg)
        total += len(rg.points)

    attempts = []

    random.shuffle(candidate_regions)

    while candidate_regions:
        pick = random.randrange(0, total)
        i = 0
        pick -= len(candidate_regions[i].points)
        while pick > 0:
            i += 1
            pick -= len(candidate_regions[i].points)
        total -= len(candidate_regions[i].points)
        reg = candidate_regions.pop(i)
        attempts.append(functools.partial(place_func, self.copy(), name, tiles, biome, reg, extra))

    return attempts

def coneria_candidates(self):
    walkable_regions = [r for r in self.traversable_regionlist if r.tile == WALKABLE_REGION]
    random.shuffle(walkable_regions)
    return [functools.partial(self.copy().place_coneria, w, False) for w in walkable_regions]+[functools.partial(self.copy().place_coneria, w, True) for w in walkable_regions]

def titan_west_candidates(self):
    attempts = []
    for rg,region in enumerate(self.traversable_regionlist):
        if region.tile != WALKABLE_REGION:
            continue
        if rg in self.reachable or rg in self.dock_exclude:
            continue
        attempts.append(functools.partial(self.copy().place_titan_west, region))
    return attempts

def place_in_desert(self, name, feature, require_canoe_access):
    regions = []
    for region in self.biome_regionlist:
        if region.tile != DESERT_REGION:
            continue
        p = next(iter(region.points))
        tr = self.traversable_regionmap[p[1]][p[0]]

        if require_canoe_access and not (tr in self.reachable or
                                         has_river_dock(self.traversable_regionlist[tr],
                                                        self.traversable_regionlist)):
            continue
        elif not airship_accessible(self.traversable_regionlist[tr], self.tilemap, self.traversable_regionlist):
            continue

        regions.append(region)

    pc = place_in_random_region(self, regions, self.biome_regionmap, 0, feature)

    if pc is False:
        return False

    print("Placed", name, pc)
    if name == "MirageTower1":
        self.overworldCoordinates["MirageTower1"] = {"X": pc[0][0]+1, "Y": pc[0][1]+2}
    if name == "Airship":
        self.airship = (pc[0][0]+4, pc[0][1]+3)

    return self.next_feature_todo()

def onrac_candidates(self):
    regions = []
    for region in self.traversable_regionlist:
        if region.tile == WALKABLE_REGION:
            regions.append(region)
    random.shuffle(regions)
    return [functools.partial(self.copy().place_onrac, r) for r in regions]

def has_river_dock(region, regionlist, checked=None):
    if checked is None:
        checked = []
    if region.regionid in checked:
        return False
    checked.append(region.regionid)

    if region.tile != WALKABLE_REGION:
        return False

    for adj in region.adjacent:
        if regionlist[adj].tile != CANOE_REGION:
            continue
        if 0 in regionlist[adj].adjacent:
            return True
        for adj2 in regionlist[adj].adjacent:
            if has_river_dock(regionlist[adj2], regionlist, checked):
                return True
    return False

def place_anywhere(self, name, feature):
    regions = []
    for rg in self.traversable_regionlist:
        if rg.tile != WALKABLE_REGION:
            continue
        if not airship_accessible(rg, self.tilemap, self.traversable_regionlist):
            continue
        regions.append(rg)

    pc = place_in_random_region(self, regions, self.traversable_regionmap, 0, feature)

    if pc is False:
        return False

    print("Placed", name, pc)
    if name == "Lefein":
        self.overworldCoordinates[name] = {"X": pc[0][0]+3, "Y": pc[0][1]+2}
    else:
        self.overworldCoordinates[name] = {"X": pc[0][0], "Y": pc[0][1]}

    return self.next_feature_todo()

def place_gaia(self):
    regions = []
    for rg in self.traversable_regionlist:
        if rg.tile != WALKABLE_REGION:
            continue
        if rg.regionid in self.reachable:
            continue
        if has_river_dock(rg, self.traversable_regionlist):
            continue
        regions.append(rg)

    pc = place_in_random_region(self, regions, self.traversable_regionmap, 0, GAIA_TOWN)

    if pc is False:
        return False

    self.dock_exclude.append(pc[1])

    print("Placed Gaia", pc)
    self.overworldCoordinates["Gaia"] = {"X": pc[0][0]+1, "Y": pc[0][1]+1}

    return self.next_feature_todo()


def place_ordeals(self):
    regions = []
    for rg in self.traversable_regionlist:
        if rg.tile != WALKABLE_REGION:
            continue
        if rg.regionid in self.reachable:
            continue
        if not has_river_dock(rg, self.traversable_regionlist):
            continue
        regions.append(rg)

    pc = place_in_random_region(self, regions, self.traversable_regionmap, 0, ORDEALS_CASTLE)

    if pc is False:
        return False

    self.dock_exclude.append(pc[1])

    print("Placed Ordeals", pc)
    self.overworldCoordinates["CastleOrdeals1"] = {"X": pc[0][0]+1, "Y": pc[0][1]+1}

    return self.next_feature_todo()

def place_waterfall(self):
    regions = []
    for rg in self.traversable_regionlist:
        if rg.tile != CANOE_REGION:
            continue
        accessible = False
        if 0 in rg.adjacent:
            accessible = True
        else:
            for adj in rg.adjacent:
                if (self.traversable_regionlist[adj].tile == WALKABLE_REGION and
                    airship_accessible(self.traversable_regionlist[adj], self.tilemap, self.traversable_regionlist)):
                    accessible = True
        if not accessible:
            continue
        regions.append(rg)

    random.shuffle(regions)

    for rg in regions:
        for p in rg.points:
            if (self.tilemap[p[1]][p[0]-1] == MOUNTAIN
                and self.tilemap[p[1]][p[0]+1] == MOUNTAIN
                and self.tilemap[p[1]-1][p[0]] == RIVER
                and self.tilemap[p[1]+1][p[0]] == RIVER):
                pc = place_feature_in_region(self, rg, self.traversable_regionmap,
                                             0, [[WATERFALL]], place_at=(p[0], p[1]))
                print("Placed waterfall",pc)
                self.overworldCoordinates["Waterfall"] = {"X": p[0], "Y": p[1]}
                return self.next_feature_todo()
    return False

def mountain_candidates(self, name, feature, teleport):
    c = [functools.partial(self.copy().place_in_mountains, region, name, feature, teleport)
         for region in self.biome_regionlist
         if region.tile == MOUNTAIN_REGION]
    random.shuffle(c)
    return c

# def airship_desert(self):
#     regions = []
#     for region in self.biome_regionlist:
#         if region.tile != DESERT_REGION:
#             continue
#         p = next(iter(region.points))
#         tv = self.traversable_regionlist[self.traversable_regionmap[p[1]][p[0]]]
#         if tv.regionid in self.reachable:
#             regions.append(region)
#             continue
#         if has_river_dock(tv, self.traversable_regionlist):
#             regions.append(region)
#             continue

#     if not regions:
#         return False

#     random.shuffle(regions)
#     rg = regions.pop()

#     pickpoint = []
#     for p in rg.points:
#         if self.tilemap[p[1]][p[0]] == DESERT:
#             self.tilemap[p[1]][p[0]] = AIRSHIP_DESERT
#             pickpoint.append(p)

#     print("Airship desert", rg.nwcorner, rg.secorner)
#     self.airship = pickpoint[random.randrange(0, len(pickpoint))]

#     return self.next_feature_todo()

def place_ship_accessible_feature(self, name, tiles, biome, region, extra):
    if biome == "cave":
        pc = place_cave(region, self.traversable_regionmap, self.tilemap, self.weightmap, 0, tiles)
    else:
        subregions = [self.biome_regionlist[r] for r in get_subregions(region, self.biome_regionmap)
                      if self.biome_regionlist[r].tile in biome]
        #print("reg:", region.nwcorner, region.secorner)
        #for sr in subregions:
        #    print("sub:", sr.nwcorner, sr.secorner)
        pc = place_in_random_region(self, subregions, self.biome_regionmap, 0, tiles)
        if pc is not False:
            pc = pc[0]

    if pc is False:
        return False

    if not self.place_dock(region):
        return False

    self.reachable.append(region.regionid)

    print("Placed", name, "at", pc, "region", region.regionid)

    if name == "Elfland":
        self.overworldCoordinates["Elfland"] = {"X": pc[0]+1, "Y": pc[1]+3}
        self.overworldCoordinates["ElflandCastle"] = {"X": pc[0]+2, "Y": pc[1]+2}
    else:
        self.overworldCoordinates[name] = {"X": pc[0]+extra[0], "Y": pc[1]+extra[1]}

    return self.next_feature_todo()


def place_earth_cave(self, name, tiles, biome, region, extra):
    pc = place_cave(region, self.traversable_regionmap, self.tilemap, self.weightmap, 0, EARTH_CAVE)

    if pc is False:
        return False

    if not self.place_canal(region):
        return False

    self.dock_exclude.append(region.regionid)

    print("Placed", name, "at", pc, "region", region.regionid)
    self.overworldCoordinates["EarthCave1"] = {"X": pc[0], "Y": pc[1]}

    return self.next_feature_todo()


features_todo = collections.deque([
    (coneria_candidates,),
    (place_gaia,),
    (place_ordeals,),
    (titan_west_candidates,),
    (place_in_desert, "MirageTower1", MIRAGE_TOWER, False),
    (place_in_desert, "Caravan", OASIS, False),
    (onrac_candidates,),
    (place_dock_accessible_feature, "EarthCave1", EARTH_CAVE, "cave", place_earth_cave),
    (place_dock_accessible_feature, "TitansTunnelEast", TITAN_CAVE_E, "cave",
     place_ship_accessible_feature),
    (place_dock_accessible_feature, "MatoyasCave", MATOYAS_CAVE, "cave",
     place_ship_accessible_feature),
    (place_dock_accessible_feature, "DwarfCave", DWARF_CAVE, "cave",
     place_ship_accessible_feature),
    (place_dock_accessible_feature, "Elfland", ELFLAND_TOWN_CASTLE, (LAND_REGION, GRASS_REGION, FOREST_REGION),
     place_ship_accessible_feature),
    (place_dock_accessible_feature, "MarshCave1", pit_cave_feature(MARSH_CAVE), (MARSH_REGION,),
     place_ship_accessible_feature),
    (place_dock_accessible_feature, "NorthwestCastle", ASTOS_CASTLE, (LAND_REGION, GRASS_REGION, FOREST_REGION, MARSH_REGION),
     place_ship_accessible_feature, (1, 1)),
    (place_dock_accessible_feature, "Melmond", MELMOND_TOWN, (LAND_REGION, GRASS_REGION, MARSH_REGION),
     place_ship_accessible_feature, (1, 1)),
    (place_dock_accessible_feature, "CrescentLake", CRESCENT_LAKE_CITY, (LAND_REGION, GRASS_REGION, FOREST_REGION, MARSH_REGION),
     place_ship_accessible_feature, (2, 5)),
    (place_anywhere, "Lefein", LEFEIN_CITY),
    (place_anywhere, "BahamutCave1", pit_cave_feature(BAHAMUTS_CAVE)),
    (place_anywhere, "Cardia1", pit_cave_feature(CARDIA_1)),
    (place_anywhere, "Cardia2", pit_cave_feature(CARDIA_2)),
    (place_anywhere, "Cardia4", pit_cave_feature(CARDIA_3)),
    (place_anywhere, "Cardia5", pit_cave_feature(CARDIA_4)),
    (place_anywhere, "Cardia6", pit_cave_feature(CARDIA_5)),
    (place_waterfall,),
    (mountain_candidates,"GurguVolcano1", VOLCANO, (3, 2)),
    (mountain_candidates,"IceCave1", ICE_CAVE_FEATURE, (2, 1)),
    (place_in_desert, "Airship", AIRSHIP_FEATURE, True),
])

class PlacementState():
    def __init__(self, tilemap, biome_regionmap, biome_regionlist, traversable_regionmap, traversable_regionlist,
                 weightmap, features_todo):
        self.tilemap = tilemap
        self.biome_regionmap = biome_regionmap
        self.biome_regionlist = biome_regionlist
        self.traversable_regionmap = traversable_regionmap
        self.traversable_regionlist = traversable_regionlist
        self.weightmap = weightmap
        self.overworldCoordinates = {}
        self.airship = None
        self.bridge = None
        self.canal = None
        self.reachable = []
        self.dock_exclude = []
        self.features_todo = features_todo

    def copy(self):
        c = copy.copy(self)
        c.tilemap = copy.deepcopy(c.tilemap)
        c.reachable = copy.copy(c.reachable)
        c.dock_exclude = copy.copy(c.dock_exclude)
        c.weightmap = copy.deepcopy(c.weightmap)
        c.features_todo = copy.copy(c.features_todo)
        c.overworldCoordinates = copy.copy(c.overworldCoordinates)
        return c

    def place_coneria(self, traversable_region, do_place_bridge):
        subregions = [self.biome_regionlist[r] for r in get_subregions(traversable_region, self.biome_regionmap)]
        pc = place_in_random_region(self, subregions, self.biome_regionmap, 0, CONERIA_CITY)
        self.reachable.append(traversable_region.regionid)
        if pc is not False:
            print("placed coneria at", pc)
            self.overworldCoordinates["Coneria"] = {"X": pc[0][0]+2, "Y": pc[0][1]+4}
            self.overworldCoordinates["ConeriaCastle1"] = {"X": pc[0][0]+3, "Y": pc[0][1]+3}
            return self.place_fiends(traversable_region, subregions, do_place_bridge)
        return False

    def place_fiends(self, region, subregions, do_place_bridge):
        pc = place_in_random_region(self, subregions, self.biome_regionmap, 0, TEMPLE_OF_FIENDS)
        if pc is not False:
            print("placed ToF at", pc)
            self.overworldCoordinates["TempleOfFiends1"] = {"X": pc[0][0]+2, "Y": pc[0][1]+2}

            # coneria region gets a dock
            pc = self.place_dock(region)
            if pc is not False:
                if do_place_bridge:
                    return [functools.partial(self.copy().bridge_candidates, region)]
                else:
                    return self.place_pravoka(region, True)
        return False

    def bridge_candidates(self, coneria_region):
        c = [functools.partial(self.copy().place_bridge, coneria_region, self.traversable_regionlist[a])
                for a in coneria_region.adjacent
                if self.traversable_regionlist[a].tile == CANOE_REGION]
        random.shuffle(c)
        return c

    def place_bridge(self, coneria_region, r):
        bridged_region = None
        pickpoint = list(r.points)
        random.shuffle(pickpoint)
        for p in pickpoint:
            c1 = self.traversable_regionmap[p[1]-1][p[0]]
            c2 = self.traversable_regionmap[p[1]+1][p[0]]
            if (c1 == coneria_region.regionid and c2 != coneria_region.regionid and
                self.traversable_regionlist[c2].tile == WALKABLE_REGION):
                self.bridge = p
                bridged_region = self.traversable_regionlist[c2]
                break

            if (c2 == coneria_region.regionid and c1 != coneria_region.regionid and
                self.traversable_regionlist[c1].tile == WALKABLE_REGION):
                self.bridge = p
                bridged_region = self.traversable_regionlist[c1]
                break

        if self.bridge is not None:
            # Bridge location
            #self.tilemap[self.bridge[1]][self.bridge[0]] = DOCK_W
            print("placed bridge at", self.bridge)
            self.reachable.append(bridged_region.regionid)
            return [functools.partial(self.copy().place_pravoka, bridged_region, False)]

        return False

    def place_pravoka(self, pravoka_region, moat):
        points = list(pravoka_region.points)
        random.shuffle(points)
        for p in points:
            x = p[0]
            y = p[1]

            if moat:
                feature = PRAVOKA_CITY_MOAT
            else:
                feature = PRAVOKA_CITY

            w = len(feature[0])
            h = len(feature)

            for c in ((-1, h-1, w-1),
                      (w,  h-1, 0),
            ):
                c1 = self.traversable_regionmap[y+c[1]][x+c[0]]
                if c1 == 0:
                    self.pravoka = place_feature_in_region(self, pravoka_region, self.traversable_regionmap,
                                                           0, feature, place_at=(p[0], p[1]))
                    if self.pravoka is not False:
                        if moat:
                            self.bridge = (x+4, y)
                        self.tilemap[y+c[1]][x+c[2]] = LAND

                        print("Placed Pravoka at", self.pravoka)
                        self.overworldCoordinates["Pravoka"] = {"X": p[0]+2, "Y": p[1]+3}
                        return self.next_feature_todo()
        return False


    def place_dock(self, region):
        points = list(region.points)
        random.shuffle(points)
        for p in points:
            for c in ((-1, 0,  0, -2, W_DOCK_STRUCTURE),
                      (0,  1, -2, -2, S_DOCK_STRUCTURE),
                      (1,  0, -3, -2, E_DOCK_STRUCTURE),
                      (0, -1, -2,  0, N_DOCK_STRUCTURE),
            ):
                if self.traversable_regionmap[p[1]+c[1]][p[0]+c[0]] == 0:
                    dock = place_feature_in_region(self, region, self.traversable_regionmap,
                                                   0, c[4], place_at=(p[0]+c[2], p[1]+c[3]))
                    if dock is not False:
                        print("placed a dock at", dock, "in region", region.regionid)
                        return True
        return False

    def place_canal(self, region):
        points = list(region.points)
        random.shuffle(points)
        for p in points:
            for c in ((-1, 0,  0, -1, W_CANAL_STRUCTURE,  1),
                      (1,  0, -5, -1, E_CANAL_STRUCTURE, -1),
            ):
                if self.traversable_regionmap[p[1]+c[1]][p[0]+c[0]] == 0:
                    dock = place_feature_in_region(self, region, self.traversable_regionmap,
                                                   0, c[4], place_at=(p[0]+c[2], p[1]+c[3]))
                    if dock is not False:
                        # canal location
                        #self.tilemap[p[1]][p[0] + c[5]] = LAND
                        self.canal = (p[0] + c[5], p[1])

                        print("placed a dock at", dock, "in region", region.regionid)
                        return True
        return False


    def place_titan_west(self, region):
        pc = place_cave(region, self.traversable_regionmap,
                        self.tilemap, self.weightmap, 0, TITAN_CAVE_W)
        if pc is False:
            return False

        print("Placed Titan west", pc)
        self.overworldCoordinates["TitansTunnelWest"] = {"X": pc[0], "Y": pc[1]}

        pc = place_cave(region, self.traversable_regionmap,
                        self.tilemap, self.weightmap, 5, SARDAS_CAVE)

        if pc is False:
            return False

        print("Placed Sarda", pc)
        self.overworldCoordinates["SardasCave"] = {"X": pc[0], "Y": pc[1]}

        self.dock_exclude.append(region.regionid)
        self.reachable.append(region.regionid)

        return self.next_feature_todo()

    def place_in_mountains(self, region, name, feature, teleport):
        points = list(region.points)
        random.shuffle(points)
        for p in points:
            x = p[0]
            y = p[1]

            w = len(feature[0])
            h = len(feature)

            for c in ((w//2, h),
            ):
                sample = self.traversable_regionlist[self.traversable_regionmap[y+c[1]][x+c[0]]]
                if sample.tile != CANOE_REGION:
                    continue
                pc = place_feature_in_region(self, region, self.biome_regionmap,
                                               0, feature, place_at=(x, y))
                if pc is not False:
                    print("Placed", name, pc)
                    self.overworldCoordinates[name] = {"X": p[0]+teleport[0], "Y": p[1]+teleport[1]}
                    return self.next_feature_todo()
        return False


    def place_onrac(self, region):
        points = list(region.points)
        random.shuffle(points)
        w = len(ONRAC_TOWN[0])
        for p in points:
            x = p[0]
            y = p[1]

            if self.tilemap[y+2][x+w] != OCEAN:
                continue

            pc = place_feature_in_region(self, region, self.traversable_regionmap,
                                         0, ONRAC_TOWN, place_at=(x, y))

            if not airship_accessible(region, self.tilemap, self.traversable_regionlist):
                return False

            if pc is not False:
                print("Placed Onrac at", pc)
                self.overworldCoordinates["Onrac"] = {"X": p[0]+1, "Y": p[1]+1}
                return self.next_feature_todo()
        return False

    def next_feature_todo(self):
        if len(self.features_todo) == 0:
            return self
        next_todo = self.features_todo.popleft()
        return next_todo[0](self.copy(), *next_todo[1:])


def place_features(tilemap):

    biome_regionmap, biome_regionlist = find_regions(tilemap, pre_shore_region_map)
    traversable_regionmap, traversable_regionlist = find_regions(tilemap, traversable_region_map)

    weightmap = []
    for x in range(0, map_size):
        weightmap.append([0] * map_size)

    walkable_count = len([t for t in traversable_regionlist if t.tile == WALKABLE_REGION])
    print("Walkable regions count", walkable_count)
    if walkable_count < 15 or walkable_count > 45:
        # too few regions or too many regions tend to fail
        return None

    pending = [PlacementState(dup_tilemap(tilemap), biome_regionmap, biome_regionlist,
                              traversable_regionmap, traversable_regionlist, weightmap,
                              copy.copy(features_todo)).next_feature_todo]

    finalstate = None
    while pending:
        p = pending.pop()
        r = p()
        if isinstance(r, PlacementState):
            finalstate = r
            break
        if r is not False:
            pending.extend(r)

    if finalstate is not None:
        return finalstate

    return None

def assign_encounter_domains(state):
    nearest_dungeon = []
    for x in range(0, map_size):
        nearest_dungeon.append([None] * map_size)

    working_list = collections.deque()

    for k,v, in state.overworldCoordinates.items():
        working_list.append((v["X"], v["Y"], k))

    while working_list:
            x, y, dungeon = working_list.popleft()

            if nearest_dungeon[y][x] is not None:
                continue

            nearest_dungeon[y][x] = dungeon

            adjacent = [(x+1, y), (x, y+1), (x-1, y), (x, y-1)]
            for ab in adjacent:
                if ab[0] >= 0 and ab[0] <= (map_size-1) and ab[1] >= 0 and ab[1] <= (map_size-1):
                    next_tile = traversable_region_map[state.tilemap[ab[1]][ab[0]]]
                    if next_tile in (WALKABLE_REGION, CANOE_REGION):
                        working_list.append((ab[0], ab[1], dungeon))

    source_encounter_domains = {
        "Coneria":         [0o54, 0o44],
        "ConeriaCastle1":  [0o54, 0o44],
        "TempleOfFiends1": [0o34],
        "Pravoka":         [0o46, 0o47],
        "Gaia":            [0o06],
        "CastleOrdeals1":  [0o14, 0o05],
        "TitansTunnelWest": [0o50],
        "SardasCave": [0o50],
        "MirageTower1": [0o16],
        "Onrac": [0o11, 0o21],
        "EarthCave1": [0o52],
        "TitansTunnelEast": [0o50],
        "MatoyasCave": [0o35, 0o45],
        "DwarfCave": [0o43],
        "Elfland": [0o64],
        "ElflandCastle": [0o64],
        "MarshCave1": [0o73],
        "NorthwestCastle": [0o53],
        "Melmond": [0o42, 0o52],
        "CrescentLake": [0o66],
        "Lefein": [0o37],
        "BahamutCave1": [0o13],
        "Cardia1": [0o12],
        "Cardia2": [0o12],
        "Cardia4": [0o12],
        "Cardia5": [0o13],
        "Cardia6": [0o13],
        "Waterfall": [0o01],
        "GurguVolcano1": [0o66],
        "IceCave1": [0o66]
    }

    domains = []

    for i in range(0, 8):
        for j in range(0, 8):
            counts = {}
            for y in range(0, 32):
                for x in range(0, 32):
                    nd = nearest_dungeon[i*32 + y][j*32 + x]
                    if nd is not None:
                        counts[nd] = counts.get(nd, 0) + 1

            pick = None
            mx = 0
            for k,v in counts.items():
                if v > mx:
                    pick = k
                    mx = v
            if pick is not None:
                dm = source_encounter_domains[pick]
                if len(dm) > 1:
                    domains.append(dm[random.randrange(0, len(dm))])
                else:
                    domains.append(dm[0])
            else:
                domains.append(0)
    print(domains)
    return domains


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
        tilemap.append([OCEAN] * map_size)

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
                    tilemap[y][x] = MOUNTAIN
                    mountain_count += 1
                elif tile > sea_elevation:
                    tilemap[y][x] = LAND
                    land_count += 1
                else:
                    tilemap[y][x] = OCEAN
        if land_count < min_land_tiles:
            sea_elevation -= .005
        if mountain_count < min_mtn_tiles:
            mountain_elevation -= .005
        if sea_elevation <= 0:
            return False

    print("sea_elevation", sea_elevation)
    print("mountain_elevation", mountain_elevation)

    print("Lowering iterations", lowering_iter)

    colormap = {OCEAN: (101, 183, 255),
                RIVER: (178, 229, 255),
                LAND: (52, 176, 0),
                MOUNTAIN: (255, 255, 255)}

    savemap(tilemap, colormap, "map1.png")

    all_simple_tiles = (MOUNTAIN, OCEAN, RIVER, LAND)

    print("expanding mountains")
    tilemap = apply_filter(tilemap, expand_mountains, {"_": (LAND, OCEAN, MOUNTAIN)}, False)

    print("expanding oceans")
    tilemap = apply_filter(tilemap, expand_oceans, {"_": (LAND, OCEAN, MOUNTAIN)}, False)

    flow_rivers(basemap, tilemap, mountain_elevation + (heightmax-mountain_elevation)*.5, heightmax, 10)
    flow_rivers(basemap, tilemap, sea_elevation + (mountain_elevation-sea_elevation)*.5, mountain_elevation, 10)

    tilemap = apply_filter(tilemap, connect_diagonals, {"_": (MOUNTAIN, LAND),
                                                        "*": all_simple_tiles}, False)

    print("removing small islands")
    regionmap, regionlist = find_regions(tilemap, pre_shore_region_map)
    remove_small_islands(tilemap, regionlist)

    print("Adding biomes")
    regionmap, regionlist = find_regions(tilemap, pre_shore_region_map)
    landregions = [r for r in regionlist if r.tile == LAND]
    tilemap = add_biomes(tilemap, landregions)

    for i in range(0, 3):
        print("removing small regions")
        regionmap, regionlist = find_regions(tilemap, pre_shore_region_map)
        remove_small_regions(tilemap, regionlist)

        print("Removing salients")
        tilemap = apply_filter(tilemap, [None], None, True, matcher=functools.partial(check_salient, pre_shore_region_map))

    print("small seas become lakes")
    regionmap, regionlist = find_regions(tilemap, pre_shore_region_map)
    small_seas_become_lakes(tilemap, regionlist)

    saveffm(tilemap, "map5.ffm")

    finalstate = place_features(tilemap)
    if finalstate is None:
        return False
    tilemap = finalstate.tilemap

    domains = assign_encounter_domains(finalstate)

    print("Applying borders")
    tilemap = apply_shores(tilemap)

    print("Removing salients")
    tilemap = apply_filter(tilemap, [None], None, True, matcher=functools.partial(check_salient, post_shore_region_map))
    tilemap = apply_borders(tilemap)

    # Exits
    # 0 "Titan E"
    # 1 "Titan W"
    # 2 "Ice Cave"
    # 3 "Castle Ordeals"
    # 4 "Castle Coneria"
    # 5 "Earth Cave",
    # 6 "Gurgu Volcano"
    # 7 "Sea Shrine"
    # 8 "Sky Castle"

    saveffm(tilemap, "map5.ffm")
    with open("map5.json", "w") as f:
        json.dump({
            "StartingLocation": {
                "X": finalstate.overworldCoordinates["ConeriaCastle1"]["X"],
                "Y": finalstate.overworldCoordinates["ConeriaCastle1"]["Y"]+5
            },
	    "AirShipLocation": {
		"X": finalstate.airship[0],
		"Y": finalstate.airship[1]
	    },
            "BridgeLocation": {
                "X": finalstate.bridge[0],
                "Y": finalstate.bridge[1]
            },
            "CanalLocation": {
                "X": finalstate.canal[0],
                "Y": finalstate.canal[1]
            },
	    "ShipLocations": [
		{
		    "TeleporterIndex": 255,
		    "X": finalstate.overworldCoordinates["Pravoka"]["X"]+1,
		    "Y": finalstate.overworldCoordinates["Pravoka"]["Y"]+3
		}
	    ],
	    "TeleporterFixups": [
                {
                    "Type": 1,
                    "Index": 0,
                    "To": {
                        "X": finalstate.overworldCoordinates["TitansTunnelEast"]["X"],
                        "Y": finalstate.overworldCoordinates["TitansTunnelEast"]["Y"]
                    }
                },
                {
                    "Type": 1,
                    "Index": 1,
                    "To": {
                        "X": finalstate.overworldCoordinates["TitansTunnelWest"]["X"],
                        "Y": finalstate.overworldCoordinates["TitansTunnelWest"]["Y"]
                    }
                },
                {
                    "Type": 1,
                    "Index": 2,
                    "To": {
                        "X": finalstate.overworldCoordinates["IceCave1"]["X"],
                        "Y": finalstate.overworldCoordinates["IceCave1"]["Y"]
                    }
                },
                {
                    "Type": 1,
                    "Index": 3,
                    "To": {
                        "X": finalstate.overworldCoordinates["CastleOrdeals1"]["X"],
                        "Y": finalstate.overworldCoordinates["CastleOrdeals1"]["Y"]
                    }
                },
                {
                    "Type": 1,
                    "Index": 4,
                    "To": {
                        "X": finalstate.overworldCoordinates["ConeriaCastle1"]["X"],
                        "Y": finalstate.overworldCoordinates["ConeriaCastle1"]["Y"]
                    }
                },
                {
                    "Type": 1,
                    "Index": 5,
                    "To": {
                        "X": finalstate.overworldCoordinates["EarthCave1"]["X"],
                        "Y": finalstate.overworldCoordinates["EarthCave1"]["Y"]
                    }
                },
                {
                    "Type": 1,
                    "Index": 6,
                    "To": {
                        "X": finalstate.overworldCoordinates["GurguVolcano1"]["X"],
                        "Y": finalstate.overworldCoordinates["GurguVolcano1"]["Y"]
                    }
                },
                {
                    "Type": 1,
                    "Index": 7,
                    "To": {
                        "X": finalstate.overworldCoordinates["Onrac"]["X"],
                        "Y": finalstate.overworldCoordinates["Onrac"]["Y"]
                    }
                },
                {
                    "Type": 1,
                    "Index": 8,
                    "To": {
                        "X": finalstate.overworldCoordinates["MirageTower1"]["X"],
                        "Y": finalstate.overworldCoordinates["MirageTower1"]["Y"]
                    }
                }
	    ],
	    "DomainFixups": [],
	    "DomainUpdates": [{"From": j, "To": i} for i,j in enumerate(domains)],
            "OverworldCoordinates": finalstate.overworldCoordinates
        }, f, indent=4)

    #printmap(tilemap)

    return True

import sys
seed = random.randrange(0, sys.maxsize)
random.seed(seed)
print("Using seed", seed)
random.seed(125)
#random.seed(9066423674080091572)
success = procgen()
while success is False:
    success = procgen()
