#!/usr/bin/python

import requests
import urllib
import re
import sys
import os
import warnings
import time
from url_parser import URLParserHref
from utils import url_resolver

base_url = "https://songs.pk"
search_url = base_url + "/search?"

class SongsPK():

    #Default directory path on your Desktop
    DIRPATH = os.path.expanduser('~/Desktop/songsPK_Collection')

    def write_mp3(self, mp3, filename=None):
        name = (mp3.geturl()).split('/')
        folder_name = os.path.expanduser(self.DIRPATH+'/') #+name[-2]+'/'
        if not os.path.exists(folder_name):
            os.system('mkdir %s' % folder_name)
        fullpath = folder_name+filename
        # print(fullpath)
        with open(fullpath, 'wb') as output:
            while True:
                buf = mp3.read(65536)  # Fixed the Buffer size
                if not buf:
                    break
                output.write(buf)


    def download(self, url_data=None, song_name=None):
        l = url_resolver(url_data)
        res, finalurl = l[0], str(l[1])

        if not finalurl.endswith('.mp3'):
            finalurl += '.mp3'

        if finalurl.endswith('.mp3') and \
            not finalurl.startswith('..'):
            with warnings.catch_warnings():
                warnings.simplefilter("ignore")
                self.write_mp3(
                    res,
                    filename=song_name + ".mp3"
                )

def get_content(url):
    return requests.get(url).content

def parse(song):
    p = re.compile("^[a-zA-Z ]*")
    song_search_string = p.search(song).group()
    return song_search_string    

def download_songs(song_list):
    spk = SongsPK()
    total_songs = len(song_list)
    songs_download_count = 0
    songs_not_downloaded = []
    
    for song in song_list:
        try:
            parsed_song = parse(song)
            if len(parsed_song) == 0:
                songs_not_downloaded.append(song)
                continue
            getVars = {'q': parsed_song}
            url = search_url + urllib.parse.urlencode(getVars)

            page = get_content(url)
            download_url = base_url + URLParserHref.get_songs_page_url(page, song)
            page = get_content(download_url)
            song_download_url = URLParserHref.get_songs_url(page)
            print("Downloading %s ..." % song)
            spk.download(song_download_url, song)
            songs_download_count += 1
        except Exception as e:
            print(e)
            songs_not_downloaded.append(song)

    print("%s out of %s songs downloaded" % (songs_download_count, total_songs)),
    if len(songs_not_downloaded) > 0:
        print("Following songs were not downloaded")
        for song in songs_not_downloaded:
            print(song),


def main():
    if len(sys.argv) < 2:
        print("Please enter file path")
        return

    file_path = sys.argv[1]
    if not os.path.exists(file_path):
         print("Path of the file is Invalid")
    with open(file_path) as f:
        content = f.readlines()

    song_set = set()
    for song in content:
        song_set.add(song.strip().lower())
    song_list = list(song_set)
    download_songs(song_list)
    

if __name__ == "__main__":
    start_time = time.time()
    main()
    elapsed_time = time.time() - start_time
    print("\n Time elapsed- %s \n" % elapsed_time)
