# Zim page form

This tool makes it easier to take zimwiki files and generate a pdf or upload to them to a dokuwiki server.
It will use pandoc in the background in order to achieve this.

## Prerequisites

In order for this to run, you will, at the very least require [Pandoc](https://pandoc.org/code.html).
If you want to generate a pdf, you will also require [MikTex](https://miktex.org/) and if you want to upload your pages on a dokuwiki, you will require a [Dokuwiki server](https://www.dokuwiki.org/dokuwiki).

NOTE: generating a pdf for the first time will prompt MikTex to download a bunch of packages.


## Development

The required packages are in 'requirements.txt'.
In order to distribute the tool using pyinstaller, you need to use the following line (on windows):
`pyinstaller -F --add-data "zimwiki_reader.lua;." --add-data "build_form.ui;." --add-data "zim_pages_selector.ui;." --path .\venv\Lib\site-packages\ -n zim_page_form --noconsole main.py`

also, if you use a python virtual environment, you need to add `--paths venv\Lib\site-packages` at the end of previous command as well.

