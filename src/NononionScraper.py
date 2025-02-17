import scrapy
import re
import json

class DarkWebScraper(scrapy.Spider):
    name = "dark_web_scraper"

    # List of test websites (replace with .onion sites later)
    start_urls = [
        "https://news.ycombinator.com/",
        "https://www.bbc.com/news",
        "https://www.theverge.com/"
    ]

    def parse(self, response):
        """Extract usernames, emails, and crypto addresses."""
        text_content = response.text

        # 🔍 Regex for data extraction
        username_pattern = r"@[a-zA-Z0-9_]{3,15}"  # Example: @username
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"  # Example: user@example.com
        btc_address_pattern = r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b"  # Bitcoin address
        eth_address_pattern = r"\b0x[a-fA-F0-9]{40}\b"  # Ethereum address

        # Extract matches
        usernames = re.findall(username_pattern, text_content)
        emails = re.findall(email_pattern, text_content)
        btc_addresses = re.findall(btc_address_pattern, text_content)
        eth_addresses = re.findall(eth_address_pattern, text_content)

        # Save results to JSON
        data = {
            "url": response.url,
            "usernames": usernames,
            "emails": emails,
            "btc_addresses": btc_addresses,
            "eth_addresses": eth_addresses,
        }

        with open("results.json", "a") as file:
            json.dump(data, file, indent=4)

        yield data
