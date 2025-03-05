import scrapy
import json
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

# ✅ Corrected Proxy Configuration (Using Privoxy instead of socks5h)
TOR_PROXY = "http://127.0.0.1:8118"  # Privoxy acts as a bridge for Tor

# ✅ List of Safe .onion Sites for Testing (Updated with new links)
target_domains = [
    "serhack5jaime7y6yeaead6gpxxignnivws4pqm3n5sume66g7l5id.onion",  # From SerHack blog
    "hellho5o35syxlrpfu45p57n42lzvirnvszmziunv7bcejynaqxyd.onion",  # From Telegram OSINT & Group Hacking Methods
    "hellho5o35syxlrpfu45p57n42lzvirnvszmziunv7bcejynaqxyd.onion",  # Repeated link
    "h36vwgmlvhyxlj7tjinbagig5c4gsjuvfatm27hg7q3thxpxs2od6ad.onion"  # From Instagram OSINT Tool & Source Code
]

class DarkWebSpider(scrapy.Spider):
    name = "darkweb_scraper"

    def start_requests(self):
        for url in target_domains:
            yield scrapy.Request(
                f"http://{url}",  # Ensure the correct format for the .onion link
                callback=self.parse,
                meta={"proxy": TOR_PROXY}  # ✅ Correct proxy usage
            )

    def parse(self, response):
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
