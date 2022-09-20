#!/usr/bin/env python3

import argparse
import os, subprocess
from pathlib import Path
from zim_tools import zim_pagelink_regex, zimlink_to_pagepath
from pandocfilters import toJSONFilter, Link, Image, Str


def prepare_for_dokuwiki(key, value, format, meta):
    if key == 'Link':
        if zim_pagelink_regex.match(value[2][0]):
            # For some reason pandoc will turn link into a string if the name is the same as the link itself
            # Thats why we change the name to the last part (pagename) of the page it refers to
            value[1][0] = Str(value[2][0].split(':')[-1])
            return Link(*value)
    if key == 'Image':
        # This is really weird, but it is how dokuwiki behaves
        value[2] = (value[2][0].replace('/', ':'), value[2][1])
        return Image(*value)

    return None

if __name__ == '__main__':
    toJSONFilter(prepare_for_dokuwiki)