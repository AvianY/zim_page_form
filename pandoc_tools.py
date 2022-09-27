from pathlib import Path
import os

from typing import List
import subprocess
import json

from zim_tools import zim_pagelink_regex

import shutil

from expand_zim_links import json_expand_links
from include_code_blocks import json_transform_rawblocks_to_codeblocks
from print_zim_links import json_get_links
from json_list_media import json_get_media
from prepare_for_dokuwiki import json_prepare_for_dokuwiki


def script_dir():
    return Path(os.path.dirname(os.path.abspath(__file__)))


def zim_filepath_to_json(filepath, filtered=True):
    p = subprocess.run([shutil.which('pandoc'), '-f', 'zimwiki_reader.lua', '-t', 'json', str(filepath)], capture_output=True, cwd=str(script_dir()))
    print(p.stderr.decode())
    json_file = json.loads(p.stdout.decode())
    if filtered:
        json_file = json_transform_rawblocks_to_codeblocks(json_file)
        json_file = json_expand_links(json_file)

    return json_file

def get_links_from_json(json_input: dict, zim_pages_only=False) -> List[str]:
    links = json_get_links(json_input)
    result = []
    for link in links:
        if zim_pages_only and zim_pagelink_regex.match(link):
            result.append(link)
        elif not zim_pages_only:
            result.append(link)
    return result

def get_links_from_zim_filepath(filepath, zim_pages_only):
    json_file = zim_filepath_to_json(filepath, filtered=False)
    return get_links_from_json(json_file, zim_pages_only)

def create_pdf_from_json(json_dict: dict, target_file, pdf_options, notebook_folder) -> None:
    json_file: str = json.dumps(json_dict)
    p = subprocess.run(['pandoc', '-f', 'json', '-t', 'pdf', '--pdf-engine=xelatex', '-o', target_file] + pdf_options, input=json_file.encode(), cwd=notebook_folder)
    p.check_returncode()

def get_media_from_json(json_input: dict) -> List[str]:
    # does not work on raw parsed zimwiki (has to be reanchored)
    return list(set(json_get_media(json_input)))

def json_to_dokuwiki(json_input) -> str:
    # does not work on raw parsed zimwiki
    prepared_json = json.dumps(json_prepare_for_dokuwiki(json_input))
    p = subprocess.run([shutil.which('pandoc'), '-f', 'json', '-t', 'dokuwiki'], input=prepared_json.encode(), capture_output=True, cwd=str(script_dir()))
    return p.stdout.decode()

