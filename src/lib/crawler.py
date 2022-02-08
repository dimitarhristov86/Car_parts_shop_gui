import requests
from bs4 import BeautifulSoup
import threading
import warnings
from src.lib.utils import get_data_path

# ignore website warnings
warnings.filterwarnings('ignore')
# get data path for crawler
DATA_PATH = get_data_path()


class Crawler:
    def __init__(self, seed):
        # self.seed is set to be a link to web page
        self.seed = seed
        # self.urls_to_visit will be a list of seeds
        self.urls_to_visit = [seed]
        # self.visited_urls is a list with already visited seeds
        self.visited_urls = []

    def crawl_links(self, url):
        # variable content will be an actual html file
        content = self.get_html_content(url)
        # self.save_content_to_html will save content(text) as html file
        self.save_content_to_html(content)
        # self.get_links_from_html getting all links in html file
        self.get_links_from_html(content)

    def run_crawler(self):
        threads = []
        # loop through all links in self.urls_to_visit
        for url in self.urls_to_visit:
            try:
                # set tr as variable for a thread
                tr = threading.Thread(target=self.crawl_links, args=(url,))
                # add tr to a list of threads
                threads.append(tr)
                # actual starting of a thread
                tr.start()
                # loop through all tr in threads list
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
            # returns content as text
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
        #  loop through all links in html file using html parser and find just the <a> tags
        for raw_link in BeautifulSoup(content, features='html.parser').find_all('a', href=True):
            # loop through all href a tags
            if '/bg/autokelly/item/' in raw_link['href']:
                # add just the href tags <a> that contains /bg/autokelly/item/ in raw_link name
                self.raw_links.append(raw_link)
        return self.raw_links

