import json
import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import random

# Configure the Tor Proxy (make sure Tor is running on port 9050)
TOR_PROXY = "socks5h://127.0.0.1:9050"

# Target domains to scan - replace with your .onion domains
target_domains = [
    "dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxxnyazubrad.onion",
    "uicrmrli3ir66c4fx4l5gv5hdb6jrzy72bitrk25w5dhv5o6sxmajxqd.onion",
    "lgh3eosuqrrtwx3s4nurjcqrm53ba5vqsbim5k5ntdp033qk17buyd.onion",
    "keybase5wmilwokqirssclfnsqrjds17jdir5wy7y71u3tanwmtp60id.onion"
]

# Updated Scrapy settings section
custom_settings = {
    'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'DOWNLOADER_MIDDLEWARES': {
        'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 1,
        'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
        'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    },
    'HTTP_PROXY': TOR_PROXY,
}

class OnionSpider(scrapy.Spider):
    name = 'onion_spider'
    start_urls = [f"http://{domain}" for domain in target_domains]
    custom_settings = custom_settings

    def parse(self, response):
        if response.status != 200:
            self.logger.error(f"Error fetching {response.url}: {response.status}")
            return
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        emails = set(a.text for a in soup.find_all('a') if "@" in a.text)
        btc_wallets = set(a.text for a in soup.find_all('a') if a.text.startswith('1') or a.text.startswith('3'))
        links = set(a['href'] for a in soup.find_all('a', href=True))
        
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
class RandomUserAgentMiddleware:
    def __init__(self, user_agent=''):
        self.user_agent_list = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0',
            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
        ]
        self.user_agent = random.choice(self.user_agent_list)
    
    def process_request(self, request, spider):
        request.headers['User-Agent'] = self.user_agent

# Run the Scrapy spider
def run_spider():
    process = CrawlerProcess()
    process.crawl(OnionSpider)
    process.start()

if __name__ == "__main__":
    run_spider()
