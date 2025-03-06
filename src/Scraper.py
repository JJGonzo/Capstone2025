import re
import requests
from fake_useragent import UserAgent

# Setup for proxy and headers
proxies = {
    'http': 'socks5h://127.0.0.1:9050',
    'https': 'socks5h://127.0.0.1:9050'
}

headers = {'User-Agent': UserAgent().random}

# Function to scrape onion links from a given URL
def find_onion_links(url):
    try:
        # Request to the given URL
        response = requests.get(url, headers=headers, proxies=proxies)
        response.raise_for_status()  # Check if the request was successful

        # Regular expression to find .onion links in the HTML content
        text_content = response.text
        pattern = r"\b\w+\.onion\b"  # Regex pattern to find .onion links
        matches = re.findall(pattern, text_content)

        # Save the extracted onion links to a file
        with open('result.txt', 'w') as file:
            for match in matches:
                file.write(match + '\n')

        print(f"Found {len(matches)} .onion links and saved them to 'result.txt'.")
    
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")


# Function to check if a given onion link is valid
def is_onion_site_valid(url):
    try:
        response = requests.get(url, headers=headers, proxies=proxies)
        # Checking if the site is up and returns status code 200
        if response.status_code == 200:
            print(f"{url} is valid!")
            return True
        else:
            print(f"{url} returned status code {response.status_code}. Not valid.")
            return False
    except requests.exceptions.RequestException as e:
        print(f"Error checking {url}: {e}")
        return False


# Example usage:
# Scraping .onion links from the provided websites
find_onion_links("http://blinkxxvyrdjgxao4lf6wgxqpbdd4xkawbe2acs7sqlfxnb5ei2xid.onion")

# Checking if the provided onion links are valid
is_onion_site_valid("http://blinkxxvyrdjgxao4lf6wgxqpbdd4xkawbe2acs7sqlfxnb5ei2xid.onion")

