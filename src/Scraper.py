import requests
from bs4 import BeautifulSoup
import scrapy
from scrapy.crawler import CrawlerProcess
import json
import os

# Configure the Tor Proxy (make sure Tor is running on port 9050)
TOR_PROXY = "socks5h://127.0.0.1:9050"

# Target domains to scan - replace with your .onion domains
target_domains = [
    "dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxxnyazubrad.onion",  # Example .onion link
    "nzdmnfcf22s5pd3wvyfy3jhwoubv6qunmdglspqhurqunvr52khattdad.onion"  # Another example
]

# Scrapy spider to scrape data from the .onion sites
class OnionSpider(scrapy.Spider):
    name = 'onion_spider'
    
    # Setting start URLs for the spider
    start_urls = [f"http://{domain}" for domain in target_domains]
    
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
        },
        'HTTP_PROXY': TOR_PROXY,  # Setting the Tor proxy for the spider
    }

    def parse(self, response):
        # Check for status code
        if response.status != 200:
            self.logger.error(f"Error fetching {response.url}: {response.status}")
            return
        
        # Scrape data using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Example: Extracting emails from .onion page (you can customize this)
        emails = set(a.text for a in soup.find_all('a') if "@" in a.text)
        btc_wallets = set(a.text for a in soup.find_all('a') if a.text.startswith('1') or a.text.startswith('3'))
        
        # Collect links
        links = set(a['href'] for a in soup.find_all('a', href=True))
        
        # Save or process the data
        data = {
            "emails": list(emails),
            "btc_wallets": list(btc_wallets),
            "links": list(links),
        }
        
        output_file = f"{response.url.replace('http://', '').replace('.onion', '').replace('.', '_')}.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        self.log(f"Data for {response.url} saved in {output_file}")

# Run the Scrapy spider
def run_spider():
    process = CrawlerProcess()
    process.crawl(OnionSpider)
    process.start()

# BeautifulSoup & requests example for manual scraping:
def scrape_with_requests():
    for domain in target_domains:
        url = f"http://{domain}"
        
        try:
            # Request to the .onion URL through the Tor proxy
            response = requests.get(url, proxies={"http": TOR_PROXY, "https": TOR_PROXY})
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                emails = set(a.text for a in soup.find_all('a') if "@" in a.text)
                btc_wallets = set(a.text for a in soup.find_all('a') if a.text.startswith('1') or a.text.startswith('3'))
                
                data = {
                    "emails": list(emails),
                    "btc_wallets": list(btc_wallets),
                    "links": [a['href'] for a in soup.find_all('a', href=True)]
                }
                
                # Saving the data to a JSON file
                output_file = f"{domain.replace('.', '_')}.json"
                with open(output_file, "w") as f:
                    json.dump(data, f, indent=4)
                print(f"Data for {domain} saved in {output_file}")
                
            else:
                print(f"Failed to retrieve {url}, status code: {response.status_code}")
        
        except requests.exceptions.RequestException as e:
            print(f"Error fetching {url}: {e}")

if __name__ == "__main__":
    # Run the Scrapy spider to scrape .onion sites
    run_spider()
    
    # You can also run the manual scraping using requests and BeautifulSoup:
    # scrape_with_requests()
