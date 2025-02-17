import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re

class DarkWebScraper(scrapy.Spider):
    name = "dark_web_scraper"
    start_urls = [
        "https://news.ycombinator.com/",
        "https://www.bbc.com/news",
        "https://www.theverge.com/"
    ]

    def __init__(self):
        options = Options()
        options.headless = True  # Run without GUI
        self.driver = webdriver.Firefox(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        text_content = self.driver.page_source  # Get full page HTML

        username_pattern = r"@[a-zA-Z0-9_]{3,15}"
        btc_address_pattern = r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"
        eth_address_pattern = r"\b0x[a-fA-F0-9]{40}\b"

        usernames = re.findall(username_pattern, text_content)
        btc_addresses = re.findall(btc_address_pattern, text_content)
        eth_addresses = re.findall(eth_address_pattern, text_content)

        yield {
            "url": response.url,
            "usernames": usernames,
            "btc_addresses": btc_addresses,
            "eth_addresses": eth_addresses,
        }

    def closed(self, reason):
        self.driver.quit()  # Close Selenium driver when done
