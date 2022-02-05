import requests
from bs4 import BeautifulSoup
import threading
import warnings
from src.lib.utils import get_data_path

# ignore website warnings
warnings.filterwarnings('ignore')

DATA_PATH = get_data_path()


class Crawler:
    def __init__(self, seed):
        self.seed = seed
        self.urls_to_visit = [seed]
        self.visited_urls = []

    def crawl_links(self, url):
        content = self.get_html_content(url)
        self.save_content_to_html(content)
        self.get_links_from_html(content)

    def run_crawler(self):
        threads = []
        for url in self.urls_to_visit:
            try:
                tr = threading.Thread(target=self.crawl_links, args=(url,))
                threads.append(tr)
                tr.start()
                for tr in threads:
                    tr.join()
            except Exception as err:
                print(err)

    def get_html_content(self, url):
        try:
            # assign response to variable response(verify-escaping SSL Certificate)
            response = requests.get(url, verify=False)
            # set encoding of the web page
            response.encoding = 'utf-8'
            # set content as variable for page html text
            content = response.text
            # returns html.text(content)
            return content
        except requests.RequestException as err:
            print(f"No content to extract! Error: {err}")

    def save_content_to_html(self, content):
        self.content = content
        # create html document
        html_doc = DATA_PATH + 'motor_oils.html'
        # save html text of the response
        with open(html_doc, 'w') as f:
            f.write(content)

    def get_links_from_html(self, content):
        self.raw_links = []
        for raw_link in BeautifulSoup(content, features='html.parser').find_all('a', href=True):
            # add just the href tags <a> to list(links)
            if '/bg/autokelly/item/' in raw_link['href']:
                self.raw_links.append(raw_link)
        return self.raw_links

