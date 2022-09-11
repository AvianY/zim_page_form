import pandoc

import argparse
import os, subprocess
from pathlib import Path

from typing import List, Optional, Callable
import re
from functools import partial

from zim_tools import zimlink_to_pagepath, zim_pagelink_regex
from urllib.parse import unquote

rawblock_language_description = re.compile('^[^(]*\(([^)]+)\)$')

def read_file(filepath):
    with open(filepath, 'r') as f:
        return f.read()

def reanchor_file(relative_filepath, source_file):
    source_path = Path(source_file).with_suffix('')

    return str(source_path / relative_filepath)

from contextlib import contextmanager

@contextmanager
def cwd(path):
    oldpwd = os.getcwd()
    os.chdir(path)
    try:
        yield
    finally:
        os.chdir(oldpwd)

def zimwiki_to_json(filepath, content: str, notebook_folder) -> str:
    # Temporarily change directory to where this script is, because pandoc library can't take readers from other directories for some reason
    with cwd(os.path.dirname(__file__)):
        doc = pandoc.read(content, format='zimwiki_reader.lua')
    for elem, path in pandoc.iter(doc, path=True):
        if isinstance(elem, pandoc.types.Link):
            if zim_pagelink_regex.match(elem[2][0]):
                elem[2] = (zimlink_to_pagepath(elem[2][0], filepath, notebook_folder), '')
        elif isinstance(elem, pandoc.types.Image):
            # attr, caption, image = elem
            # src, title = image
            # identifier, classes, attributes = attr

            for i, attr_pair in enumerate(elem[0][2]):
                if attr_pair[0] == 'href':
                    link = unquote(attr_pair[1])
                    elem[0][2][i] = ('href', zimlink_to_pagepath(link, filepath))                

            elem[2] = (reanchor_file(elem[2][0], filepath), '')
        elif isinstance(elem, pandoc.types.RawBlock):
            holder, index = path[-1]

            attr = ("", [], [])
            match = rawblock_language_description.match(elem[0][0])
            if match is not None:
                attr[1].append(match.group(1))

            code = read_file(reanchor_file(elem[1], filepath))
            holder[index] = pandoc.types.CodeBlock(attr, code)

    return pandoc.write(doc, format='json')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get all the page dependencies of the current zim page')
    parser.add_argument('filepath')

    parsed = parser.parse_args()

    filepath = parsed.filepath

    with open(filepath, 'r') as f:
        converted = zimwiki_to_json(filepath, f.read())
        print(converted)