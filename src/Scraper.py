import json
import requests
from bs4 import BeautifulSoup

# Use the correct SOCKS5H proxy
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050',
}

# Target .onion domains
target_domains = [
    "lgh3eosuqrrtwx3s4nurujcqrm53ba5vqsbim5k5ntdp033qkl7buyd.onion"
]

# Function to scrape .onion sites
def scrape_onion_site(url):
    try:
        print(f"Scraping: {url}")
        
        # Ensure the full URL has http:// (not https://)
        full_url = f"http://{url}" if not url.startswith("http") else url
        
        response = requests.get(full_url, proxies=proxies, timeout=60)

        if response.status_code != 200:
            print(f"Error fetching {url}: {response.status_code}")
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
        
        output_file = f"{url.replace('.onion', '').replace('.', '_')}.json"
        with open(output_file, 'w') as f:
            json.dump(data, f, indent=4)
        
        print(f"Data for {url} saved in {output_file}")
    
    except requests.exceptions.RequestException as e:
        print(f"Error scraping {url}: {e}")

# Run the scraper
if __name__ == "__main__":
    for domain in target_domains:
        scrape_onion_site(domain)
