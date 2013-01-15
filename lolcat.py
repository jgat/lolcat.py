#!/usr/bin/env python
"""lolcat.py

Like cat, but with colours.

By Jackson Gatenby.
Inspired by https://github.com/busyloop/lolcat
"""
import sys
import random
import math
import argparse

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

def lol(string, offset=random.randint(0, 200)):
    """lol a string."""
    result = ''
    for i, line in enumerate(string.split('\n')):
        for j, char in enumerate(line):
            # colour is based on the sum of the row/column, to a scaling factor
            rgb = rainbow(offset + i + j / SPREAD)
            result += colour(char, *rgb)
        result += '\n' # print the newline normally

    if string.endswith('\n'):
        result = result[:-1] # avoid an extra newline at the end
    return result

def cat(f):
    """cat a file."""
    return f.read()

class LolArgumentParser(argparse.ArgumentParser):
    def format_help(self):
        return lol(super(LolArgumentParser, self).format_help())

if __name__ == '__main__':
    parser = LolArgumentParser(description="Like cat, but with colours.")
    parser.add_argument('files', nargs='*', default=['-'], metavar='file',
        help='Files to cat. "-" is stdin. Default is stdin.')
    args = parser.parse_args()

    # lolcat each file.
    for fname in args.files:
        f = open(fname) if fname != '-' else sys.stdin
        with f:
            sys.stdout.write(lol(cat(f)))
