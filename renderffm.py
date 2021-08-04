import PIL.Image
import sys

def render(inp, outp):
    maptiles = PIL.Image.open("maptiles.png")

    mapffm = open(inp, "rb")

    img = PIL.Image.new("RGB", (16*256, 16*256))

    for y in range(0, 256):
        for x in range(0, 256):
            tile = mapffm.read(1)[0]
            row = tile // 16
            col = tile % 16
            src = maptiles.crop((col*16, row*16, col*16 + 16, row*16 + 16))
            img.paste(src, (x*16, y*16, x*16+16, y*16+16))


    img.save(outp)

render(sys.argv[1], sys.argv[2])
