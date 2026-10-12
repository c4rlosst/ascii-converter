# ascii-converter

Turn an image into ASCII art. The image is divided into a grid of cells (clusters of pixels), each cell is averaged to one brightness value, and that value picks a character.

## Setup

```
pip install pillow
```

## Usage

```
python ascii_converter.py photo.jpg
python ascii_converter.py photo.jpg -w 150 -r detailed
python ascii_converter.py photo.jpg -c            # colour (ANSI terminals)
python ascii_converter.py photo.jpg -i -o art.txt # inverted, saved to a file
```

| Flag | Meaning |
| --- | --- |
| `-w, --width` | Output width in characters (default 100). Larger = smaller cells = more detail. |
| `-r, --ramp` | `standard`, `detailed`, `blocks`, `simple`, or your own characters ordered dark to light. |
| `-i, --invert` | Flip the ramp, for light text on a dark background. |
| `-c, --color` | Colour each character with its cell's average colour. |
| `-o, --output` | Write to a file instead of printing. |
