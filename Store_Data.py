import sqlite3
import json

# Connect to database
conn = sqlite3.connect("../data/osint_data.db")
cursor = conn.cursor()

# Create table
cursor.execute('''
CREATE TABLE IF NOT EXISTS ThreatData (
    id INTEGER PRIMARY KEY,
    username TEXT,
    forum_post TEXT
)
''')

# Load data from JSON
with open("../data/extracted_data.json", "r") as json_file:
    data = json.load(json_file)

# Insert into database
for entry in data:
    cursor.execute("INSERT INTO ThreatData (username, forum_post) VALUES (?, ?)",
                   (entry["username"], entry["post"]))

conn.commit()
conn.close()

print("Data stored in osint_data.db")
