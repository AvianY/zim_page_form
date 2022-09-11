import configparser
import os, re, pandoc
import sys
from pathlib import Path

from typing import Optional, Tuple
from configparser import ConfigParser

zim_pagepath_regex = re.compile('^([^:#+/]+)(:[^:#+/]+)*$')

zim_pagelink_regex = re.compile('^[:+]?([^:#+/]+)(:[^:#+/]+)*(#[^:#+/]+)?$')

zim_extension_inline_code_regex = re.compile('^\[\[([^]|]*)\|CODE:([^]|]*)\]\]$')


def find_first_relative_filepath(source_filepath: Path, relative_filepath: Path, notebook_folder: Path) -> Path:
    toplevel_zim_filename = Path(relative_filepath.parts[0]).with_suffix('.txt') # filename of the root page of the source
    source = Path(source_filepath)

    for dir in reversed(source.parents):
        if is_zim_file(notebook_folder / dir / toplevel_zim_filename):
            return dir / relative_filepath

    return source.parent / relative_filepath


'''
filename = name of file (example.txt)
filepath = relative filepath from notebook root (folder/example.txt)

pagepath = path made of pages (folder:example)
pagename = name of page (example) -- not really useful

absolute_link = link with absolute reference - starts with colon - (:folder:example.txt)
subrelative_link = link that refers to the subpage of the page it is in - starts with + - (+subpage) - not really useful
relative_link = link that refers to the most distant ancestor page that has the same initial name in common - it is convoluted ... -
'''

def zimlink_to_pagepath_section(link: str, source_filepath: Optional[Path], notebook_folder) -> Tuple[str, str]:
    joining_colon = '' if source_filepath is None else ':'

    pagepath: str
    section: Optional[str] = None

    pound_idx = link.rfind('#')
    if pound_idx != -1:
        section = link[pound_idx + 1:]
        link = link[0:pound_idx]

    if link[0] == ':': # absolute link
        link = link[1:]
        pagepath = link
    elif link[0] == '+': # subrelative link
        link = link[1:]
        pagepath = filepath_to_zim_pagepath(source_filepath) + joining_colon + link
    else: # relative link
        source_dir = Path() if source_filepath is None else source_filepath
        relative_path = find_first_relative_filepath(source_dir, zim_pagepath_to_filepath(link), notebook_folder)
        pagepath = filepath_to_zim_pagepath(relative_path)
    
    return pagepath, section

def zimlink_to_pagepath(link, source_filepath, notebook_folder) -> str:
    return zimlink_to_pagepath_section(link, source_filepath, notebook_folder)[0]

def zimlink_to_absolute_link(link, source_filepath, notebook_folder) -> str:
    return ':' + zimlink_to_pagepath_section(link, source_filepath, notebook_folder)[0]

def zimlink_to_filepath(link, source_filepath, notebook_folder) -> str:
    return zim_pagepath_to_filepath(zimlink_to_pagepath_section(link, source_filepath, notebook_folder)[0])

def zim_pagepath_to_filepath(pagepath: str) -> Path:
    slashed = pagepath.replace(':', '/') + '.txt'
    return Path(slashed.replace(' ', '_'))

def filepath_to_zim_pagepath(filename: Path, keepSuffix=False) -> str:
    if not keepSuffix:
        filename = filename.with_suffix('')
    coloned = ':'.join(filename.parts)
    return coloned.replace('_', ' ')

def is_zim_file(filepath: Path) -> bool:
    if not filepath.is_file(): return False
    with open(filepath, "r") as f:
        if f.readline() == 'Content-Type: text/x-zim-wiki\n':
            return True
    return False

def find_zim_pagepaths(root):
    result = []

    txt_filepaths = Path(root).glob('**/*.txt')
    for filepath in txt_filepaths:
        if is_zim_file(filepath):
            result.append(filepath)
    return result

def get_links(filename, zim_pages_only=False, reader_path='./'):
    result = []
    with open(filename, 'r') as f:
        parsed = pandoc.read(f.read(), format=os.path.join(reader_path, 'zimwiki_reader.lua'))
        for elem in pandoc.iter(parsed):
            if isinstance(elem, pandoc.types.Link):
                if zim_pages_only and not zim_pagelink_regex.match(elem[2][0]): continue
                result.append(elem[2][0])
    return result
