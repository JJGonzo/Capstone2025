import requests
from bs4 import BeautifulSoup
import json

# Configure Tor proxy
proxies = {
    "http": "socks5h://127.0.0.1:9050",
    "https": "socks5h://127.0.0.1:9050"
}

# Dark web target URL
url = "http://somedarkwebforum.onion"

# Request page through Tor
response = requests.get(url, proxies=proxies)
soup = BeautifulSoup(response.text, "html.parser")

# Extract usernames & posts
data = []
for post in soup.find_all("div", class_="post"):
    username = post.find("span", class_="username").text
    content = post.find("p").text
    data.append({"username": username, "post": content})

# Save extracted data
with open("../data/extracted_data.json", "w") as json_file:
    json.dump(data, json_file, indent=4)

print("Scraping complete! Data saved to extracted_data.json")
