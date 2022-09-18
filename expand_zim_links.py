#!/usr/bin/env python3

from pathlib import Path

from zim_tools import zimlink_to_pagepath, zim_pagelink_regex, find_notebook_parent_folder
from urllib.parse import unquote
from pandocfilters import toJSONFilter, walk, Link, Image


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
            value[2] = (zimlink_to_pagepath(value[2][0], source_filepath, notebook_folder), '')
            return Link(*value)
    elif key == 'Image':
        # attr, caption, image = elem
        # src, title = image
        # identifier, classes, attributes = attr

        for i, attr_pair in enumerate(value[0][2]):
            if attr_pair[2][0] == 'href':
                link = unquote(attr_pair[1])
                value[0][2][i] = ('href', zimlink_to_pagepath(link, source_filepath, notebook_folder))

        # NOTE: I don't know if this should be here. It's not a link...
        value[2] = (reanchor_file(value[2][0], source_filepath, notebook_folder), '')
        return Image(*value)
    return None

if __name__ == '__main__':
    toJSONFilter(expand_zim_links)

