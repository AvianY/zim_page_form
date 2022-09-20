#!/usr/bin/env python3

import argparse
from pathlib import Path

import sys, io, os
from functools import partial

from pandocfilters import applyJSONFilters, walk

from urllib.parse import unquote


# TODO: join get_inline_links with get_block_links
def get_inline_links(key, value, format, meta):
    if key == 'Link':
        print(value[2][0])
    elif key == 'Image':
        # attr, caption, image = elem
        # src, title = image
        # identifier, classes, attributes = attr

        for i, attr_pair in enumerate(value[0][2]):
            if attr_pair[0] == 'href':
                print(unquote(value[0][2][i][1]))
    return None

def get_block_links(key, value, format, meta):
    if key == 'Para':
        return walk(value, get_inline_links, format, meta)
    return None


if __name__ == '__main__':
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    source = input_stream.read()
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""

    applyJSONFilters([get_block_links], source, format).split(os.linesep)

    