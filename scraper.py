from Crawler.crawler import Crawler
import threading


class Scraper:
    def __init__(self, base_url):
        self.base_url = base_url

    def get_crawler_links(self):
        # import raw_links from Crawler.crawler.py.get_links_from_html
        crawler_links = []
        # TODO
        for link in crawler_links:
            raw_url = self.base_url+link
            print(raw_url)
            return raw_url


if __name__ == '__main__':
    scraper = Scraper('https://www.autokelly.bg')
    scraper.get_crawler_links()
