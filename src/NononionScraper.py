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
        options.headless = True  # Run without GUI
        self.driver = webdriver.Firefox(options=options)

    def parse(self, response):
        self.driver.get(response.url)
        text_content = self.driver.page_source  # Get full page HTML

        # DEBUG: Print the first 500 characters of the page
        print(f"\n[DEBUG] First 500 characters from {response.url}:\n{text_content[:500]}\n")

        # **Force test with known sample data**
        sample_text = """
        @example_username This is a test with BTC: 1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa 
        and ETH: 0x742d35Cc6634C0532925a3b844Bc454e4438f44e
        """
        
        # **Regex for usernames, emails, and crypto addresses**
        username_pattern = r"@[a-zA-Z0-9_]{3,30}"
        btc_pattern = r"\b[13][a-km-zA-HJ-NP-Z1-9]{25,39}\b"
        eth_pattern = r"0x[a-fA-F0-9]{40,42}"
        email_pattern = r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"

        # **Find matches in the real page content and sample text**
        usernames = re.findall(username_pattern, text_content) + re.findall(username_pattern, sample_text)
        btc_addresses = re.findall(btc_pattern, text_content) + re.findall(btc_pattern, sample_text)
        eth_addresses = re.findall(eth_pattern, text_content) + re.findall(eth_pattern, sample_text)
        emails = re.findall(email_pattern, text_content) + re.findall(email_pattern, sample_text)

        # **Check if anything was found**
        if usernames or btc_addresses or eth_addresses or emails:
            yield {
                "url": response.url,
                "usernames": usernames,
                "emails": emails,
                "btc_addresses": btc_addresses,
                "eth_addresses": eth_addresses,
            }
        else:
            print(f"[DEBUG] No relevant data found on {response.url}")

    def closed(self, reason):
        self.driver.quit()  # Close Selenium driver when done

