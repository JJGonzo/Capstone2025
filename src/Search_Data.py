# OSINT Data Storage Tool - Quick Guide
# -----------------------------------
#
# SETUP:
# 1. Make sure you're in the src directory
# 2. Run test_setup.py first:    python3 test_setup.py
# 3. Then run this file:         python3 Store_Data.py
# 4. Finally run Search_Data.py: python3 Search_Data.py
#
# CREATING/EDITING THIS FILE:
# 1. In terminal type:           nano Store_Data.py
# 2. Delete everything in nano:  Press Ctrl + K repeatedly until file is empty
# 3. Copy this entire file:     Select all this code including comments
# 4. Paste into nano:           Right-click or Cmd+V (Mac) or Ctrl+V (Windows)
# 5. Save and exit:             Press Ctrl + X, then Y, then Enter
#
# HOW IT WORKS:
# - Creates SQLite database in data directory
# - Reads from final_results.json
# - Stores data in database for searching
# - Shows confirmation when complete
#
# TROUBLESHOOTING:
# - If "file not found": Make sure final_results.json exists
# - If no data appears: Run test_setup.py first
# - If you get errors: Make sure you're in the src directory
#
# Directory structure should be:
# your_project/
# ├── src/
# │   ├── Store_Data.py
# │   ├── Search_Data.py
# │   └── test_setup.py
# └── data/
#     └── osint_data.db

import sqlite3
import json
import os

# Get database path
current_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(current_dir, "data")
db_path = os.path.join(data_dir, "osint_data.db")

# Create data directory if it doesn't exist
if not os.path.exists(data_dir):
    os.makedirs(data_dir)

# Connect to database
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Create table with updated schema
cursor.execute('''
CREATE TABLE IF NOT EXISTS ThreatData (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT,
    email TEXT,
    username TEXT,
    bitcoin_address TEXT,
    monero_address TEXT,
    ip_address TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Load data from scraper.py output
try:
    with open("final_results.json", "r") as f:
        nonion_data = json.load(f)
        
    # Insert data from nonion scraper
    for domain, info in nonion_data.items():
        emails = info.get("emails", [])
        usernames = info.get("usernames", [])
        ips = info.get("ips", [])
        
        for email in emails:
            cursor.execute("""
                INSERT INTO ThreatData (url, email)
                VALUES (?, ?)
            """, (domain, email))
            
        for username in usernames:
            cursor.execute("""
                INSERT INTO ThreatData (url, username)
                VALUES (?, ?)
            """, (domain, username))
            
        for ip in ips:
            cursor.execute("""
                INSERT INTO ThreatData (url, ip_address)
                VALUES (?, ?)
            """, (domain, ip))

except Exception as e:
    print(f"Error processing scraper data: {e}")

# Commit and close
conn.commit()
conn.close()

print("Data successfully stored in osint_data.db")
