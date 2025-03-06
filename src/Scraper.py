from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from bs4 import BeautifulSoup
import re
import time

def tor_driver():
    options = Options()
    options.headless = True
    options.set_preference('network.proxy.type', 1)
    options.set_preference('network.proxy.socks', '127.0.0.1')
    options.set_preference('network.proxy.socks_port', 9050)
    options.set_preference("network.proxy.socks_remote_dns", True)
    options.set_preference("browser.privatebrowsing.autostart", True)
    options.set_preference("profile", "")  # Forces Selenium to use a clean temporary profile

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def fetch_onion_links(query, pages=1):
    driver = tor_driver()
    onion_links = set()

    onionsearch_url = 'https://onionsearch.io/'  # OnionSearch public frontend URL (clearnet)

    driver.get(onionsearch_url)
    time.sleep(5)

    search_box = driver.find_element(By.NAME, 'search')
    search_box.send_keys(query + Keys.RETURN)
    time.sleep(5)

    for page in range(pages):
        soup = BeautifulSoup(driver.page_source, 'html.parser')

        for link in soup.find_all('a', href=True):
            href = link['href']
            if re.match(r'http[s]?://[a-z2-7]{56}\.onion', href):
                onion_links.add(href)

        try:
            next_button = driver.find_element(By.LINK_TEXT, 'Next')
            next_button.click()
            time.sleep(5)
        except:
            break

    driver.quit()
    return list(onion_links)

import requests
from bs4 import BeautifulSoup

proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

def scrape_site(url):
    try:
        res = requests.get(url, proxies=proxies, timeout=15)
        soup = BeautifulSoup(res.text, 'html.parser')
        text = soup.get_text()

        # Basic OSINT Patterns
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
