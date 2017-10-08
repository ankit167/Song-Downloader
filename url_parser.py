from bs4 import BeautifulSoup

class URLParserHref(object):
    @staticmethod
    def get_songs_page_url(page_data):
        soup = BeautifulSoup(page_data, "html.parser")
        for link in soup.select('div.single-songs a'):
            return link.get('href')

    @staticmethod
    def get_songs_url(song_data):
        soup = BeautifulSoup(song_data, "html.parser")
        for link in soup.select('div.page-down-btns a'):
            return link.get('href')