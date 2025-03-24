import requests
from bs4 import BeautifulSoup
import re
import csv
import argparse
import sys
import json
from datetime import datetime

# Show friendly startup guide
if len(sys.argv) == 1:
    print("""
🔍 Dark Web OSINT Scraper - Quick Start

--mode hiddenwiki
    → Automatically pulls links from the Hidden Wiki.

--mode manual
    → Prompts you to type/paste links directly.

--mode file --file onions.csv
    → Loads links from a CSV or text file you provide.

--limit 10
    → (Optional) Limit how many links to scrape.

Example Usage:
    python scraper.py --mode hiddenwiki --limit 10
    python scraper.py --mode manual
    python scraper.py --mode file --file onions.csv
""")

# Set up command-line arguments
parser = argparse.ArgumentParser(
    description="""
Dark Web OSINT Scraper

Modes:
  --mode hiddenwiki      → Automatically pulls links from the Hidden Wiki.
  --mode manual          → Prompts you to type/paste links directly.
  --mode file            → Loads links from a CSV or text file (use with --file).

Other Options:
  --file onions.csv      → Required with 'file' mode.
  --limit 10             → (Optional) Limit number of links to scrape.

Examples:
  python scraper.py --mode hiddenwiki
  python scraper.py --mode file --file onions.csv --limit 10
""",
    formatter_class=argparse.RawDescriptionHelpFormatter
)

parser.add_argument('--mode', choices=['hiddenwiki', 'manual', 'file'], required=True,
                    help="Scraping mode: hiddenwiki | manual | file")
parser.add_argument('--file', type=str, help="Path to CSV or text file with .onion links (required if mode is 'file')")
parser.add_argument('--limit', type=int, default=None, help="Max number of onion links to scrape")

args = parser.parse_args()

# Tor proxy settings
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

def log_error(message, log_file="errors.log"):
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(log_file, "a", encoding='utf-8') as f:
        f.write(f"[{timestamp}] {message}\n")

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
                'emails': list(set(emails)),
                'bitcoin_addresses': list(set(bitcoin)),
                'monero_addresses': list(set(monero)),
                'usernames': list(set(usernames)),
                'ips': list(set(ips))
            }
        else:
            return None

    except requests.exceptions.HTTPError as e:
        msg = f"[HTTPError] {url} - {e}"
    except requests.exceptions.ConnectionError as e:
        msg = f"[ConnectionError] {url} - {e}"
    except requests.exceptions.Timeout as e:
        msg = f"[Timeout] {url} - {e}"
    except requests.exceptions.RequestException as e:
        msg = f"[RequestException] {url} - {e}"
    except Exception as e:
        msg = f"[Unexpected Error] {url} - {e}"
    else:
        msg = None

    if msg:
        print(f"[SKIPPED] {msg}")
        log_error(msg)
    return None

def save_results_json(results, filename="results.json"):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=4)

def save_results_csv(results, filename="results.csv"):
    with open(filename, mode='w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['URL', 'Emails', 'Bitcoin', 'Monero', 'Usernames', 'IPs'])
        for r in results:
            writer.writerow([
                r['url'],
                ", ".join(r['emails']),
                ", ".join(r['bitcoin_addresses']),
                ", ".join(r['monero_addresses']),
                ", ".join(r['usernames']),
                ", ".join(r['ips'])
            ])

# Load onion links based on mode
if args.mode == 'hiddenwiki':
    onion_urls = fetch_hidden_wiki_links()
elif args.mode == 'manual':
    onion_urls = load_onion_links_manual()
elif args.mode == 'file':
    if not args.file:
        print("Error: --file argument is required when using file mode.")
        sys.exit(1)
    onion_urls = load_onion_links_from_file(args.file)
else:
    print("Invalid mode.")
    sys.exit(1)

total_found = len(onion_urls)
print(f"\nFound {total_found} onion links.")

if args.limit:
    onion_urls = onion_urls[:args.limit]
    print(f"Limiting scrape to first {args.limit} links.")

confirm = input(f"\nProceed with scraping {len(onion_urls)} links? (y/n): ").strip().lower()
if confirm != 'y':
    print("Aborting scrape.")
    sys.exit(0)

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

if useful_results:
    save_results_csv(useful_results)
    save_results_json(useful_results)
    print("OSINT data saved to results.csv and results.json")
else:
    print("No OSINT data collected, so no output files were saved.")
