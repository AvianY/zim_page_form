#!/usr/bin/env python3
 
import os, sys, io
from pathlib import Path
from typing import List
import json

from pandocfilters import walk, Str

from zim_tools import zim_pagelink_regex, is_url

def reduce_rawtext_path_to_str(key, value, format, meta):
    if key == 'Link':
        if not zim_pagelink_regex.match(value[2][0]) and not is_url(value[2][0]):
            return Str(value[2][0])
    elif key == 'Para':
        return walk(value, reduce_rawtext_path_to_str, format, meta)
    return []

def json_get_rawtext_paths(json_input: dict):
    if 'meta' in json_input:
        meta = json_input['meta']
    elif json_input[0]:  # old API
        meta = json_input[0]['unMeta']
    else:
        meta = {}

    altered = walk(json_input, reduce_rawtext_path_to_str, format, meta)

    return [Path(str(block['c'])) for block in altered['blocks']]
    

if __name__ == '__main__':
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    source = input_stream.read()
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""

    links = json_get_rawtext_paths(json.loads(source))

    for link in links:
        print(link)
    