import scrapy
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
import re

class DarkWebScraper(scrapy.Spider):
    name = "dark_web_scraper"
    start_urls = [
        "https://news.ycombinator.com/",
        "https://www.bbc.com/news",
        "https://www.theverge.com/",
    ]

    def __init__(self):
        options = Options()
        options.headless = True  # Run in headless mode
        
        # Set a custom profile if necessary
        options.add_argument("--profile");
        options.add_argument("/home/munz/.mozilla/firefox/selenium-profile")
        
        try:
            self.driver = webdriver.Firefox(options=options)
        except Exception as e:
            print(f"Error initializing WebDriver: {e}")
            self.driver = None

    def parse(self, response):
        if not self.driver:
            print("WebDriver not initialized. Skipping.")
            return

        self.driver.get(response.url)
        text_content = self.driver.page_source  # Get full page HTML

        # Define regex patterns for data extraction
        username_pattern = r"@([A-Za-z0-9_]{3,15})"  # Extracts usernames
        btc_address_pattern = r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"  # Bitcoin addresses
        eth_address_pattern = r"\b0x[a-fA-F0-9]{40}\b"  # Ethereum addresses

        usernames = re.findall(username_pattern, text_content)
        btc_addresses = re.findall(btc_address_pattern, text_content)
        eth_addresses = re.findall(eth_address_pattern, text_content)

        yield {
            "url": response.url,
            "usernames": list(set(usernames)),
            "btc_addresses": list(set(btc_addresses)),
            "eth_addresses": list(set(eth_addresses)),
        }

    def closed(self, reason):
        if self.driver:
            self.driver.quit()  # Close WebDriver properly

