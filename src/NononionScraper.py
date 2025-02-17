import scrapy
import re

class DarkWebScraper(scrapy.Spider):
    name = "dark_web_scraper"
    start_urls = [
        "https://news.ycombinator.com/",
        "https://www.bbc.com/news",
        "https://www.theverge.com/"
    ]

    def parse(self, response):
        """Extract usernames and crypto addresses from web pages."""
        text_content = response.text  # Get raw HTML as text

        # Regex for finding usernames and crypto addresses
        username_pattern = r"@[a-zA-Z0-9_]{3,15}"  # Example: @username
        btc_address_pattern = r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"  # Bitcoin
        eth_address_pattern = r"\b0x[a-fA-F0-9]{40}\b"  # Ethereum

        # Find matches
        usernames = re.findall(username_pattern, text_content)
        btc_addresses = re.findall(btc_address_pattern, text_content)
        eth_addresses = re.findall(eth_address_pattern, text_content)

        yield {
            "url": response.url,
            "usernames": usernames,
            "btc_addresses": btc_addresses,
            "eth_addresses": eth_addresses,
        }
