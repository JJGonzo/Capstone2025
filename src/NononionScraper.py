import subprocess
import json

# List of target domains to scan (Add more as needed)
target_domains = [
    "uwsp.edu",
    "news.ycombinator.com",
    "bbc.com",
    "theverge.com"
]

# Function to run theHarvester for a single domain
def run_theHarvester(domain):
    print(f"\n Running theHarvester for: {domain}")
    command = f"theHarvester -d {domain} -b all -f {domain.replace('.', '_')}.json"
    subprocess.run(command, shell=True)

# Function to read results from theHarvester JSON output
def parse_results(json_file):
    try:
        with open(json_file, "r") as file:
            data = json.load(file)

        emails = data.get("emails", [])
        usernames = data.get("users", [])

        return emails, usernames
    except Exception as e:
        print(f" Error reading JSON {json_file}: {e}")
        return [], []

# Main function
if __name__ == "__main__":
    all_results = {}

    for domain in target_domains:
        run_theHarvester(domain)  # Run theHarvester on each domain
        
        # Parse results from each domain's output
        json_filename = f"{domain.replace('.', '_')}.json"
        emails, usernames = parse_results(json_filename)

        all_results[domain] = {
            "emails": emails,
            "usernames": usernames
        }

    # Save all extracted data to a single JSON file
    with open("final_results.json", "w") as f:
        json.dump(all_results, f, indent=4)

    print("\n All data saved in final_results.json")
