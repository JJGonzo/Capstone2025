import sqlite3
import json

# Connect to database (Ensure the directory exists)
conn = sqlite3.connect("osint_data.db")
cursor = conn.cursor()

# Create table with updated schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS ThreatData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT,
    username TEXT
)
''')

# Load data from the JSON output of your scraper
json_file = "final_results.json"

try:
    with open(json_file, "r") as f:
        data = json.load(f)
except json.JSONDecodeError as e:
    print(f"Error parsing JSON: {e}")
    exit()

# Insert extracted emails and usernames into the database
for domain, info in data.items():
    emails = info.get("emails", [])
    usernames = info.get("usernames", [])

    for email in emails:
        cursor.execute("INSERT INTO ThreatData (email, username) VALUES (?, ?)", (email, None))

    for username in usernames:
        cursor.execute("INSERT INTO ThreatData (email, username) VALUES (?, ?)", (None, username))

# Commit and close
conn.commit()
conn.close()

print("Data successfully stored in osint_data.db")
