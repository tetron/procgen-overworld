import copy
import sys
import random

WALL = "#"
FLOOR = "."
INSIDE_FLOOR = "+"
EMPTY = " "
DOOR = "%"

map_size = 64

def check_rule(tilemap, rule, x, y, multi):
    for j in range(0, 3):
        for i in range(0, 3):
            ruletile = rule[0][j*3 + i]
            checktile = tilemap[(y+(j-1)) % map_size][(x+(i-1)) % map_size]
            if (checktile == ruletile) or (ruletile in multi and checktile in multi[ruletile]):
                pass
            else:
                return False
    return rule[1]

class Map:
    def __init__(self, cp=None):
        if cp is not None:
            self.dmap = copy.copy(cp.dmap)
        else:
            self.dmap = []
            for x in range(0, map_size):
                self.dmap.append([EMPTY] * map_size)

    def dup(self):
        return Map(self)

    def dump(self):
        for y in self.dmap:
            for x in y:
                sys.stdout.write(x)
            sys.stdout.write('\n')

    def put(self, x, y, v):
        self.dmap[y % map_size][x % map_size] = v

    def get(self, x, y):
        return self.dmap[y % map_size][x % map_size]

    def apply_filter(self, rules, multi, repeat, matcher=check_rule):
        tilemap = self.dmap
        recur = True
        while recur:
            newtilemap = []
            for x in range(0, map_size):
                newtilemap.append([tilemap[0][0]] * map_size)

            any_rule_matched = False
            for y,row in enumerate(tilemap):
                for x,tile in enumerate(row):
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

        self.dmap = tilemap

    def box(self, x, y, w, h, r, l, a, b, pts, inside):
        # r, l, a, b
        # sides where hallways can start
        # r(ight), l(eft), a(bove) b(elow)

        if w < 0:
            x += w + 1
            w = -w
        if h < 0:
            y += h + 1
            h = -h

        for i in range(y, y+h):
            for j in range(x, x+w):
                if inside and i < (y+h-1):
                    self.put(j, i, INSIDE_FLOOR)
                else:
                    self.put(j, i, FLOOR)

        for i in range(y, y+h):
            if l or inside:
                pts.add((x, i))
            if r or inside:
                pts.add((x+w-1, i))
        for i in range(x, x+w):
            if a or inside:
                pts.add((i, y))
            if b or inside:
                pts.add((i, y+h-1))

    def box_empty(self, x, y, w, h):
        if w < 0:
            x += w
            w = -w
        if h < 0:
            y += h
            h = -h
        for i in range(y, y+h):
            if i < 1 or i > (map_size-2):
                return False
            for j in range(x, x+w):
                if j < 1 or j > (map_size-2):
                    return False
                if self.get(j, i) != EMPTY:
                    return False
        return True

    def points(self):
        pts = []
        for j in range(0, map_size):
            for i in range(0, map_size):
                if self.dmap[j][i] == FLOOR:
                    pts.append((i, j))
        return pts

def place_box(m, rw, rh, src, dst, r, l, a, b, inside=False):
    pts = list(src)
    random.shuffle(pts)

    w = random.randint(rw[0], rw[1])
    h = random.randint(rh[0], rh[1])

    extend = 2

    wofs = random.randint(0, w-1)
    hofs = random.randint(0, h-1)

    for p in pts:
        if r:
            if m.box_empty(p[0]+1, p[1]-hofs-(extend-1), w+1, h+extend):
                # to the right
                m.box(p[0], p[1]-hofs, w, h, r, l, a, b, dst, inside)
                return True

        if l:
            if m.box_empty(p[0]-1, p[1]-hofs-(extend-1), -w-1, h+extend):
                # to the left
                m.box(p[0], p[1]-hofs, -w, h, r, l, a, b, dst, inside)
                return True

        if b:
            if m.box_empty(p[0]-wofs-(extend-1), p[1]+1, w+extend, h+1):
                # below
                m.box(p[0]-wofs, p[1], w, h, r, l, a, b, dst, inside)
                return True
        if a:
            if m.box_empty(p[0]-wofs-(extend-1), p[1]-1, w+extend, -h-1):
                # above
                m.box(p[0]-wofs, p[1], w, -h, r, l, a, b, dst, inside)
                return True
    return False

cleanup_floors = [
    [["_", FLOOR, "_",
      "_", EMPTY, FLOOR,
      "_", "_", "_"],
     FLOOR],
    [["_", "_", "_",
      "_", EMPTY, FLOOR,
      "_", FLOOR, "_"],
     FLOOR],
    [["_", "_", "_",
      FLOOR, EMPTY, "_",
      "_", FLOOR, "_"],
     FLOOR],
    [["_",   FLOOR, "_",
      FLOOR, EMPTY, "_",
      "_", "_", "_"],
     FLOOR],
]

remove_salient = [
    [[EMPTY, EMPTY, EMPTY,
      EMPTY, FLOOR, EMPTY,
      "_", FLOOR, "_"],
     EMPTY],
    [["_", EMPTY, EMPTY,
      FLOOR, FLOOR, EMPTY,
      "_", EMPTY, EMPTY],
     EMPTY],
    [["_", FLOOR, "_",
      EMPTY, FLOOR, EMPTY,
      EMPTY, EMPTY, EMPTY],
     EMPTY],
    [[EMPTY, EMPTY, "_",
      EMPTY, FLOOR, FLOOR,
      EMPTY, EMPTY, "_"],
     EMPTY],
    ]


add_walls = [
    [["*",   "*", "*",
      "*", EMPTY, "*",
      "*", FLOOR, "*"],
     WALL],
    [["*",     "*", "*",
      FLOOR, EMPTY, "*",
      "*",     "*", "*"],
     WALL],
    [["*", FLOOR, "*",
      "*", EMPTY, "*",
      "*", "*",  "*"],
     WALL],
    [["*",   "*",   "*",
      "*", EMPTY, FLOOR,
      "*",   "*",  "*"],
     WALL],

    [["*",   "*", "*",
      "*", EMPTY, "*",
      "*", "*", FLOOR],
     WALL],
    [["*",     "*", "*",
      "*", EMPTY, "*",
      FLOOR,     "*", "*"],
     WALL],
    [[FLOOR, "*", "*",
      "*", EMPTY, "*",
      "*", "*",  "*"],
     WALL],
    [["*",   "*",   FLOOR,
      "*", EMPTY, "*",
      "*",   "*",  "*"],
     WALL],

    [[INSIDE_FLOOR,   INSIDE_FLOOR,  "_",
      INSIDE_FLOOR,   INSIDE_FLOOR,  "_",
      "&",   INSIDE_FLOOR,  "_"],
     WALL],

    [["_",   INSIDE_FLOOR,  INSIDE_FLOOR,
      "_",   INSIDE_FLOOR,  INSIDE_FLOOR,
      "_",   INSIDE_FLOOR,  "&"],
     WALL],

    [["_",   "_",  "_",
      INSIDE_FLOOR,   INSIDE_FLOOR,  INSIDE_FLOOR,
      INSIDE_FLOOR,   INSIDE_FLOOR,  INSIDE_FLOOR],
     WALL],

    [[INSIDE_FLOOR,   INSIDE_FLOOR,  INSIDE_FLOOR,
      "&",   INSIDE_FLOOR,  "&",
      "_",   "_",  "_",],
     WALL],

    [[INSIDE_FLOOR,   INSIDE_FLOOR,  "_",
      "&",   INSIDE_FLOOR,  "_",
      "_",   "_",  "_",],
     WALL],

    [["_",   INSIDE_FLOOR,  INSIDE_FLOOR,
      "_",   INSIDE_FLOOR,  "&",
      "_",   "_",  "_",],
     WALL],

    [["_",   "_",  "_",
      "_",   INSIDE_FLOOR,  INSIDE_FLOOR,
      "_",   INSIDE_FLOOR,  INSIDE_FLOOR],
     WALL],

    [["_",   "_",  "_",
      INSIDE_FLOOR,  INSIDE_FLOOR, "_",
      INSIDE_FLOOR,  INSIDE_FLOOR, "_"],
     WALL],


    ]

def main():
    m = Map()

    hallway_pts = set()
    room_pts = set()

    #random.seed(1) # left
    # random.seed(5) # up
    # random.seed(7) # down
    # random.seed(10) # right

    #random.seed(7)

    m.box(30, 30, 5, 5, True, True, True, True, room_pts, False)

    hallwaywidth = 2
    hallwaylength = 8

    n = 40
    while n > 0:
        r = random.randint(0, 3)
        if r == 0:
            pl = place_box(m, (hallwaylength/2, hallwaylength), (1, hallwaywidth), room_pts, hallway_pts, True, True, False, False)
        if r == 1:
            pl = place_box(m, (1, hallwaywidth), (hallwaylength/2, hallwaylength), room_pts, hallway_pts, False, False, True, True)
        if r == 2:
            pl = place_box(m, (hallwaylength/2, hallwaylength), (1, hallwaywidth), hallway_pts, hallway_pts, True, True, False, False)
        if r == 3:
            pl = place_box(m, (1, hallwaywidth), (hallwaylength/2, hallwaylength), hallway_pts, hallway_pts, False, False, True, True)

        if not pl:
            continue

        n -= 1

    r = random.randint(3, 5)
    for n in range(0, r):
        place_box(m, (4, 10), (4, 10), hallway_pts, room_pts, True, True, True, True)

    r = random.randint(2, 4)
    for n in range(0, r):
        treasure_pts = set()
        place_box(m, (5, 10), (5, 10), hallway_pts | room_pts, treasure_pts, False, False, True, False, inside=True)
        treasure_pts = list(treasure_pts)
        random.shuffle(treasure_pts)
        for t in treasure_pts:
            if (m.dmap[t[1]][t[0]] == FLOOR and
                m.dmap[t[1]-1][t[0]] == INSIDE_FLOOR and
                m.dmap[t[1]-2][t[0]] == INSIDE_FLOOR and
                m.dmap[t[1]-1][t[0]-1] == INSIDE_FLOOR and
                m.dmap[t[1]-1][t[0]+1] == INSIDE_FLOOR):
                m.dmap[t[1]-1][t[0]] = DOOR
                break

    # for p in room_pts:
    #   m.dmap[p[1]][p[0]] = "2"

    # for p in hallway_pts:
    #    m.dmap[p[1]][p[0]] = "1"

    #for p in treasure_pts:
    #   m.dmap[p[1]][p[0]] = "3"

    if True:
        print("Removing salients")
        tilemap = m.apply_filter(remove_salient, {"_": [FLOOR, EMPTY]}, True)

        #print("Cleanup floors")
        #tilemap = m.apply_filter(cleanup_floors, {"_": [FLOOR, EMPTY]}, False)

        print("Adding walls")
        tilemap = m.apply_filter(add_walls, {"_": [FLOOR, EMPTY], "*": [FLOOR, EMPTY, INSIDE_FLOOR], "&": [INSIDE_FLOOR, DOOR]}, False)

    stairs_pts = m.points()
    # find corners, put stairs in a corner.
    random.shuffle(stairs_pts)
    m.dmap[stairs_pts[0][1]][stairs_pts[0][0]] = ">"
    m.dmap[stairs_pts[1][1]][stairs_pts[1][0]] = "<"

    m.dump()

main()
