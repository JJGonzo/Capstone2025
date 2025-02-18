import subprocess
import json
import os

# List of target domains to scan
target_domains = [
    "uwsp.edu",
]

# Function to run theHarvester and capture JSON output
def run_theHarvester(domain):
    print(f"\nRunning theHarvester for: {domain}")
    json_filename = f"{domain.replace('.', '_')}.json"
    command = f"theHarvester -d {domain} -b bing -f {json_filename}"

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)

        # Debugging output
        if result.returncode != 0:
            print(f"Error running theHarvester for {domain}: {result.stderr}")
            return {}

        # Check if JSON file exists and has data
        if not os.path.exists(json_filename) or os.path.getsize(json_filename) == 0:
            print(f"Error: {json_filename} is empty or does not exist!")
            return {}

        # Read JSON output from the file
        with open(json_filename, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError as e:
                print(f"Error parsing {json_filename}: {e}")
                return {}

    except Exception as e:
        print(f"Unexpected error: {e}")
        return {}

# Main function
if __name__ == "__main__":
    all_results = {}

    for domain in target_domains:
        harvester_data = run_theHarvester(domain)

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
