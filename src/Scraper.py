import requests
from bs4 import BeautifulSoup
import re

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'}

# Simple function to scrape OnionEngine.com for onion URLs
def fetch_onion_links(query, pages=1):
    onion_links = set()

    for page in range(1, pages + 1):
        url = f'https://onionengine.com/search.php?search={query}&submit=Search&page={page}'
        res = requests.get(url, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')

        # Extract all links explicitly ending with .onion
        links = soup.find_all('a', href=True)
        for link in links:
            href = link['href']
            if '.onion' in href and not 'onionengine.com' in href:
                # Ensure full onion link is properly formatted
                onion_match = re.search(r'(https?://[a-z2-7]{56}\.onion)', href)
                if onion_match:
                    onion_links.add(onion_match.group(1))

    return list(onion_links)

# Scrape individual onion site via Tor proxy
def scrape_site(url):
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    try:
        res = requests.get(url, proxies=proxies, timeout=20, headers=headers)
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text()

        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        bitcoin = re.findall(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b', text)
        monero = re.findall(r'4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}', text)
        usernames = re.findall(r'@[A-Za-z0-9_]{3,}', text)

        return {
            'url': url,
            'emails': set(emails),
            'bitcoin_addresses': set(bitcoin),
            'monero_addresses': set(monero),
            'usernames': set(usernames)
        }

    except Exception as e:
        print(f'Error scraping {url}: {e}')
        return None

if __name__ == '__main__':
    query = input("Enter your search query: ")
    onion_urls = fetch_onion_links(query, pages=1)

    print(f'Found {len(onion_urls)} onion links.')

    for url in onion_urls:
        print(f'\nScraping {url}')
        result = scrape_site(url)
        if result:
            print(f"Emails: {result['emails']}")
            print(f"Bitcoin Addresses: {result['bitcoin_addresses']}")
            print(f"Monero Addresses: {result['monero_addresses']}")
            print(f"Usernames: {result['usernames']}")
