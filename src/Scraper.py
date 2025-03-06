import sys
import requests
import argparse
import random
import re
import json
import os
import time
from bs4 import BeautifulSoup

# Configuration
class Configuration:
    __darkdump_api__ = "https://ahmia.fi/search/?q="
    __socks5init__ = "socks5h://localhost:9050"

def fetch_search_results(query, use_proxy):
    headers = {'User-Agent': 'Mozilla/5.0'}
    proxy_config = {'http': Configuration.__socks5init__, 'https': Configuration.__socks5init__} if use_proxy else {}
    
    try:
        response = requests.get(Configuration.__darkdump_api__ + query, headers=headers, proxies=proxy_config)
        soup = BeautifulSoup(response.content, 'html.parser')
        return soup.find_all('a')
    except Exception as e:
        print(f"Error fetching Ahmia.fi results: {e}")
        return []

def extract_onion_links(results):
    onion_links = []
    for link in results:
        href = link.get('href')
        if href and '.onion' in href:
            onion_links.append(href)
    return list(set(onion_links))

def scrape_site(url, use_proxy, scrape_images):
    headers = {'User-Agent': 'Mozilla/5.0'}
    proxy_config = {'http': Configuration.__socks5init__, 'https': Configuration.__socks5init__} if use_proxy else {}
    
    try:
        response = requests.get(url, headers=headers, proxies=proxy_config)
        soup = BeautifulSoup(response.content, 'html.parser')
        text_content = soup.get_text()
        image_urls = [img['src'] for img in soup.find_all('img') if img.get('src')] if scrape_images else []
        return text_content, image_urls
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None, []

def main():
    parser = argparse.ArgumentParser(description="Darkdump: A simple dark web search and scraper.")
    parser.add_argument("-q", "--query", help="The search query for Ahmia.fi", required=True)
    parser.add_argument("-p", "--proxy", help="Use Tor proxy for scraping", action="store_true")
    parser.add_argument("-i", "--images", help="Scrape images and visual content from the site", action="store_true")
    parser.add_argument("-s", "--scrape", help="Scrape the actual site for content and look for keywords", action="store_true")
    args = parser.parse_args()
    
    print(f"Searching Ahmia.fi for: {args.query}")
    results = fetch_search_results(args.query, args.proxy)
    onion_links = extract_onion_links(results)
    
    if not onion_links:
        print("No .onion links found.")
        return
    
    print("Found .onion links:")
    for link in onion_links:
        print(link)
    
    if args.scrape:
        for link in onion_links:
            print(f"Scraping {link}...")
            text, images = scrape_site(link, args.proxy, args.images)
            if text:
                print(f"Extracted text: {text[:500]}...")  # Show only the first 500 characters
            if args.images and images:
                print(f"Found images: {images}")

if __name__ == "__main__":
    main()
