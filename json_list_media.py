import pandoc

import argparse
import os, subprocess
from pathlib import Path
from typing import List

def json_list_media(json_files: List[Path]) -> List[Path]:
    result = []
    for filepath in json_files:
        with open(filepath, 'r') as f:
            doc = pandoc.read(f.read(), format='json')

            for elem in pandoc.iter(doc):
                if isinstance(elem, pandoc.types.Image):
                    result.append(Path(elem[2][0]))
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='get all the media contained in the provided json files')
    parser.add_argument('filepaths', nargs='+')

    parsed = parser.parse_args()

    media = json_list_media(parsed.filepaths)
    for medium in media:
        print(medium)
