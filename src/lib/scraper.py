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
        return self.links

    def scrape_links_to_text(self):
        items = []
        for link in self.links:
            r = re.compile(r'.+?>([^<]+)')
            res = r.search(str(link))
            items.append(res.group(1))
        return items

    def check_table_content(self):
        for row in self.session.query(Car_parts.manufacturer):
            brand = 'CASTROL'
            if brand not in row:
                self.add_scraped_data_to_db()
            else:
                print('Table is not empty')
                break

    def add_scraped_data_to_db(self):
        try:
            item_info = []
            for items in self.scrape_links_to_text():
                if "CASTROL" in items:
                    item_info.append(items)
                elif "STARLINE" in items:
                    item_info.append(items)
            for item in item_info:
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
                self.session.add_all(car_part)
                self.session.commit()
        except Exception as e:
            print(e)
