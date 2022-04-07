import copy
import sys
import random

map_size = 64

class Map:
    def __init__(self, cp=None):
        if cp is not None:
            self.dmap = copy.copy(cp.dmap)
        else:
            self.dmap = []
            for x in range(0, map_size):
                self.dmap.append([' '] * map_size)

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

    def box(self, x, y, w, h, fill, pts):
        if w < 0:
            x += w
            w = -w
        if h < 0:
            y += h
            h = -h

        if fill:
            for i in range(y, y+h):
                for j in range(x, x+w):
                    self.put(j, i, "#")
        else:
            for i in range(y, y+h):
                for j in range(x, x+w):
                    self.put(j, i, ".")

            for i in range(y, y+h):
                self.put(x,   i, "#")
                self.put(x+w, i, "#")
                if i != y:
                    pts.add((x, i))
                    pts.add((x+w, i))
            for i in range(x, x+w):
                self.put(i, y,   "#")
                self.put(i, y+h, "#")
                if i != x:
                    pts.add((i, y))
                    pts.add((i, y+h))

            self.put(x+w, y+h, "#")

    def box_empty(self, x, y, w, h):
        if w < 0:
            x += w
            w = -w
        if h < 0:
            y += h
            h = -h
        for i in range(y, y+h):
            for j in range(x, x+w):
                if self.get(j, i) != " ":
                    return False
        return True

    def points(self):
        pts = []
        for j in range(0, map_size):
            for i in range(0, map_size):
                if self.dmap[j][i] == "#":
                    pts.append((i, j))
        return pts

def make_room(m, rw, rh, src, dst, xdir, ydir):
    pts = list(src)
    random.shuffle(pts)

    w = random.randint(rw[0], rw[1])
    h = random.randint(rh[0], rh[1])

    for p in pts:
        if xdir:
            if m.box_empty(p[0]+1, p[1]-(h//2), w, h) and m.get(p[0]-1, p[1]) == ".":
                # to the right
                m.box(p[0], p[1]-(h//2), w, h, False, dst)
                m.put(p[0], p[1], ".")
                break

            if m.box_empty(p[0]-1, p[1]-(h//2), -w, h) and m.get(p[0]+1, p[1]) == ".":
                # to the left
                m.box(p[0], p[1]-(h//2), -w, h, False, dst)
                m.put(p[0], p[1], ".")
                break

        if ydir:
            if m.box_empty(p[0]-(w//2), p[1]+1, w, h) and m.get(p[0], p[1]-1) == ".":
                # below
                m.box(p[0]-(w//2), p[1], w, h, False, dst)
                m.put(p[0], p[1], ".")
                break

            if m.box_empty(p[0]-(w//2), p[1]-1, w, -h) and m.get(p[0], p[1]+1) == ".":
                # above
                m.box(p[0]-(w//2), p[1], w, -h, False, dst)
                m.put(p[0], p[1], ".")
                break

def main():
    m = Map()

    hallway_pts = set()
    room_pts = set()

    m.box(30, 30, 5, 5, False, room_pts)

    for n in range(0, 6):
        if random.randint(0, 1) == 0:
            make_room(m, (6, 12), (2, 3), room_pts, hallway_pts, True, False)
        else:
            make_room(m, (2, 3), (6, 12), room_pts, hallway_pts, False, True)

        make_room(m, (4, 12), (4, 12), hallway_pts, room_pts, True, True)

    m.dump()

main()
