__version__ = 3

import sys
import requests
from bs4 import BeautifulSoup
import argparse
import random
import re
import json
import os

class Configuration:
    DARKDUMP_REQUESTS_SUCCESS_CODE = 200
    DARKDUMP_TOR_RUNNING = False 
    __socks5init__ = "socks5h://localhost:9050"
    __darkdump_api__ = "https://ahmia.fi/search/?q="

class Darkdump:
    def extract_links(self, soup):
        return [a['href'] for a in soup.find_all('a', href=True)]

    def extract_metadata(self, soup):
        meta_data = {}
        for meta in soup.find_all('meta'):
            meta_name = meta.get('name') or meta.get('property')
            if meta_name:
                meta_data[meta_name] = meta.get('content')
        return meta_data

    def crawl(self, query, amount, use_proxy=False):
        headers = {'User-Agent': 'Mozilla/5.0'}
        proxy_config = {'http': 'socks5h://localhost:9050', 'https': 'socks5h://localhost:9050'} if use_proxy else {}
        
        try:
            page = requests.get(Configuration.__darkdump_api__ + query, headers=headers, proxies=proxy_config)
            soup = BeautifulSoup(page.content, 'html.parser')
            results = soup.find_all('a')
            onion_links = list(set([link.get('href') for link in results if link.get('href') and ".onion" in link.get('href')]))
            
            print(f"Found {len(onion_links)} .onion links:")
            for idx, link in enumerate(onion_links[:amount], start=1):
                print(f"{idx}. {link}")
        except Exception as e:
            print(f"Error in fetching search results: {e}")


def darkdump_main():
    parser = argparse.ArgumentParser(description="Darkdump: A simple .onion search scraper.")
    parser.add_argument("-q", "--query", help="Search query for the deep web", type=str, required=True)
    parser.add_argument("-a", "--amount", help="Number of results to return", type=int, default=10)
    parser.add_argument("-p", "--proxy", help="Use Tor proxy", action="store_true")
    
    args = parser.parse_args()
    print(f"Searching for: {args.query}, retrieving {args.amount} results...")
    Darkdump().crawl(args.query, args.amount, use_proxy=args.proxy)

if __name__ == "__main__":
    darkdump_main()
