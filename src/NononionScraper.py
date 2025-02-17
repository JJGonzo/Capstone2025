import requests
from bs4 import BeautifulSoup

# Define the target URL
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

# Parse the HTML content
soup = BeautifulSoup(response.text, "html.parser")

# Extract article titles and links using the new class "titleline"
articles = []
for item in soup.find_all("span", class_="titleline"):
    title_tag = item.find("a")
    if title_tag:
        title = title_tag.text.strip()
        link = title_tag.get("href", "No link available")
        articles.append({"title": title, "link": link})

# Display results
if articles:
    for article in articles[:10]:  # Limit to first 10 results
        print(f"{article['title']} - {article['link']}")
    print("\nScraper tested successfully on a normal website!")
else:
    print("No articles found. The website structure might have changed.")
