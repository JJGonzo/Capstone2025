import requests
from bs4 import BeautifulSoup
import re
import csv

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

def load_onion_links_manual():
    print("Enter .onion links (one per line). Type 'done' to finish:")
    onion_links = []
    while True:
        entry = input("> ").strip()
        if entry.lower() == 'done':
            break
        if entry.endswith(".onion"):
            onion_links.append(entry)
        else:
            print("Invalid .onion link. Make sure it ends in .onion.")
    return onion_links

def load_onion_links_from_file(filename):
    onion_links = []
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                for cell in row:
                    cell = cell.strip()
                    if cell.endswith(".onion"):
                        onion_links.append(cell)
        return onion_links
    except Exception as e:
        print(f"Error reading file: {e}")
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
    # === SELECT YOUR INPUT MODE ===
    
    # Option 1: Use Hidden Wiki to fetch links
    onion_urls = fetch_hidden_wiki_links()

    # Option 2: Manually enter links
    # onion_urls = load_onion_links_manual()

    # Option 3: Load from file (CSV or TXT with comma-separated or line-by-line .onion links)
    # onion_urls = load_onion_links_from_file("onions.csv")

    print(f"\nFound {len(onion_urls)} onion links to scrape.")

    useful_results = []

    for idx, url in enumerate(onion_urls, 1):
        print(f"\n[{idx}/{len(onion_urls)}] Scraping {url}")
        result = scrape_site(url)

        if result:
            print("OSINT data found:")
            if result['emails']: print(f"  Emails: {result['emails']}")
            if result['bitcoin_addresses']: print(f"  Bitcoin: {result['bitcoin_addresses']}")
            if result['monero_addresses']: print(f"  Monero: {result['monero_addresses']}")
            if result['usernames']: print(f"  Usernames: {result['usernames']}")
            if result['ips']: print(f"  IPs: {result['ips']}")

            useful_results.append(result)
        else:
            print("No useful OSINT data found or site unreachable.")

    print("\n--- Summary ---")
    print(f"Total sites scraped: {len(onion_urls)}")
    print(f"Sites with OSINT data: {len(useful_results)}")
