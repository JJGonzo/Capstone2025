import re
import requests
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager

def tor_driver():
    options = Options()
    options.headless = True
    options.set_preference('network.proxy.type', 1)
    options.set_preference('network.proxy.socks', '127.0.0.1')
    options.set_preference('network.proxy.socks_port', 9050)  # CONFIRMED CORRECT
    options.set_preference("network.proxy.socks_remote_dns", True)
    options.set_preference("browser.privatebrowsing.autostart", True)

    service = Service(GeckoDriverManager().install())
    driver = webdriver.Firefox(service=service, options=options)
    return driver

def fetch_onion_links(query, pages=1):
    driver = tor_driver()
    onion_links = set()
    driver.set_page_load_timeout(30)

    onionsearch_url = 'https://onionengine.com/'

    try:
        driver.get(onionsearch_url)
        driver.implicitly_wait(10)

        search_box = driver.find_element(By.NAME, 'search')
        search_box.send_keys(query + Keys.RETURN)
        time.sleep(3)

        for page in range(pages):
            soup = BeautifulSoup(driver.page_source, 'html.parser')

            for link in soup.find_all('a', href=True):
                href = link['href']
                if re.match(r'http[s]?://[a-z2-7]{56}\.onion', href):
                    onion_links.add(href)

            try:
                next_button = driver.find_element(By.LINK_TEXT, 'Next')
                next_button.click()
                time.sleep(3)
            except Exception as e:
                print(f"No more pages or pagination issue: {e}")
                break

    except Exception as main_e:
        print(f"Error fetching onion links: {main_e}")

    finally:
        driver.quit()

    return list(onion_links)

def scrape_site(url):
    proxies = {
        'http': 'socks5h://127.0.0.1:9050',
        'https': 'socks5h://127.0.0.1:9050'
    }

    try:
        res = requests.get(url, proxies=proxies, timeout=20)
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
