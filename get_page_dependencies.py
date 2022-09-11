import argparse
import os
from pathlib import Path

from typing import List

from zim_tools import is_zim_file, filepath_to_zim_pagepath, get_links, zim_pagelink_regex, zimlink_to_pagepath, zim_pagepath_to_filepath
from copy import deepcopy


def get_page_dependencies(links: list, pageformat: str, notebook_folder: Path, found_pages: list=[], source_filepath=None) -> list:
    result = found_pages.copy()
    for link in links:
        
        pagepath = zimlink_to_pagepath(link, source_filepath, notebook_folder)
        filepath = zim_pagepath_to_filepath(pagepath)

        found_pagepath = pagepath if pageformat == 'zimpage' else filepath
        # NOTE: Uncongruent capitalization is not supported yet
        if found_pagepath in result or not is_zim_file(notebook_folder / filepath):
            continue

        result.append(found_pagepath)
        for page_dependency in get_page_dependencies(get_links(notebook_folder / filepath, zim_pages_only=True), pageformat, notebook_folder, result, filepath):
            if page_dependency not in result:
                result.append(page_dependency)
    return result



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get all the page dependencies of the current zim page')
    parser.add_argument('pages', nargs='+')
    parser.add_argument('--format', default='filepath', help='The output format. It can be either filepath or zimpage')
    parser.add_argument('--notebook-folder', default='./', help='The pages will be relative to this directory')


    parsed = parser.parse_args()

    if parsed.format not in ['filepath', 'zimpage']:
        raise ValueError('The --format argument has incorrect value')

    pages = parsed.pages
    for i in range(len(pages)):
        try:
            pages[i] = filepath_to_zim_pagepath(Path(pages[i]))
        except:
            pass

    found_pages = get_page_dependencies(pages, parsed.format, Path(parsed.notebook_folder))

    for page in found_pages:
        print(page)

