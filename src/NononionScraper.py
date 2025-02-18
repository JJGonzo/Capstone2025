import subprocess
import json

# List of target domains to scan
target_domains = [
    "uwsp.edu",
]

# Function to run theHarvester and capture JSON output
def run_theHarvester(domain):
    print(f"\nRunning theHarvester for: {domain}")
    command = f"theHarvester -d {domain} -b bing -f {domain.replace('.', '_')}.json"

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Check if theHarvester ran successfully
        if result.returncode != 0:
            print(f"Error running theHarvester for {domain}: {result.stderr}")
            return {}

        # Read JSON output from the saved file
        json_filename = f"{domain.replace('.', '_')}.json"
        with open(json_filename, "r") as file:
            return json.load(file)

    except Exception as e:
        print(f"Error processing theHarvester output for {domain}: {e}")
        return {}

# Main function
if __name__ == "__main__":
    all_results = {}

    for domain in target_domains:
        harvester_data = run_theHarvester(domain)  # Run theHarvester

        # Extract data safely
        emails = harvester_data.get("emails", [])
        usernames = harvester_data.get("users", [])

        all_results[domain] = {
            "emails": emails,
            "usernames": usernames
        }

    # Save extracted data to a JSON file
    with open("final_results.json", "w") as f:
        json.dump(all_results, f, indent=4)

    print("\nAll data saved in final_results.json")
