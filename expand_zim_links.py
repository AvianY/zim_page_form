#!/usr/bin/env python3

from pathlib import Path

import sys, io
from zim_tools import filepath_to_zim_pagepath, is_url, zimlink_to_pagepath, zim_pagelink_regex, find_notebook_parent_folder
from urllib.parse import unquote
from pandocfilters import walk, Link, Image
import json


def reanchor_file(relative_filepath, source_file, relative_to=None):
    source_path = Path(source_file).with_suffix('')
    reanchored = (source_path / relative_filepath).resolve()
    if relative_to is not None:
        return str(reanchored.relative_to(relative_to))
    return str(reanchored)


def expand_zim_links(key, value, format, meta):
    source_filepath = Path(meta['source_files']['c'][0]['c'])
    notebook_folder = find_notebook_parent_folder(source_filepath)
    if key == 'Link':
        if zim_pagelink_regex.match(value[2][0]):
            value[2] = (zimlink_to_pagepath(value[2][0], source_filepath, notebook_folder), value[2][1])
            return Link(*value)
        elif not is_url(value[2][0]):
            value[2] = (reanchor_file(value[2][0], source_filepath, notebook_folder), value[2][1])
            return Link(*value)

    elif key == 'Image':
        # attr, caption, image = elem
        # src, title = image
        # identifier, classes, attributes = attr

        for i, attr_pair in enumerate(value[0][2]):
            if attr_pair[0] == 'href':
                link = unquote(attr_pair[1])
                value[0][2][i] = ('href', zimlink_to_pagepath(link, source_filepath, notebook_folder))

        # NOTE: I don't know if this should be here. It's not a link...
        if not Path(value[2][0]).is_absolute():
            value[2] = (reanchor_file(value[2][0], source_filepath, notebook_folder), value[2][1])
        return Image(*value)
    return None

def json_expand_links(json_input: dict, format=''):
    if 'meta' in json_input:
        meta = json_input['meta']
    elif json_input[0]:  # old API
        meta = json_input[0]['unMeta']
    else:
        meta = {}

    return walk(json_input, expand_zim_links, format, meta)

if __name__ == '__main__':
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    source = input_stream.read()
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""

    sys.stdout.write(json.dumps(json_expand_links(json.loads(source), format)))
    