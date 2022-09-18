#!/usr/bin/env python3
 
import os, sys, io
from pathlib import Path
from typing import List

from pandocfilters import applyJSONFilters, walk

def print_media(key, value, format, meta) -> List[Path]:
    if key == 'Image':
        print(value[2][0])
    return None

def get_block_links(key, value, format, meta):
    if key == 'Para':
        return walk(value, print_media, format, meta)
    return None

if __name__ == '__main__':
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    source = input_stream.read()
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""

    applyJSONFilters([print_media], source, format).split(os.linesep)

    