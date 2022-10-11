#!/usr/bin/env python3

from pathlib import Path

import re, sys, io
import json

from zim_tools import zimlink_to_pagepath, zim_pagelink_regex
from urllib.parse import unquote
from pandocfilters import toJSONFilter, walk, CodeBlock

from typing import Union, List


rawblock_language_description = re.compile('^[^(]*\(([^)]+)\)$')

def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def reanchor_file(relative_filepath, source_file):
    source_path = Path(source_file).with_suffix('')

    return str(source_path / relative_filepath)


def include_codeblocks(key, value, format, meta) -> Union[List[dict], dict, None]:
    source_filepath = meta['source_files']['c'][0]['c']
    if key == 'RawBlock':
        attr: tuple = ("", [], [])
        match = rawblock_language_description.match(value[0][0])
        if match is not None:
            attr[1].append(match.group(1))

        code = read_file(reanchor_file(value[1], source_filepath))
        return CodeBlock(attr, code)
    return None

def json_transform_rawblocks_to_codeblocks(json_input: dict, format=''):
    if 'meta' in json_input:
        meta = json_input['meta']
    elif json_input[0]:  # old API
        meta = json_input[0]['unMeta']
    else:
        meta = {}

    return walk(json_input, include_codeblocks, format, meta)

if __name__ == '__main__':
    input_stream = io.TextIOWrapper(sys.stdin.buffer, encoding='utf-8')
    source = input_stream.read()
    if len(sys.argv) > 1:
        format = sys.argv[1]
    else:
        format = ""

    sys.stdout.write(json.dumps(json_transform_rawblocks_to_codeblocks(json.loads(source), format)))
    