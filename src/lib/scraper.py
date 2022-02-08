import re
from src.lib.db import DB, Car_parts
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import create_engine

db = DB()
conn = db.get_connection_string()
engine = create_engine(conn)
Session = sessionmaker(bind=engine)


class Scraper:
    def __init__(self, crw_links):
        self.links = crw_links
        self.session = Session()
        self.session.begin()

    def get_crawler_links(self):
        # getting the crawled links from Crawler
        return self.links

    def scrape_links_to_text(self):
        items = []
        # loop through all links in Crawler raw_links
        for link in self.links:
            # using regex to extract only the text name from href <a> tags
            r = re.compile(r'.+?>([^<]+)')
            # search and save the result of regex search as string in variable res
            res = r.search(str(link))
            # add regex group to an items list
            items.append(res.group(1))
        return items

    def check_table_content(self):
        # loop through all data in manufacturer field in db table Car_parts
        for row in self.session.query(Car_parts.manufacturer):
            brand = 'CASTROL'
            # check if "CASTROL" name is already in manufacturer field in db table Car_parts
            if brand not in row:
                # if not then added to table - don't want to add Castrol brands twice in db table
                self.add_scraped_data_to_db()
            else:
                # otherwise, print in console and brake the loop
                print('Table is not empty')
                break

    def add_scraped_data_to_db(self):
        try:
            item_info = []
            # loop through all name text of scraped text
            for items in self.scrape_links_to_text():
                if "CASTROL" in items:
                    item_info.append(items)
                elif "STARLINE" in items:
                    item_info.append(items)
            # loop through all text in item_info list
            for item in item_info:
                # set variables with data from text
                item_name = item
                item_description = 'Engine oil for light vehicles'
                item_category = 'Engine oil'
                item_application = 'Use in light vehicles'
                item_manufacturer = item.split()[0]
                car_part = [Car_parts(
                        product_name=item_name,
                        product_description=item_description,
                        category=item_category,
                        application=item_application,
                        manufacturer=item_manufacturer)]
                # adding additional data to Car_parts table get it from car_part
                self.session.add_all(car_part)
                self.session.commit()
        except Exception as e:
            print(e)
