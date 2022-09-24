import configparser
import os, re
import sys
from pathlib import Path
import subprocess
from typing import List

import json

from typing import List, Optional, Tuple

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

def zimlink_to_pagepath_section(link: str, anchor_filepath: Path, notebook_folder: Path) -> Tuple[str, Optional[str]]:
    if anchor_filepath.is_absolute():
        anchor_filepath = anchor_filepath.relative_to(notebook_folder)

    joining_colon = '' if anchor_filepath == Path() else ':'

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
        pagepath = filepath_to_zim_pagepath(anchor_filepath) + joining_colon + link
    else: # relative link
        relative_path = find_first_relative_filepath(anchor_filepath, zim_pagepath_to_filepath(link), notebook_folder)
        pagepath = filepath_to_zim_pagepath(relative_path)
    
    return pagepath, section

def zimlink_to_pagepath(link, source_filepath, notebook_folder) -> str:
    return zimlink_to_pagepath_section(link, source_filepath, notebook_folder)[0]

def zimlink_to_absolute_link(link, source_filepath, notebook_folder) -> str:
    return ':' + zimlink_to_pagepath(link, source_filepath, notebook_folder)

def zimlink_to_filepath(link, source_filepath, notebook_folder) -> Path:
    return zim_pagepath_to_filepath(zimlink_to_pagepath(link, source_filepath, notebook_folder))

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
    with open(filepath, "rb") as f:
        if f.readline() == b'Content-Type: text/x-zim-wiki' + os.linesep.encode():
            return True
    return False

def find_zim_pagepaths(root):
    result = []

    txt_filepaths = Path(root).glob('**/*.txt')
    for filepath in txt_filepaths:
        if is_zim_file(filepath):
            result.append(filepath)
    return result

def is_zim_notebook_folder(folderpath: Path):
    try:
        parser = configparser.ConfigParser()    
        parser.read(folderpath / 'notebook.zim')
        if 'Notebook' in parser and 'name' in parser['Notebook']:
            return True
    except:
        pass
    return False

def find_notebook_parent_folder(path: Path):
    if not path.is_file() and is_zim_notebook_folder(path):
        return path
    for parent_folder in path.parents:
        if is_zim_notebook_folder(parent_folder):
            return Path(parent_folder)
    return None
