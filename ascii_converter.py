"""Turn an image into ASCII art.

The image is divided into a grid of cells (clusters of pixels). Each cell is
averaged down to one brightness value, which picks a character from a ramp
ordered dark -> light.
"""

import argparse
import sys

from PIL import Image, ImageOps

# Dark -> light. A dark pixel gets a "dense" character.
RAMPS = {
    "standard": "@%#*+=-:. ",
    "detailed": "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\\|()1{}[]?-_+~<>i!lI;:,\"^`'. ",
    "blocks": "█▓▒░ ",
    "simple": "#. ",
}

# Terminal characters are roughly twice as tall as they are wide, so each cell
# covers twice as many pixel rows as columns to keep the proportions right.
CELL_ASPECT = 2.0


def convert(image, cols, ramp, invert=False, color=False):
    """Return the ASCII art for `image` as a string, `cols` characters wide."""
    image = ImageOps.exif_transpose(image).convert("RGB")
    width, height = image.size
    rows = max(1, round(cols * height / width / CELL_ASPECT))

    # BOX resampling averages every pixel inside each cell: one cell -> one pixel.
    cells = image.resize((cols, rows), Image.BOX)
    gray = cells.convert("L")

    chars = ramp[::-1] if invert else ramp
    last = len(chars) - 1

    lines = []
    for y in range(rows):
        line = []
        for x in range(cols):
            char = chars[gray.getpixel((x, y)) * last // 255]
            if color:
                r, g, b = cells.getpixel((x, y))
                char = f"\x1b[38;2;{r};{g};{b}m{char}"
            line.append(char)
        lines.append("".join(line) + ("\x1b[0m" if color else ""))
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description="Convert an image to ASCII art.")
    parser.add_argument("image", help="path to the input image")
    parser.add_argument("-w", "--width", type=int, default=100,
                        help="output width in characters (default: 100)")
    parser.add_argument("-r", "--ramp", default="standard",
                        help=f"ramp name ({', '.join(RAMPS)}) or your own characters, dark to light")
    parser.add_argument("-i", "--invert", action="store_true",
                        help="flip the ramp (use for light text on a dark background)")
    parser.add_argument("-c", "--color", action="store_true",
                        help="colour each character with its cell's average colour (ANSI terminals)")
    parser.add_argument("-o", "--output", help="write to a file instead of the terminal")
    args = parser.parse_args()

    if args.width < 1:
        parser.error("--width must be at least 1")
    ramp = RAMPS.get(args.ramp, args.ramp)
    if len(ramp) < 2:
        parser.error("a ramp needs at least 2 characters")

    try:
        with Image.open(args.image) as image:
            art = convert(image, args.width, ramp, args.invert, args.color and not args.output)
    except OSError as err:
        sys.exit(f"Could not open {args.image}: {err}")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(art + "\n")
    else:
        sys.stdout.reconfigure(encoding="utf-8")
        print(art)


if __name__ == "__main__":
    main()
