#!/usr/bin/env python3

from pathlib import Path

import re

from zim_tools import zimlink_to_pagepath, zim_pagelink_regex
from urllib.parse import unquote
from pandocfilters import toJSONFilter, walk, CodeBlock


rawblock_language_description = re.compile('^[^(]*\(([^)]+)\)$')

def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def reanchor_file(relative_filepath, source_file):
    source_path = Path(source_file).with_suffix('')

    return str(source_path / relative_filepath)


def include_code_blocks(key, value, format, meta) -> str:
    source_filepath = meta['source_files']['c'][0]['c']
    if key == 'RawBlock':
        attr = ("", [], [])
        match = rawblock_language_description.match(value[0][0])
        if match is not None:
            attr[1].append(match.group(1))

        code = read_file(reanchor_file(value[1], source_filepath))
        return CodeBlock(attr, code)
    return None


if __name__ == '__main__':
    toJSONFilter(include_code_blocks)

