import requests
from bs4 import BeautifulSoup
import re

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64)'}

def fetch_hidden_wiki_links():
    url = "http://wiki47qqn6tey4id7xeqb6l7uj6jueacxlqtk3adshox3zdohvo35vad.onion/"
    
    try:
        response = requests.get(url, proxies=proxies, headers=headers, timeout=30)
        soup = BeautifulSoup(response.text, 'html.parser')

        onion_links = set()

        # Find all links with .onion domain explicitly
        for link in soup.find_all('a', href=True):
            href = link['href']
            if re.match(r'http[s]?://[a-z2-7]{56}\.onion', href):
                onion_links.add(href)

        return list(onion_links)

    except Exception as e:
        print(f"Error accessing Hidden Wiki: {e}")
        return []

def scrape_site(url):
    try:
        res = requests.get(url, proxies=proxies, timeout=20)
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text()

        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        bitcoin = re.findall(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b', text)
        monero = re.findall(r'4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}', text)
        usernames = re.findall(r'@[A-Za-z0-9_]{3,}', text)
        ips = re.findall(r'(?:\d{1,3}\.){3}\d{1,3}', text)

        return {
            'url': url,
            'emails': set(emails),
            'bitcoin_addresses': set(bitcoin),
            'monero_addresses': set(monero),
            'usernames': set(usernames),
            'ips': set(re.findall(r'[0-9]+(?:\.[0-9]+){3}', text))
        }

    except Exception as e:
        print(f'Error scraping {url}: {e}')
        return None

if __name__ == '__main__':
    onion_urls = fetch_hidden_wiki_links()
    print(f"Found {len(onion_urls)} onion links from Hidden Wiki.")

    for url in onion_urls:
        print(f'\nScraping {url}')
        result = scrape_site(url)
        if result:
            print(f"Emails: {result['emails']}")
            print(f"Bitcoin Addresses: {result['bitcoin_addresses']}")
            print(f"Monero Addresses: {result['monero_addresses']}")
            print(f"Usernames: {result['usernames']}")
            print(f"IP Addresses: {result['ips']}")
