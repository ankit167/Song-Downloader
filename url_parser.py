from bs4 import BeautifulSoup
from BestMatchService import BestMatchService
from utils import trim

class URLParserHref(object):

    @staticmethod
    def get_songs_page_url(page_data, song):
        search_name_list = []
        search_href_list = []
        soup = BeautifulSoup(page_data, "html.parser")
        for link in soup.select('div.single-songs figcaption h3 a'):
            search_name_list.append(trim(link.get_text()))
            search_href_list.append(link.get('href'))
        best_match_index = BestMatchService.get_best_match(search_name_list, song)
        return search_href_list[best_match_index]

    @staticmethod
    def get_songs_url(song_data):
        soup = BeautifulSoup(song_data, "html.parser")
        for link in soup.select('div.page-down-btns a'):
            return link.get('href')