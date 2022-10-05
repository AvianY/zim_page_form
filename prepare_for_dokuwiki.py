#!/usr/bin/env python3

import argparse
import os, subprocess, sys, io
import json
from pathlib import Path
from zim_tools import is_url, zim_pagelink_regex, zimlink_to_pagepath, filepath_to_zim_pagepath
from pandocfilters import toJSONFilter, Link, Image, Str, walk


def prepare_for_dokuwiki(key, value, format, meta):
    prefix = meta['prefix']['c']
    if key == 'Link':
        if zim_pagelink_regex.match(value[2][0]):
            # For some reason pandoc will turn link into a string if the name is the same as the link itself
            # Thats why we change the name to the last part (pagename) of the page it refers to
            if value[1][0] == value[2][0]:
                value[1][0] = Str(value[2][0].split(':')[-1])
            value[2] = (prefix + value[2][0], value[2][1])
        elif not is_url(value[2][0]):
            value[2] = (prefix + filepath_to_zim_pagepath(Path(value[2][0]), keepSuffix=True), value[2][1])
        return Link(*value)
    if key == 'Image':
        # This is really weird, but it is how dokuwiki behaves
        value[2] = (prefix + ':'.join(Path(value[2][0]).parts), value[2][1])
        return Image(*value)

    return None
    
def json_prepare_for_dokuwiki(json_input: dict, format='', prefix=''):
    if 'meta' in json_input:
        meta = json_input['meta']
    elif json_input[0]:  # old API
        meta = json_input[0]['unMeta']
    else:
        meta = {}
    meta['prefix'] = {'t': 'MetaString', 'c': prefix}

    return walk(json_input, prepare_for_dokuwiki, format, meta)

if __name__ == '__main__':
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    source = input_stream.read()
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""

    sys.stdout.write(json.dumps(json_prepare_for_dokuwiki(json.loads(source), format)))
    