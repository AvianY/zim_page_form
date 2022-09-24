import argparse
import os
from pathlib import Path

from typing import List

from zim_tools import is_zim_file, filepath_to_zim_pagepath, zim_pagelink_regex, zimlink_to_pagepath, zim_pagepath_to_filepath
from pandoc_tools import get_links_from_zim_filepath

def norecursion(an=0,defret=[],initial=[]):
    """ Recursion/loop prevention function decorator

        For example, could be used when traversing a graph, which nodes assigned
        unique IDs and you would like to avoid loops.

        Keyword arguments:
        an -- position of function argument, which is used as unique id (0-based)
        defret -- default return value, which is returned when recursion is detected
        initial -- initial content of call stack. Array of unique ids

        Vadim Zaliva <lord@crocodile.org>
    """
    class decorate:
        def __init__(self):
            self.cs=initial
            
        def __call__(self, f):
            def new_f(*args, **kwds):
                id=args[an]
                if id in self.cs:
                    #print "recursion detected at '%s' in %s" % (id, str(self.cs))
                    return defret
                else:
                    self.cs.append(id)
                    x = f(*args, **kwds)
                    self.cs.remove(id)
                    return x
            return new_f
    return decorate()

@norecursion()
def get_page_dependencies(links: list, notebook_folder: Path, source_filepath) -> list:
    result = []
    for link in links:
        
        pagepath = zimlink_to_pagepath(link, source_filepath, notebook_folder)
        absolute_filepath = notebook_folder / zim_pagepath_to_filepath(pagepath)

        # NOTE: Uncongruent capitalization is not supported yet
        if pagepath in result or not is_zim_file(absolute_filepath):
            continue

        result.append(absolute_filepath)
        links = get_links_from_zim_filepath(absolute_filepath, zim_pages_only=True)
        for page_dependency in get_page_dependencies(links, notebook_folder, absolute_filepath):
            if page_dependency not in result:
                result.append(page_dependency)
    return result


def to_relative_filepaths(filepaths: List[Path], notebook_folder: Path):
    result = []

    for filepath in filepaths:
        if filepath.is_absolute():
            result.append(filepath.relative_to(notebook_folder))
        else:
            result.append(filepath)
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get all the page dependencies of the current zim page')
    parser.add_argument('filepaths', nargs='+', help='absolute/relative filepaths of the zim pages')
    parser.add_argument('--format', default='filepath', help='The output format. It can be either filepath, relative_filepath or zimpage')
    parser.add_argument('--notebook-folder', default='./', help='The pages will be relative to this directory')

    parsed = parser.parse_args()

    if parsed.format not in ['filepath', 'zimpage', 'relative_filepath']:
        raise ValueError('The --format argument has incorrect value')

    notebook_folder = Path(parsed.notebook_folder)
    filepaths = [Path(filepath) for filepath in parsed.filepaths]
    pages = []
    for filepath in to_relative_filepaths(filepaths, notebook_folder):
        pages.append(filepath_to_zim_pagepath(Path(filepath)))

    found_filepaths: List[Path] = get_page_dependencies(pages, notebook_folder, notebook_folder)

    for filepath in found_filepaths:
        relative_filepath = filepath.relative_to(parsed.notebook_folder)
        if parsed.format == 'filepath':
            print(filepath)
        elif parsed.format == 'relative_filepath':
            print(relative_filepath)
        else:
            print(filepath_to_zim_pagepath(relative_filepath))
