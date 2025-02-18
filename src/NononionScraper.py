import subprocess
import json

# List of target domains to scan
target_domains = [
    "uwsp.edu",
    "news.ycombinator.com",
    "bbc.com",
    "theverge.com"
]

# Function to run theHarvester and capture JSON output
def run_theHarvester(domain):
    print(f"\n Running theHarvester for: {domain}")
    command = f"theHarvester -d {domain} -b all -j"
    
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return json.loads(result.stdout)  # Parse JSON output from theHarvester
    except Exception as e:
        print(f"Error running theHarvester for {domain}: {e}")
        return {}

# Main function
if __name__ == "__main__":
    all_results = {}

    for domain in target_domains:
        harvester_data = run_theHarvester(domain)  # Run theHarvester
        
        if "emails" in harvester_data and "users" in harvester_data:
            emails = [email["email"] for email in harvester_data["emails"]]
            usernames = harvester_data["users"]
        else:
            emails, usernames = [], []

        all_results[domain] = {
            "emails": emails,
            "usernames": usernames
        }

    # Save extracted data to a JSON file
    with open("final_results.json", "w") as f:
        json.dump(all_results, f, indent=4)

    print("\n All data saved in final_results.json")
