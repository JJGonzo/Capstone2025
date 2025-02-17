import requests
from bs4 import BeautifulSoup

# Define target website
url = "https://news.ycombinator.com/"

# Simulate a real browser with headers
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

# Fetch the webpage with error handling
try:
    response = requests.get(url, headers=headers, timeout=10)
    response.raise_for_status()
except requests.exceptions.RequestException as e:
    print(f"Error fetching data: {e}")
    exit()

# Parse HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Extract article titles and links
articles = []
for item in soup.find_all("a", class_="storylink"):
    title = item.text.strip()
    link = item.get("href", "No link available")  # Handle missing links
    articles.append({"title": title, "link": link})

# Display results
if articles:
    for article in articles[:10]:  # Limit to first 10 results
        print(f"{article['title']} - {article['link']}")
    print("\nScraper tested successfully on a normal website!")
else:
    print("No articles found. The website structure might have changed.")
