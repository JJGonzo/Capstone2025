import os

print("Running OSINT Investigation System...")

# Run scraper
os.system("python3 scripts/scraper.py")

# Store extracted data
os.system("python3 scripts/store_data.py")

# Search function
search_keyword = input("Enter keyword to search: ")
os.system(f"python3 scripts/search_data.py {search_keyword}")

# Generate final report
os.system("python3 scripts/generate_report.py")

print("OSINT Process Complete! Report generated in reports/OSINT_Report.pdf")
