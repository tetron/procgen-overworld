import random
import math
import PIL.Image

perturb_reduction = 0
minimum_rect = 16
map_size = 128
land_pct = .2
mountain_pct = 0.00

def perturb_point(basemap, x0, y0, x1, y1, r0):
    if abs(x0 - x1) <= minimum_rect and abs(y0 - y1) <= minimum_rect:
        return

    if x0+1 == x1-1:
        x2 = x0+1
    elif x0 == x1:
        x2 = x0
    elif x0+1 == x1:
        x2 = x0
    else:
        n = int((x1-x0)/4)
        x2 = random.randint(x0+n, x1-n)

    if y0+1 == y1-1:
        y2 = y0+1
    elif y0 == y1:
        y2 = y0
    elif y0+1 == y1:
        y2 = y0
    else:
        n = int((y1-y0)/4)
        y2 = random.randint(y0+n, y1-n)

    x2 = int((x0+x1)/2)
    y2 = int((y0+y1)/2)

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
    perturb_point(basemap, x0, y0, x2, y2, r0)
    perturb_point(basemap, x2, y0, x1, y2, r0)
    perturb_point(basemap, x0, y2, x2, y1, r0)
    perturb_point(basemap, x2, y2, x1, y1, r0)

def clamp(n):
    return min(max(n, 0), map_size-1)

def nearby_point(basemap, x, y, a, b, points):
    a = clamp(a)
    b = clamp(b)
    if basemap[b][a] is None:
        return
    if (a,b) in points:
        return
    if len(points) < 3:
        points.append((a, b))
    else:
        dist = math.sqrt((a-x)*(a-x) + (b-y)*(b-y))
        for i in range(0, 3):
            px = points[i][0]
            py = points[i][1]
            pdist = math.sqrt((px-x)*(px-x) + (py-y)*(py-y))
            if dist < pdist:
                points.insert(i, (a, b))
                break
        if len(points) > 3:
            points.pop()


def nearest_three_points(basemap, x, y):
    points = []
    n = 0
    if basemap[y][x] is not None:
        return points
    while n < map_size:
        n += 1
        for i in range(-n, n):
            nearby_point(basemap, x, y, x+i, y-n, points)
            nearby_point(basemap, x, y, x+n, y+i, points)
            nearby_point(basemap, x, y, x-i, y+n, points)
            nearby_point(basemap, x, y, x-n, y-i, points)
        if len(points) == 3:
            break
    return points


def interpolate_height(basemap, x, y):
    p = nearest_three_points(basemap, x, y)
    if len(p) == 0:
        return basemap[y][x]

    # https://codeplea.com/triangular-interpolation
    #print(x, y, p)
    #print((p[1][1]-p[2][1])*(p[0][0]-p[2][0]))
    #print((p[2][0]-p[1][0])*(p[0][1]-p[2][1]))
    interp = 0
    divisor = (p[1][1]-p[2][1])*(p[0][0]-p[2][0]) + (p[2][0]-p[1][0])*(p[0][1]-p[2][1])
    if divisor != 0:
        w0 = ((p[1][1]-p[2][1])*(x-p[2][0]) + (p[2][0]-p[1][0])*(y-p[2][1])) / divisor
        w1 = ((p[2][1]-p[0][1])*(x-p[2][0]) + (p[0][0]-p[2][0])*(y-p[2][1])) / divisor
        w2 = 1 - w0 - w1

        interp += w0 * basemap[p[0][1]][p[0][0]]
        interp += w1 * basemap[p[1][1]][p[1][0]]
        interp += w2 * basemap[p[2][1]][p[2][0]]

    return interp


def interpolate_heights(basemap):
    newbasemap = []
    for x in range(0, map_size):
        newbasemap.append([0] * map_size)

    for y,row in enumerate(basemap):
        print(y)
        for x,tile in enumerate(row):
            newbasemap[y][x] = interpolate_height(basemap, x, y)
    return newbasemap

eliminate_islands = [
    ["..."
     ".#."
     "...",
     "."],
    ["..."
     ".M."
     "...",
     "."],
    ["___"
     "_M_"
     "___",
     "#"]]

eliminate_ponds = [
    ["___"
     "_._"
     "___",
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
    ["#__"
     "_.."
     "_..",
     "#"],
    ["_#_"
     "..."
     "...",
     "#"],
    ["__#"
     ".._"
     ".._",
     "#"],
    ["_.."
     "#.."
     "_..",
     "#"],
    [".._"
     "..#"
     ".._",
     "#"],
    ["_.."
     "_.."
     "#__",
     "#"],
    ["..."
     "..."
     "_#_",
     "#"],
    [".._"
     ".._"
     "__#",
     "#"]
]

def check_rule(tilemap, rule, x, y, multi):
    for j in range(0, 3):
        for i in range(0, 3):
            ruletile = rule[0][j*3 + i]
            checktile = tilemap[y+(j-1)][x+(i-1)]
            if checktile == ruletile or (ruletile == "_" and checktile in multi):
                pass
            else:
                return False
    return rule[1]


def apply_filter(tilemap, rules, multi):
    newtilemap = []
    for x in range(0, map_size):
        newtilemap.append(['.'] * map_size)

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
                    break
            newtilemap[y][x] = rep

    return newtilemap


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

    basemap[int(map_size/2)-1][int(map_size/2)-1] = 1

    perturb_point(basemap, border, border, map_size-1-border, map_size-1-border, 0)

    tilemap = []
    for x in range(0, map_size):
        tilemap.append(['.'] * map_size)

    #print(nearest_three_points(basemap, 63, 63), interpolate_height(basemap, 63, 63))
    #print(nearest_three_points(basemap, 62, 62), interpolate_height(basemap, 62, 62))
    #return

    basemap = interpolate_heights(basemap)

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

    print("sea_elevation", sea_elevation)
    print("mountain_elevation", mountain_elevation)

    print("Lowering iterations", lowering_iter)

    #tilemap = apply_filter(tilemap, eliminate_islands, ["#", "."])
    #tilemap = apply_filter(tilemap, eliminate_ponds, ["#", "M"])
    #tilemap = apply_filter(tilemap, expand_mountains, ["#", ".", "M"])
    # tilemap = apply_filter(tilemap, expand_mountains, ["#", ".", "M"])
    # tilemap = apply_filter(tilemap, expand_shores, ["#", "."])

    for y,row in enumerate(tilemap):
        for x,tile in enumerate(row):
            print(tilemap[y][x], end='')
        print("")

    img = PIL.Image.new("RGB", (map_size, map_size))

    sea = (101, 183, 255)
    land = (52, 176, 0)
    mountains = (255, 255, 255)

    for y,row in enumerate(tilemap):
        for x,tile in enumerate(row):
            if tilemap[y][x] == ".":
                img.putpixel((x, y), sea)
            if tilemap[y][x] == "#":
                img.putpixel((x, y), land)
            if tilemap[y][x] == "M":
                img.putpixel((x, y), mountains)

    img.save("map.png")


procgen()
