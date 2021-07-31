import random
import PIL.Image

pf = .2

def perturb_point(basemap, x0, y0, x1, y1, r0):
    if abs(x0 - x1) <= 1 and abs(y0 - y1) <= 1:
        if x0 == x1 or y0 == y1:
            return
        # the x0, y0 and x1, y1 corners are already set
        # need to set the x0, y1, and x1, y0 corners
        midp = (basemap[y0][x0]+basemap[y1][x1])/2.0
        basemap[y0][x1] = midp + random.uniform(-r0, r0)
        basemap[y1][x0] = midp + random.uniform(-r0, r0)
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

    #x2 = int((x1+x0)/2)
    #y2 = int((y1+y0)/2)

    if basemap[y2][x2] != .5:
        return

    #print(basemap[y0][x0],basemap[y1][x0],basemap[y0][x1],basemap[y1][x1])
    midp = (basemap[y0][x0]+basemap[y1][x0]+basemap[y0][x1]+basemap[y1][x1])/4.0
    basemap[y2][x2] = midp + random.uniform(-r0, r0)
    #print(x0, y0, x1, y1, x2, y2, midp, basemap[y2][x2], r0)

    perturb_point(basemap, x0, y0, x2, y2, r0*pf)
    perturb_point(basemap, x2, y0, x1, y2, r0*pf)
    perturb_point(basemap, x0, y2, x2, y1, r0*pf)
    perturb_point(basemap, x2, y2, x1, y1, r0*pf)


def remove_tiles(tilemap):
    newtilemap = []
    for x in range(0, 256):
        newtilemap.append(['.'] * 256)

    for y,row in enumerate(tilemap):
        for x,tile in enumerate(row):
            newtilemap[y][x] = tilemap[y][x]

    for y,row in enumerate(tilemap):
        for x,tile in enumerate(row):
            if tile == '#':
                if (newtilemap[y-1][x-1] == '.' and
                    newtilemap[y-1][x] == '.' and
                    newtilemap[y-1][x+1] == '.' and
                    newtilemap[y][x-1] == '.' and
                    newtilemap[y][x+1] == '.' and
                    newtilemap[y+1][x-1] == '.' and
                    newtilemap[y+1][x] == '.' and
                    newtilemap[y+1][x+1] == '.'):
                    newtilemap[y][x] = '.'

    return newtilemap

def expand_tiles(tilemap, expand, repl):
    newtilemap = []
    for x in range(0, 256):
        newtilemap.append(['.'] * 256)

    for y,row in enumerate(tilemap):
        for x,tile in enumerate(row):
            newtilemap[y][x] = tilemap[y][x]

    for y,row in enumerate(tilemap):
        for x,tile in enumerate(row):
            if tile == expand:
                if newtilemap[y-1][x-1] in repl:
                    newtilemap[y-1][x-1] = expand
                if newtilemap[y-1][x] in repl:
                    newtilemap[y-1][x] = expand
                if newtilemap[y-1][x+1] in repl:
                    newtilemap[y-1][x+1] = expand

                if newtilemap[y][x-1] in repl:
                    newtilemap[y][x-1] = expand
                if newtilemap[y][x+1] in repl:
                    newtilemap[y][x+1] = expand

                if newtilemap[y+1][x-1] in repl:
                    newtilemap[y+1][x-1] = expand
                if newtilemap[y+1][x] in repl:
                    newtilemap[y+1][x] = expand
                if newtilemap[y+1][x+1] in repl:
                    newtilemap[y+1][x+1] = expand

    return newtilemap

eliminate_islands = [
    ["..."
     ".#."
     "...",
     "."]]

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
    for x in range(0, 256):
        newtilemap.append(['.'] * 256)

    for y,row in enumerate(tilemap):
        if y == 0 or y == 255:
            continue
        for x,tile in enumerate(row):
            if x == 0 or x == 255:
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
    for x in range(0, 256):
        basemap.append([.5] * 256)

    basemap[127][127] = 1

    perturb_point(basemap, 5, 5, 127, 127, .5)
    perturb_point(basemap, 127, 127, 250, 250, .5)
    perturb_point(basemap, 5, 127, 127, 250, .5)
    perturb_point(basemap, 127, 5, 250, 127, .5)

    tilemap = []
    for x in range(0, 256):
        tilemap.append(['.'] * 256)

    for y,row in enumerate(basemap):
        for x,tile in enumerate(row):
            if tile > .527:
                tilemap[x][y] = 'M'
            elif tile > .501:
                tilemap[x][y] = '#'
        print("")

    tilemap = apply_filter(tilemap, eliminate_islands, [])
    tilemap = apply_filter(tilemap, expand_mountains, ["#", ".", "M"])
    tilemap = apply_filter(tilemap, expand_shores, ["#", "."])

    print("After")
    for y,row in enumerate(tilemap):
        for x,tile in enumerate(row):
            print(tilemap[y][x], end='')
        print("")

    img = PIL.Image.new("RGB", (256, 256))

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
