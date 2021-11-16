import re


class Scraper:
    def __init__(self, crw_links):
        self.links = crw_links

    def get_crawler_links(self):
        return self.links

    def scrape_links_to_text(self):
        items = []
        for link in self.links:
            r = re.compile(r'.+?>([^<]+)')
            res = r.search(str(link))
            items.append(res.group(1))
        return items

