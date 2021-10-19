import requests
from bs4 import BeautifulSoup


class Crawler:
    def __init__(self, seed):
        self.seed = seed
        self.urls_to_visit = [seed]
        self.visited_urls = []

    def run_crawler(self):
        for url in self.urls_to_visit:
            try:
                content = self.get_html_content(url)
                self.save_content_to_html(content)
                self.get_links_from_html()
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
        html_doc = './html_data/motor_oils.html'
        # save html text of the response
        with open(html_doc, 'w') as f:
            f.write(content)

    def get_links_from_html(self):
        self.raw_links = []
        for raw_link in BeautifulSoup(self.content, features='html.parser').find_all('a', href=True):
            # add just the href tags to a list(links)
            if '/bg/autokelly/item/' in raw_link['href']:
                self.raw_links.append(raw_link)
        return self.raw_links


if __name__ == '__main__':
    crawler = Crawler('https://www.autokelly.bg/bg/products/43758570.html?ids=39849642;51224611')
    crawler.run_crawler()
