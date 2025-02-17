import scrapy
import re
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from scrapy.http import HtmlResponse

class DarkWebScraper(scrapy.Spider):
    name = "dark_web_scraper"

    start_urls = [
        "https://news.ycombinator.com/",
        "https://www.bbc.com/news",
        "https://www.theverge.com/"
    ]

    def __init__(self):
options = Options()
options.headless = True  # Run in headless mode
profile_path = "/home/munz/snap/firefox/common/.mozilla/firefox/v0pl6ivt.Selenium-Profile"
options.set_preference("profile", profile_path)

driver = webdriver.Firefox(options=options)

    def parse(self, response):
        """Extract usernames, emails, and crypto addresses."""
        
        self.driver.get(response.url)  # Load page in Selenium
        text_content = self.driver.page_source  # Get full page HTML
        
        # Regex for common data types
        username_pattern = r"@[a-zA-Z0-9_]{3,15}"  # Example: @username
        email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"  # Emails
        btc_address_pattern = r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"  # Bitcoin
        eth_address_pattern = r"\b0x[a-fA-F0-9]{40}\b"  # Ethereum

        # Find matches
        usernames = re.findall(username_pattern, text_content)
        emails = re.findall(email_pattern, text_content)
        btc_addresses = re.findall(btc_address_pattern, text_content)
        eth_addresses = re.findall(eth_address_pattern, text_content)

        yield {
            "url": response.url,
            "usernames": list(set(usernames)),
            "emails": list(set(emails)),
            "btc_addresses": list(set(btc_addresses)),
            "eth_addresses": list(set(eth_addresses)),
        }

    def closed(self, reason):
        """Close Selenium driver when Scrapy is done."""
        self.driver.quit()
