import scrapy
import json
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

# ✅ Corrected Proxy Configuration (Using Privoxy instead of socks5h)
TOR_PROXY = "http://127.0.0.1:8118"  # Privoxy acts as a bridge for Tor

# ✅ List of Safe .onion Sites for Testing (Updated with new links)
target_domains = [
    "http://blinkxxvyrdjgxao4lf6wgxqpbdd4xkawbe2acs7sqlfxnb5ei2xid.onion",  # Example .onion link
]

class DarkWebSpider(scrapy.Spider):
    name = "darkweb_scraper"

    # Set the headers to mimic a real browser request
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'RETRY_ENABLED': True,
        'RETRY_TIMES': 5,  # Retry up to 5 times
        'RETRY_HTTP_CODES': [503],  # Retry on 503 errors
        'DOWNLOAD_DELAY': 1,  # Add a delay to avoid being rate-limited
    }

    def start_requests(self):
        for url in target_domains:
            yield scrapy.Request(
                f"http://{url}",  # Ensure the correct format for the .onion link
                callback=self.parse,
                meta={"proxy": TOR_PROXY}  # Correct proxy usage
            )

    def parse(self, response):
        # Check for errors (e.g., 503)
        if response.status == 503:
            self.logger.warning(f"503 error on {response.url}. Retrying...")
            yield scrapy.Request(
                response.url, 
                callback=self.parse, 
                meta={"proxy": TOR_PROXY}, 
                dont_filter=True  # Don't filter this request
            )
            return

        soup = BeautifulSoup(response.text, "html.parser")

        # ✅ Extract Emails
        emails = set(a.text for a in soup.find_all("a") if "@" in a.text)

        # ✅ Extract Bitcoin Wallets
        btc_wallets = set(a.text for a in soup.find_all("a") if a.text.startswith("1") or a.text.startswith("3"))

        # ✅ Extract Links
        links = set(a["href"] for a in soup.find_all("a", href=True))

        # ✅ Save Data
        data = {
            "emails": list(emails),
            "btc_wallets": list(btc_wallets),
            "links": list(links),
        }

        with open("darkweb_results.json", "w") as f:
            json.dump(data, f, indent=4)

        self.log("\n✅ Dark web data saved in darkweb_results.json")

# ✅ Run the Scrapy Spider
process = CrawlerProcess()
process.crawl(DarkWebSpider)
process.start()
