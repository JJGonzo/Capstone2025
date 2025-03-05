import scrapy
import requests
import json
import time
from bs4 import BeautifulSoup

# Tor Proxy Configuration
TOR_PROXY = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

# List of .onion sites to scrape
target_domains = [
    "http://expyuzz4wqqyqhjn.onion",  # Tor Project
    "http://duckduckgogg42xjoc72x3sjasowoarfbgcmvfimaftt6twagswzczad.onion",  # DuckDuckGo
    "http://msydqstlz2kzerdg.onion",  # Ahmia Search Engine
    "http://www.propub3r6espa33w.onion/",  # ProPublica
    "http://zqktlwiuavvvqqt4ybvgvi7tyo4hjl5xz5h3px5c5akk3qq4h4tzufqd.onion"  # The Hidden Wiki
]

class DarkWebSpider(scrapy.Spider):
    name = "darkweb_scraper"

    def start_requests(self):
        for url in target_domains:
            yield scrapy.Request(url, callback=self.parse, meta={"proxy": TOR_PROXY["http"]})

    def parse(self, response):
        soup = BeautifulSoup(response.text, "html.parser")

        # Extract Emails
        emails = set(a.text for a in soup.find_all("a") if "@" in a.text)
        
        # Extract Bitcoin Wallets
        btc_wallets = set(a.text for a in soup.find_all("a") if a.text.startswith("1") or a.text.startswith("3"))
        
        # Extract Links
        links = set(a["href"] for a in soup.find_all("a", href=True))

        # Save Data
        data = {
            "emails": list(emails),
            "btc_wallets": list(btc_wallets),
            "links": list(links),
        }

        with open("darkweb_results.json", "w") as f:
            json.dump(data, f, indent=4)

        self.log("\n Dark web data saved in darkweb_results.json")

# Run the spider
from scrapy.crawler import CrawlerProcess

process = CrawlerProcess()
process.crawl(DarkWebSpider)
process.start()
