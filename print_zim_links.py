#!/usr/bin/env python3

import sys, io, os

from pandocfilters import walk, Str
import json

from urllib.parse import unquote


def reduce_links_to_strings(key, value, format, meta):
    if key == 'Link':
        return Str(value[2][0])
    elif key == 'Image':
        # attr, caption, image = elem
        # src, title = image
        # identifier, classes, attributes = attr
        for i, attr_pair in enumerate(value[0][2]):
            if attr_pair[0] == 'href':
                return Str(unquote(value[0][2][i][1]))
    elif key == 'Para':
        return walk(value, reduce_links_to_strings, format, meta)
    else:
        return []

def json_get_links(json_input: dict):
    if 'meta' in json_input:
        meta = json_input['meta']
    elif json_input[0]:  # old API
        meta = json_input[0]['unMeta']
    else:
        meta = {}

    altered = walk(json_input, reduce_links_to_strings, format, meta)

    return [str(block['c']) for block in altered['blocks']]
    

if __name__ == '__main__':
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    source = input_stream.read()
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""

    links = json_get_links(json.loads(source))

    for link in links:
        print(link)
    