import dokuwiki
import argparse
import configparser

from zim_tools import filepath_to_zim_pagepath

def read_into_lines(filename):
    with open(filename) as f:
        lines = f.readlines()
        return [line.rstrip() for line in lines]

def read_into_string(filename):
    with open(filename, 'rb') as f:
        return f.read()

def read_credentials(filename):
    confparser = configparser.ConfigParser()
    confparser.read(filename)

    return {
        'server': confparser['credentials']['server'],
        'username': confparser['credentials']['username'],
        'password': confparser['credentials']['password']
    }

def upload_files_to_dokuwiki(pages, media, credentials):
    wiki = dokuwiki.DokuWiki(credentials['server'], credentials['username'], credentials['password'])
    
    for pagepath in pages:
        wiki.pages.set(pagepath, pages[pagepath])

    for mediapath in media:
        wiki.medias.set(mediapath, media[mediapath])

def delete_files_from_dokuwiki(pagenames, medianames, credentials):
    wiki = dokuwiki.DokuWiki(credentials['server'], credentials['username'], credentials['password'])

    for filename in pagenames:
        wiki.pages.delete(filename)

    for filename in medianames:
        wiki.medias.delete(filename)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Upload dokuwiki pages and media')
    parser.add_argument('pages_file', help='File with a list of pages that will be uploaded')
    parser.add_argument('media_file', help='File with a list of media that will be uploaded')
    parser.add_argument('credentials_file', help='File with dokuwiki credentials (server, username, password)')
    parser.add_argument('-d', action='store_true', help='Delete specified pages and media')

    args = parser.parse_args()

    credentials = read_credentials(args.credentials_file)
    zim_filenames = read_into_lines(args.pages_file)
    media_filenames = read_into_lines(args.media_file)

    try:
        if not args.d:
            upload_files_to_dokuwiki(zim_filenames, media_filenames, credentials)
        else:
            delete_files_from_dokuwiki(zim_filenames, media_filenames, credentials)
    except (dokuwiki.DokuWikiError, Exception) as err:
        print(f'unable to connect: {err}')
        exit(1)