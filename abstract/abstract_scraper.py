import logging
import requests
from abc import ABC, abstractmethod

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

    def send_get_request(self, url, headers=None, cookies=None, params=None):
        try:
            response = requests.get(url, headers=headers, cookies=cookies, params=params)
            response.raise_for_status()  # Raise an error for bad status codes
            self.logger.info(f"GET request to {url} successful")
            return response
        except requests.RequestException as e:
            self.logger.error(f"GET request to {url} failed: {e}")
            return None

    def send_post_request(self, url, headers=None, cookies=None, params=None, json=None):
        try:
            response = requests.post(url, headers=headers, cookies=cookies, params=params, json=json)
            response.raise_for_status()  # Raise an error for bad status codes
            self.logger.info(f"POST request to {url} successful")
            return response
        except requests.RequestException as e:
            self.logger.error(f"POST request to {url} failed: {e}")
            return None

    # Feel free to add any other methods you think you might need or could be useful
