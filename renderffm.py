import PIL.Image
import sys

def render(inp, outp, tiles="maptiles.png", map_size=256):
    maptiles = PIL.Image.open(tiles)

    mapffm = open(inp, "rb")

    img = PIL.Image.new("RGB", (16*map_size, 16*map_size))

    for y in range(0, map_size):
        for x in range(0, map_size):
            tile = mapffm.read(1)[0]
            row = tile // 16
            col = tile % 16
            src = maptiles.crop((col*16, row*16, col*16 + 16, row*16 + 16))
            img.paste(src, (x*16, y*16, x*16+16, y*16+16))


    img.save(outp)

if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
