# 🕵️‍♂️ Dark Web OSINT Scraper

A Python-based tool that scrapes `.onion` websites on the Tor network for open source intelligence (OSINT) indicators such as email addresses, cryptocurrency wallets, usernames, and IP addresses.

---


## 🚀 Features

- 🔍 Extracts:
  - Email addresses
  - Bitcoin & Monero wallet addresses
  - Usernames (e.g. @example)
  - IP addresses
- 🌐 Supports multiple scraping methods:
  - Hidden Wiki link discovery
  - Manual input
  - File-based list loading (CSV or TXT)
- ⚙️ Configurable scraping limit
- 📁 Saves results to `.json` and `.csv` files
- 📄 Logs errors to timestamped `errors.log`
- 🔐 Routes all traffic through Tor (`socks5h://127.0.0.1:9050`)
- 💬 Built-in search tool for querying scraped data (`search_results.py`)
- 🧪 Graceful error handling


## 📦 Requirements

- Python 3.6+
- Tor service running locally (via Tor Browser or `tor` daemon)
- Install dependencies using: pip install -r requirements.txt

## ⚙️ Usage
### Scrape from the Hidden Wiki (first 10 results)

```bash
python scraper.py --mode hiddenwiki --limit 10
```

### Scrape from manual input

```bash
python scraper.py --mode manual
```

### Scrape from a list in CSV or TXT file

```bash
python scraper.py --mode file --file onions.csv
```


## 📁 Output
results.json file will be created that you can open in your web browser for a clean list of OSINT Data

```bash
python3 results.csv
```


## 🔍 Searching Your Results
Use search_results.py to search through collected OSINT data.

```bash
python search_results.py
```

Select field: Email, BTC, Monero, Username, IP

View all unique values

Filter by search term

