import logging
import pandas as pd
from bs4 import BeautifulSoup
from abc import ABC
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

class AbstractScraper(ABC):
    
    def __init__(self, retailer, country):
        self.retailer = retailer
        self.country = country
        self.logger = self._get_logger()
        self.logger.info(f"Initialized scraper for retailer: {self.retailer}, country: {self.country}")
        
    def _get_logger(self):
        # Set up logger
        logger = logging.getLogger(f"{self.retailer}_{self.country}")
        logger.setLevel(logging.INFO)
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

class NotinoScraper(AbstractScraper):
    
    def __init__(self, retailer, country):
        super().__init__(retailer, country)
        self.base_url = "https://www.notino.cz/zubni-pasty/?f=1-9-2-4891-7183&npc=23"
        self.driver = self._setup_driver()
        
    def _setup_driver(self):
        options = Options()
        options.headless = True  # Run headless Chrome
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver
        
    def scrape(self):
        self.driver.get(self.base_url)
        products = []

        while True:
            soup = BeautifulSoup(self.driver.page_source, 'html.parser') 
            product_list = soup.find_all('div', class_='sc-bSstmL')

            for product in product_list:
                try:
                    product_name = product.find('h3', class_='eDlssm').text.strip() if product.find('h3', class_='eDlssm') else None
                    brand = product.find('h2', class_='kbBsIA').text.strip() if product.find('h2', class_='kbBsIA') else None
                    price = product.find('span', class_='dOVzXZ').text.strip() if product.find('span', class_='dOVzXZ') else None
                    stock = False if product.find('div', class_='sc-egTsrv') else True
                    price_after_sale = product.find('span', class_='price-discount').text.strip() if product.find('span', class_='price-discount') else None
                    promocode = product.find('span', class_='gfxrfw').text.strip() if product.find('span', class_='gfxrfw') else None
                    url = "https://www.notino.cz/" + product.find('a', class_='OFtqG')['href'] if product.find('a', class_='OFtqG') else None
                    image = product.find('img', class_='sc-iKOmoZ')['src'] if product.find('img', class_='sc-iKOmoZ') else None

                    products.append({
                        'product_name': product_name,
                        'brand': brand,
                        'price': price,
                        'price_after_sale': price_after_sale,
                        'promocode': promocode,
                        'stock': stock,
                        'url': url,
                        'image': image
                    })
                    
                except Exception as e:
                    self.logger.error(f"Error processing product: {e}")


            self.driver.quit()
            print(products)
            return pd.DataFrame(products)

def main(retailer: str, country: str) -> pd.DataFrame:
    scraper = NotinoScraper(retailer=retailer, country=country)
    products_df = scraper.scrape()
    return products_df

if __name__ == "__main__":
    df_raw = main(retailer="notino", country="cz")
    df_raw.to_csv("notino_raw.csv", index=False)
