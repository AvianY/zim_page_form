#!/usr/bin/env python3
 
import os, sys, io
from pathlib import Path
from typing import List
import json

from pandocfilters import applyJSONFilters, walk, Str

from zim_tools import find_notebook_parent_folder

def reduce_media_to_str(key, value, format, meta):
    if key == 'Image':
        return Str(value[2][0])
    elif key == 'Para':
        return walk(value, reduce_media_to_str, format, meta)
    else:
        return []

def json_get_media(json_input: dict):
    if 'meta' in json_input:
        meta = json_input['meta']
    elif json_input[0]:  # old API
        meta = json_input[0]['unMeta']
    else:
        meta = {}

    altered = walk(json_input, reduce_media_to_str, format, meta)

    return [Path(str(block['c']))
     for block in altered['blocks']]
    

if __name__ == '__main__':
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    source = input_stream.read()
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""

    links = json_get_media(json.loads(source))

    for link in links:
        print(link)
    