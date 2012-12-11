#!/usr/bin/env python
"""lolcat.py

Like cat, but with colours.

By Jackson Gatenby.
Inspired by https://github.com/busyloop/lolcat
"""
import sys
import random
import math

FREQ = 0.1
SPREAD = 3.0

def rgb_to_256(red, green, blue):
    """Convert an RGB-colour to the nearest 256-colour."""
    r, g, b = (int(x / 42.5) for x in (red, green, blue))
    if r == g == b:
        # the colour is close enough to grey. choose the right grey.
        return 232 + int((red + green + blue) / 32.001)
    else:
        # the colour is not grey
        r, g, b = (int(x * 6. / 256) for x in (red, green, blue))
        return 16 + 36 * r + 6 * g + b

def colour(string, red, green, blue):
    """Wrap a string with ANSI-colours"""
    prefix = "\033[38;5;{col}m".format(col=rgb_to_256(red, green, blue))
    suffix = "\033[0m"
    return prefix + string + suffix

def rainbow(pos):
    """Return the right colour for position pos"""
    red = math.sin(FREQ * pos) * 127 + 128
    green = math.sin(FREQ * pos + math.pi * 2 / 3) * 127 + 128
    blue = math.sin(FREQ * pos + math.pi * 4 / 3) * 127 + 128
    return (red, green, blue)

if __name__ == '__main__':
    files = sys.argv[1:] or ['-']
    offset = random.randint(0, 200)

    # lolcat each file.
    for fname in files:
        f = open(fname) if fname != '-' else sys.stdin
        for i, line in enumerate(f):
            for j, char in enumerate(line[:-1]):
                rgb = rainbow(offset + i + j / SPREAD)
                sys.stdout.write(colour(char, *rgb))
            sys.stdout.write(line[-1]) # print the newline normally
        f.close()
