import subprocess
import json
import os

# List of target domains to scan
target_domains = ["uwsp.edu"]

# Function to run theHarvester and ensure JSON file is saved
def run_theHarvester(domain):
    print(f"\nRunning theHarvester for: {domain}")

    # Define output filename
    output_file = f"{domain.replace('.', '_')}.json"
    
    # Run theHarvester with file output option
    command = f"theHarvester -d {domain} -b bing -f {output_file}"
    subprocess.run(command, shell=True)

    # Ensure the file was created before reading
    if os.path.exists(output_file):
        try:
            with open(output_file, "r") as f:
                data = json.load(f)
                return data  # Return parsed JSON
        except json.JSONDecodeError as e:
            print(f"Error parsing JSON file {output_file}: {e}")
    else:
        print(f"Error: JSON file {output_file} not found.")

    return {}  # Return empty dict if error occurs

# Main function
if __name__ == "__main__":
    all_results = {}

    for domain in target_domains:
        harvester_data = run_theHarvester(domain)  # Run theHarvester

        if harvester_data and "emails" in harvester_data:
            emails = harvester_data["emails"]
        else:
            emails = []

        if harvester_data and "users" in harvester_data:
            usernames = harvester_data["users"]
        else:
            usernames = []

        all_results[domain] = {
            "emails": emails,
            "usernames": usernames
        }

    # Save extracted data to a JSON file
    with open("final_results.json", "w") as f:
        json.dump(all_results, f, indent=4)

    print("\nAll data saved in final_results.json")
