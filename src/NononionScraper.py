import requests
from bs4 import BeautifulSoup

# Regular website for testing
url = "https://news.ycombinator.com/"

# Make a request (NO NEED FOR TOR)
response = requests.get(url)

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Extract article titles
articles = []
for item in soup.find_all("a", class_="storylink"):
    title = item.text
    link = item["href"]
    articles.append({"title": title, "link": link})

# Print results
for article in articles:
    print(f"{article['title']} - {article['link']}")

print("Scraper tested successfully on a normal website!")
