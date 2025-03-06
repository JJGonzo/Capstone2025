import subprocess
import json
import os
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
import scrapy
from scrapy.crawler import CrawlerProcess

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
    
    # Scrapy settings
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'DOWNLOADER_MIDDLEWARES': {
            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
            'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,  # Disable default user agent middleware
            'myproject.middlewares.RandomUserAgentMiddleware': 500,  # Enable our custom middleware
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


# Custom middleware for rotating user agents
class RandomUserAgentMiddleware(UserAgentMiddleware):
    def __init__(self, user_agent=''):
        # List of user agents for rotation
        self.user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            # Add more user agents here
        ]
        self.user_agent = random.choice(self.user_agent_list)

    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.user_agent


# Run the Scrapy spider
def run_spider():
    process = CrawlerProcess()
    process.crawl(OnionSpider)
    process.start()


# Run the spider
if __name__ == "__main__":
    # Run the Scrapy spider to scrape .onion sites
    run_spider()
