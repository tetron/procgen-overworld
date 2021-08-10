import random
import math
import json
import functools
import copy
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
        self.border_points = set()
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
    pending = []

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
                        regionlist[current_region].border_points.add((x, y))

        while pending and not working_stack:
            x, y, current_region = pending.pop(0)
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


def render_feature(tilemap, regionmap, weightmap, feature, x, y):
    for y2,row in enumerate(feature):
        for x2,tile in enumerate(row):
            if feature[y2][x2] is not None:
                tilemap[y+y2][x+x2] = feature[y2][x2]
                regionmap[y+y2][x+x2] = -1

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


def place_feature_in_region(r, regionmap, tilemap, weightmap, maxweight, feature, place_at=None):
    h = len(feature)
    w = len(feature[0])

    candidates = set()
    if place_at is not None:
        if check_fit(regionmap, r, place_at[0], place_at[1], h, w):
            candidates.add(place_at)
    else:
        for y in range(r.nwcorner[1], r.secorner[1]-h):
            for x in range(r.nwcorner[0], r.secorner[0]-w):
                if check_fit(regionmap, r, x, y, h, w):
                    candidates.add((x, y))

    candidates = list(candidates)

    if not candidates:
        return False

    random.shuffle(candidates)

    candidates.sort(key=lambda n: weightmap[n[1]+(h//2)][n[0]+(w//2)])
    if weightmap[candidates[0][1]+(h//2)][candidates[0][0]+(w//2)] > maxweight:
        return False

    render_feature(tilemap, regionmap, weightmap, feature, candidates[0][0], candidates[0][1])
    return (candidates[0][0], candidates[0][1])


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

    render_feature(tilemap, regionmap, weightmap, [[cave]], candidates[0][0], candidates[0][1])
    return True


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
    non_water_tiles = all_tiles.difference([OCEAN, RIVER, SHORE_N, SHORE_E, SHORE_S, SHORE_W])
    non_ocean_shore_tiles = all_tiles.difference([OCEAN, SHORE_NW, SHORE_NE, SHORE_SW, SHORE_SE, RIVER])
    tilemap = apply_filter(tilemap, apply_shores1, {"*": all_tiles, "_": non_water_tiles}, False)
    tilemap = apply_filter(tilemap, apply_shores2, {"*": all_tiles, "_": non_water_tiles}, False)
    tilemap = apply_filter(tilemap, apply_shores3, {"*": all_tiles, "_": non_ocean_shore_tiles}, False)

    return tilemap

def apply_borders(tilemap):
    all_tiles = set(ALL_TILES)

    non_desert_tiles = all_tiles.difference([DESERT, DESERT_NW, DESERT_NE, DESERT_SW, DESERT_SE])
    non_marsh_tiles = all_tiles.difference([MARSH, MARSH_NW, MARSH_NE, MARSH_SW, MARSH_SE])
    non_grass_tiles = all_tiles.difference([GRASS, GRASS_NW, GRASS_NE, GRASS_SW, GRASS_SE])
    non_forest_tiles = all_tiles.difference([FOREST_NW, FOREST_N, FOREST_NE, FOREST_W, FOREST,
                                             FOREST_E, FOREST_SW, FOREST_S, FOREST_SE])
    non_mountain_tiles = all_tiles.difference([MOUNTAIN, EARTH_CAVE, ICE_CAVE, DWARF_CAVE, MATOYAS_CAVE, SARDAS_CAVE, TITAN_CAVE_E, TITAN_CAVE_W])
    non_water_tiles = all_tiles.difference([OCEAN, RIVER, SHORE_N, SHORE_E, SHORE_S, SHORE_W])

    tilemap = apply_filter(tilemap, mountain_borders, {"_": non_mountain_tiles, "*": all_tiles}, False)
    tilemap = apply_filter(tilemap, river_borders, {"_": non_water_tiles,
                                                    "*": all_tiles},
                           False)

    tilemap = apply_filter(tilemap, desert_borders, {"_": non_desert_tiles, "*": all_tiles}, False)
    tilemap = apply_filter(tilemap, marsh_borders,  {"_": non_marsh_tiles, "*": all_tiles}, False)
    tilemap = apply_filter(tilemap, grass_borders,  {"_": non_grass_tiles, "*": all_tiles}, False)
    tilemap = apply_filter(tilemap, forest_borders, {"_": non_forest_tiles, "*": all_tiles}, False)

    return tilemap


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
        subregions.add(other_regionmap[p[1]][p[0]])
    return subregions

def place_in_random_region(subregions, biome_regionmap, tilemap, weightmap, weight, feature):
    random.shuffle(subregions)
    for sr in subregions:
        loc = place_feature_in_region(sr, biome_regionmap, tilemap, weightmap, weight, feature)
        if loc is not False:
            return loc
    return False

class PlacementState():
    def __init__(self, tilemap, biome_regionmap, biome_regionlist, traversable_regionmap, traversable_regionlist, weightmap):
        self.tilemap = tilemap
        self.biome_regionmap = biome_regionmap
        self.biome_regionlist = biome_regionlist
        self.traversable_regionmap = traversable_regionmap
        self.traversable_regionlist = traversable_regionlist
        self.weightmap = weightmap
        self.coneria = False
        self.fiends = False
        self.bridge = False
        self.pravoka = False
        self.reachable = []

    def copy(self):
        c = copy.copy(self)
        c.tilemap = copy.deepcopy(c.tilemap)
        c.weightmap = copy.deepcopy(c.weightmap)
        return c

    def place_coneria(self, traversable_region):
        subregions = [self.biome_regionlist[r] for r in get_subregions(traversable_region, self.biome_regionmap)]
        self.coneria = place_in_random_region(subregions, self.biome_regionmap, self.tilemap, self.weightmap, 0, CONERIA_CITY)
        self.reachable.append(traversable_region.regionid)
        if self.coneria is not False:
            print("placed coneria at", self.coneria)
            return [functools.partial(self.copy().place_fiends, traversable_region, subregions)]
        return False

    def place_fiends(self, region, subregions):
        self.fiends = place_in_random_region(subregions, self.biome_regionmap, self.tilemap, self.weightmap, 0, TEMPLE_OF_FIENDS)
        if self.fiends is not False:
            print("placed ToF at", self.fiends)
            return [functools.partial(self.place_pravoka, region)]+[functools.partial(self.copy().bridge_candidates, region)]
        return False

    def bridge_candidates(self, coneria_region):
        return [functools.partial(self.copy().place_bridge, coneria_region, self.traversable_regionlist[a])
                for a in coneria_region.adjacent
                if self.traversable_regionlist[a].tile == CANOE_REGION]

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

        if self.bridge is not False:
            self.tilemap[self.bridge[1]][self.bridge[0]] = DOCK_W
            print("placed bridge at", self.bridge)
            self.reachable.append(bridged_region.regionid)
            return [functools.partial(self.copy().place_pravoka, bridged_region)]

        return False

    def place_pravoka(self, pravoka_region):
        for p in pravoka_region.points:
            x = p[0]
            y = p[1]

            w = len(PRAVOKA_CITY[0])
            h = len(PRAVOKA_CITY)

            for c in ((-1, h-1, w-1),
                      (w,  h-1, 0),
            ):
                c1 = self.traversable_regionmap[y+c[1]][x+c[0]]
                if c1 == 0:
                    self.pravoka = place_feature_in_region(pravoka_region, self.traversable_regionmap, self.tilemap,
                                                           self.weightmap, 0, PRAVOKA_CITY, place_at=(p[0], p[1]))
                    if self.pravoka is not False:
                        self.tilemap[y+c[1]][x+c[2]] = LAND
                        print("placed pravoka at", self.pravoka)
                        def dwarf(self, region):
                            return self.place_dwarf_cave(region)
                        return [functools.partial(self.copy().dock_accessible_candidates, dwarf)]
        return False

    def dock_accessible_candidates(self, placement_func):
        candidate_regions = []
        total = 0
        for a in self.traversable_regionlist[0].adjacent:
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
            attempts.append(functools.partial(placement_func, self.copy(), reg))

        return attempts

    def place_dock(self, region):
        for p in region.border_points:
            for c in ((-1, 0,  0, -1, EW_DOCK),
                      (0,  1, -1,  0, NS_DOCK),
                      (1,  0,  0, -1, EW_DOCK),
                      (0,  1, -1,  0, NS_DOCK),
            ):
                if self.tilemap[p[1]+c[1]][p[0]+c[0]] == OCEAN:
                    dock = place_feature_in_region(region, self.traversable_regionmap, self.tilemap,
                                                  self.weightmap, 0, c[4], place_at=(p[0]+c[2], p[1]+c[3]))
                    if dock is not False:
                        print("placed a dock at", dock)
                        return True
        return False

    def place_dwarf_cave(self, region):
        pc = place_cave(region, self.traversable_regionmap, self.tilemap, self.weightmap, 0, DWARF_CAVE)
        if pc is False:
            return False
        print("Placed dwarf cave")

        if not self.place_dock(region):
            return False

        def elf(self, region):
            return self.place_elfland(region)
        return [functools.partial(self.copy().dock_accessible_candidates, elf)]

    def place_elfland(self, region):
        subregions = [self.biome_regionlist[r] for r in get_subregions(region, self.biome_regionmap)
                      if self.biome_regionlist[r].tile in (LAND_REGION, GRASS_REGION, FOREST_REGION)]
        self.elfland = place_in_random_region(subregions, self.biome_regionmap, self.tilemap, self.weightmap, 0, ELFLAND_TOWN_CASTLE)

        if self.elfland is False:
            return False

        if not self.place_dock(region):
            return False

        print("placed Elfland at", self.elfland)
        return self
        #return [functools.partial(self.place_pravoka, region)]+[functools.partial(self.copy().bridge_candidates, region)]


def place_features(tilemap):

    biome_regionmap, biome_regionlist = find_regions(tilemap, pre_shore_region_map)
    traversable_regionmap, traversable_regionlist = find_regions(tilemap, traversable_region_map)

    # features = [CONERIA_CITY, TEMPLE_OF_FIENDS, PRAVOKA_CITY, ELFLAND_TOWN_CASTLE, ASTOS_CASTLE,
    #             ORDEALS_CASTLE, MELMOND_TOWN, ONRAC_TOWN,
    #             LEIFEN_CITY, CRESCENT_LAKE_CITY, GAIA_TOWN,
    #             MIRAGE_TOWER, VOLCANO, OASIS,
    #             pit_cave_feature(MARSH_CAVE), pit_cave_feature(BAHAMUTS_CAVE),
    #             pit_cave_feature(CARDIA_1), pit_cave_feature(CARDIA_2),
    #             pit_cave_feature(CARDIA_3), pit_cave_feature(CARDIA_4),
    #             pit_cave_feature(CARDIA_5)
    # ]

    walkable_regions = [r for r in traversable_regionlist if r.tile == WALKABLE_REGION]
    random.shuffle(walkable_regions)

    weightmap = []
    for x in range(0, map_size):
        weightmap.append([0] * map_size)

    pending = []
    for w in walkable_regions:
        pending.append(functools.partial(PlacementState(dup_tilemap(tilemap), biome_regionmap, biome_regionlist,
                                                        traversable_regionmap, traversable_regionlist, weightmap).place_coneria, w))

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
        return finalstate.tilemap

    # checkp = tilemap

    # current_region = None
    # weight = 0
    # placed = False

    # for w in walkable_regions:
    #     current_region = w
    #     tilemap = dup_tilemap(checkp)

    #     subregions = [biome_regionlist[r] for r in get_subregions(w, biome_regionmap)]
    #     placed = place_in_random_region(subregions, biome_regionmap, tilemap, weightmap, weight, CONERIA_CITY)
    #     if placed is False:
    #         continue
    #     print("placed coneria at",placed)

    #     placed = place_in_random_region(subregions, biome_regionmap, tilemap, weightmap, weight, TEMPLE_OF_FIENDS)
    #     if placed is False:
    #         continue
    #     print("placed ToF at",placed)

    #     bridge_point = None
    #     bridged_region = None
    #     for a in current_region.adjacent:
    #         r = traversable_regionlist[a]
    #         if r.tile != CANOE_REGION:
    #             continue
    #         pickpoint = list(r.points)
    #         random.shuffle(pickpoint)
    #         for p in pickpoint:
    #             c1 = traversable_regionmap[p[1]-1][p[0]]
    #             c2 = traversable_regionmap[p[1]+1][p[0]]
    #             if (c1 == current_region.regionid and c2 != current_region.regionid and
    #                 traversable_regionlist[c2].tile == WALKABLE_REGION):
    #                 bridge_point = p
    #                 bridged_region = traversable_regionlist[c2]
    #                 break
    #             if (c2 == current_region.regionid and c1 != current_region.regionid and
    #                 traversable_regionlist[c1].tile == WALKABLE_REGION):
    #                 bridge_point = p
    #                 bridged_region = traversable_regionlist[c1]
    #                 break
    #         if bridge_point is not None:
    #             break

    #     if bridge_point is None:
    #         print("Couldn't place bridge")
    #         continue

    #     print("Placed bridge",bridge_point)
    #     tilemap[bridge_point[1]][bridge_point[0]] = DOCK_W

    #     placed_pravoka = False
    #     for p in bridged_region.border_points:
    #         x = p[0]
    #         y = p[1]

    #         w = len(PRAVOKA_CITY[0])+1
    #         h = len(PRAVOKA_CITY)+1

    #         for c in ((-1,   h, "W"),
    #                   ( w,   h, "E"),
    #                   (w//2, h, "S"),
    #         ):
    #             c1 = traversable_regionmap[y+c[1]][x+c[0]]
    #             if (traversable_regionlist[c1].tile == SAILING_REGION):

    #                 placed_pravoka = place_feature_in_region(bridged_region, traversable_regionmap, tilemap,
    #                                                          weightmap, weight, PRAVOKA_CITY, place_at=(p[0], p[1]))

    #             if placed_pravoka is not False:
    #                 print("Placed as", c[2])
    #                 # make a canal
    #                 break

    #         if placed_pravoka is not False:
    #             break

    #     if placed_pravoka is False:
    #         print("Couldn't place pravoka")
    #         continue
    #     else:
    #         print("placed pravoka", placed_pravoka)


    #     return tilemap

    return None

    # landregions.sort(key=lambda r: len(r.points), reverse=True)
    # total = 0
    # for r in landregions:
    #     total += len(r.points)

    # starting_location = None

    # print("Placing features")
    # weightmap = []
    # for x in range(0, map_size):
    #     weightmap.append([0] * map_size)
    # ids = list(range(0, len(regionlist)))
    # random.shuffle(ids)
    # i = 0
    # for f in features:
    #     found = False
    #     maxweight = 0
    #     while not found:
    #         val = random.randint(0, total)
    #         for r in landregions:
    #             val -= len(r.points)
    #             if val <= 0:
    #                 break
    #         loc = place_feature_in_region(r, regionmap, tilemap, weightmap, maxweight, f)
    #         if loc:
    #             found = True
    #             if f is CONERIA_CITY:
    #                 starting_location = (loc[0]+3, loc[1]+7)
    #         maxweight += 1

    # caves = [MATOYAS_CAVE, DWARF_CAVE, EARTH_CAVE, TITAN_CAVE_E, TITAN_CAVE_W, SARDAS_CAVE, ICE_CAVE]

    # print("Placing caves")
    # for c in caves:
    #     found = False
    #     maxweight = 0
    #     while not found:
    #         val = random.randint(0, total)
    #         for r in landregions:
    #             val -= len(r.points)
    #             if val <= 0:
    #                 break
    #         if place_cave(r, regionmap, tilemap, weightmap, maxweight, c):
    #             found = True
    #         maxweight += 1


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

    points = []
    for y,row in enumerate(basemap):
        for x,tile in enumerate(row):
            if tile >= (mountain_elevation + ((heightmax-mountain_elevation)*.5)):
                points.append((x,y))

    print("flowing rivers")
    random.shuffle(points)
    for p in points[:16]:
        flow_river(basemap, tilemap, [p])

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

    tilemap = place_features(tilemap)
    if tilemap is None:
        return False

    print("Applying borders")
    tilemap = apply_shores(tilemap)

    print("Removing salients")
    tilemap = apply_filter(tilemap, [None], None, True, matcher=functools.partial(check_salient, post_shore_region_map))
    tilemap = apply_borders(tilemap)

    starting_location = (0,0)



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

    saveffm(tilemap, "map5.ffm")
    with open("map5.json", "w") as f:
        json.dump({
            "StartingLocation": {
                "X": starting_location[0],
                "Y": starting_location[1]
            },
	"AirShipLocation": {
		"X": 0,
		"Y": 0
	},
	"ShipLocations": [
	],
	"TeleporterFixups": [
	],
	"DomainFixups": [
	]
        }, f, indent=4)

    #printmap(tilemap)

    return True

random.seed(125)
success = procgen()
#while success is False:
#success = procgen()
