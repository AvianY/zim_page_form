import pandoc

import argparse
import os, subprocess
from pathlib import Path
from zim_tools import zim_pagelink_regex, zimlink_to_pagepath


def json_to_dokuwiki(filepath: str, content: str) -> str:
    doc = pandoc.read(content, format='json')

    for elem in pandoc.iter(doc):
        if isinstance(elem, pandoc.types.Link):
            if zim_pagelink_regex.match(elem[2][0]):
                elem[1][0] = pandoc.types.Str(elem[2][0].split(':')[-1])
        if isinstance(elem, pandoc.types.Image):
            # This is really weird, but it is how dokuwiki behaves
            elem[2] = (elem[2][0].replace('/', ':'), elem[2][1])

    return pandoc.write(doc, format='dokuwiki')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Convert the provided json file to dokuwiki file')
    parser.add_argument('filepath')

    parsed = parser.parse_args()

    filepath = parsed.filepath

    with open(filepath, 'r') as f:
        converted = json_to_dokuwiki(filepath, f.read())
        print(converted)
