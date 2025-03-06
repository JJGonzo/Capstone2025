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
        res = requests.get(url, proxies=proxies, timeout=15)
        res.raise_for_status()
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text()

        emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', text)
        bitcoin = re.findall(r'\b[13][a-km-zA-HJ-NP-Z1-9]{25,34}\b', text)
        monero = re.findall(r'4[0-9AB][1-9A-HJ-NP-Za-km-z]{93}', text)
        usernames = re.findall(r'@[A-Za-z0-9_]{3,}', text)
        ips = re.findall(r'(?:\d{1,3}\.){3}\d{1,3}', text)

        # Check if there's any relevant OSINT data
        if emails or bitcoin or monero or usernames or ips:
            return {
                'url': url,
                'emails': set(emails),
                'bitcoin_addresses': set(bitcoin),
                'monero_addresses': set(monero),
                'usernames': set(usernames),
                'ips': set(ips)
            }
        else:
            return None

    except requests.exceptions.RequestException:
        print(f"[SKIPPED - Unreachable] {url}")
        return None
    except Exception as e:
        print(f"[SKIPPED - Error] {url}: {e}")
        return None

if __name__ == '__main__':
    onion_urls = fetch_hidden_wiki_links()
    print(f"Found {len(onion_urls)} onion links from Hidden Wiki.")

    useful_results = []

    for idx, url in enumerate(onion_urls, 1):
        print(f"\n[{idx}/{len(onion_urls)}] Scraping {url}")
        result = scrape_site(url)

        if result:
            print("✅ OSINT data found:")
            if result['emails']: print(f"  Emails: {result['emails']}")
            if result['bitcoin_addresses']: print(f"  Bitcoin: {result['bitcoin_addresses']}")
            if result['monero_addresses']: print(f"  Monero: {result['monero_addresses']}")
            if result['usernames']: print(f"  Usernames: {result['usernames']}")
            if result['ips']: print(f"  IPs: {result['ips']}")

            useful_results.append(result)
        else:
            print("❌ No useful OSINT data found or site unreachable.")

    print("\n--- Summary ---")
    print(f"Total sites scraped: {len(onion_urls)}")
    print(f"Sites with OSINT data: {len(useful_results)}")
