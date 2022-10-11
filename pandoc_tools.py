from pathlib import Path
import os

from typing import List
import subprocess
import json
from printers.json_list_rawtexts import json_get_rawtext_paths

from zim_tools import zim_pagelink_regex

import shutil

from filters.expand_zim_links import json_expand_links
from filters.include_code_blocks import json_transform_rawblocks_to_codeblocks
from printers.print_zim_links import json_get_links
from printers.json_list_media import json_get_media
from filters.prepare_for_dokuwiki import json_prepare_for_dokuwiki


def script_dir():
    return Path(os.path.dirname(os.path.abspath(__file__)))


def zim_filepath_to_json(filepath, filtered=True):
    CREATE_NO_WINDOW = 0x08000000
    p = subprocess.run([shutil.which('pandoc'), '-f', 'zimwiki_reader.lua', '-t', 'json', str(filepath)], capture_output=True, cwd=str(script_dir()), creationflags=CREATE_NO_WINDOW)
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
    CREATE_NO_WINDOW = 0x08000000
    p = subprocess.run(['pandoc', '-f', 'json', '-t', 'pdf', '--pdf-engine=xelatex', '-o', target_file] + pdf_options, input=json_file.encode(), cwd=notebook_folder, creationflags=CREATE_NO_WINDOW)
    p.check_returncode()

def get_media_from_json(json_input: dict) -> List[str]:
    # does not work on raw parsed zimwiki (has to be reanchored)
    return list(set(json_get_media(json_input)))

def get_rawtexts_from_json(json_input: dict) -> List[str]:
    return list(set(json_get_rawtext_paths(json_input)))

def json_to_dokuwiki(json_input, prefix) -> str:
    # does not work on raw parsed zimwiki
    prepared_json = json.dumps(json_prepare_for_dokuwiki(json_input, prefix=prefix))
    CREATE_NO_WINDOW = 0x08000000
    p = subprocess.run([shutil.which('pandoc'), '-f', 'json', '-t', 'dokuwiki'], input=prepared_json.encode(), capture_output=True, cwd=str(script_dir()), creationflags=CREATE_NO_WINDOW)
    return p.stdout.decode()

