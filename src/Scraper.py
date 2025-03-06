import requests
from bs4 import BeautifulSoup
import re
import json
import time
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry

class DarkScrape:
    '''Scrapes data from an onion site using Privoxy. Data scraped consists of:
        * emails
        * links
        * images
        * text
        * title
        * bitcoin addresses
        if available.
    '''
    def __init__(self):
        self.session = self.connect_via_privoxy()
        self.ip = self.get_ip()
        if self.ip:
            print("Connected to: ", self.ip)
        self.response = ""
        self.url = ""
        self.soup = BeautifulSoup("", "html.parser")

    def connect_via_privoxy(self):
        session = requests.Session()
        session.proxies = {
            'http': 'http://127.0.0.1:8118',
            'https': 'http://127.0.0.1:8118'
        }
        retry_strategy = Retry(
            total=5,
            backoff_factor=2,
            status_forcelist=[500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        return session

    def get_ip(self):
        try:
            response = self.session.get("http://check.torproject.org", timeout=10)
            return response.text if response.status_code == 200 else None
        except requests.exceptions.RequestException:
            return None

    def emails(self):
        return list(set(re.findall(r'[\w\.-]+@[\w\.-]+', self.response)))
        
    def links(self):
        links = [g.get('href') for g in self.soup.find_all('a')]
        onion_links = [l for l in links if l and ".onion" in l]
        return list(set(onion_links))
    
    def images(self):
        links = [g.get('src') for g in self.soup.find_all(lambda tag: tag.name in ["i", "img", "a"]) if g.get('src')]
        return list(set(links))
    
    def text(self):
        return self.soup.get_text(separator=' ', strip=True)

    def title(self):
        return self.soup.title.text if self.soup.title else ""

    def bitcoins(self):
        return list(set(re.findall(r'\b(?:bc1|[13])[a-zA-HJ-NP-Z0-9]{25,42}\b', self.response)))
    
    def scrape(self, url):
        if not url.startswith("http://") and not url.startswith("https://"):
            url = "http://" + url
        
        try:
            r = self.session.get(url, timeout=60)
            if r.status_code == 200:
                self.response = r.text
            else:
                print("Response: ", r.status_code)
                return self
        except requests.exceptions.RequestException as err:
            print("Error: ", err)
            return self
        
        self.url = url
        self.soup = BeautifulSoup(self.response, "html.parser")
        return self
    
    @property
    def result(self): 
        return {
            "url": self.url,
            "title": self.title(),
            "links": self.links(),
            "emails": self.emails(),
            "images": self.images(),
            "text": self.text(),
            "bitcoin": self.bitcoins()
        }

if __name__ == "__main__":
    target_domains = [
        "lgh3eosuqrrtwx3s4nurujcqrm53ba5vqsbim5k5ntdp033qkl7buyd.onion"
    ]
    
    scraper = DarkScrape()
    for domain in target_domains:
        scraper.scrape(domain)
        output_file = f"{domain.replace('.onion', '').replace('.', '_')}.json"
        with open(output_file, 'w') as f:
            json.dump(scraper.result, f, indent=4)
        print(f"Data for {domain} saved in {output_file}")
