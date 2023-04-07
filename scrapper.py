import logging
from bs4 import BeautifulSoup
import requests


class fetch:
    """
    class to fetch data from a url using requests package
    """

    def __init__(self, url: str) -> None:
        """initialise
        Args:
            url (str): url from where the data is to be fetched
        """
        self.__url = url

    def get(self) -> requests:
        """fetch content from url
        Returns:
            requests: request object of get request
        """
        r = requests.get(self.__url)
        logging.info('satus code for get request on %s : %s',
                     self.__url, r.status_code)
        return r


class scrape:
    """scrape verge
    """

    def __init__(self, url: str) -> None:
        """initialise
        Args:
            url (str): url for webpage
        """
        self.__url = url

    def __bsobjget(self, url, features='') -> BeautifulSoup:
        obj = fetch(url)
        res = obj.get()
        if res.status_code != 200:
            raise Exception('bad response')
        soup = BeautifulSoup(res.content, features=features)
        return soup

    def __processurlsoup(self, soupurl, i=0):
        details = {}

        # id
        details['id'] = i

        # url of article
        url = soupurl.find('loc').text
        details['url'] = url

        # headline for article
        headline = soupurl.find('news:title').text
        details['headline'] = headline

        # author
        bs = self.__bsobjget(url, features='html.parser')
        s = bs.find('span', attrs={
                    "class": "font-medium uppercase tracking-6"})
        author = s.a.text
        details['author'] = author

        # publication date
        date = soupurl.find('news:publication_date').text.split('T')[0]
        details['date'] = date

        logging.info("Gathering details %i is successful", i)

        return details

    def scraping(self, x=0, limit=-1):
        soup1 = self.__bsobjget(self.__url+'/sitemaps/google_news', 'lxml-xml')
        if limit == -1:
            urls = soup1.find_all('url')
        else:
            urls = soup1.find_all('url', limit=limit)
        # print(urls)
        details = []
        for i, url in enumerate(urls):
            if url == None:
                continue
            logging.info('Processing article id: %i', i+x)
            details.append(self.__processurlsoup(url, i+x))
        return details
