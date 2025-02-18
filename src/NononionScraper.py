import subprocess
import json
import os

# List of target domains to scan
target_domains = ["uwsp.edu"]

# Function to run theHarvester and read the JSON output file
def run_theHarvester(domain):
    print(f"\nRunning theHarvester for: {domain}")

    # Define output filename
    output_file = f"{domain.replace('.', '_')}.json"

    # Run theHarvester with file output option
    command = f"theHarvester -d {domain} -b all -f {output_file}"
    subprocess.run(command, shell=True)

    # Ensure JSON file exists
    if not os.path.exists(output_file):
        print(f"Error: JSON file {output_file} not found.")
        return {}

    try:
        # Read and parse JSON file
        with open(output_file, "r") as f:
            data = json.load(f)
        
        return data  # Return parsed JSON data
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON file {output_file}: {e}")
        return {}

# Main function
if __name__ == "__main__":
    all_results = {}

    for domain in target_domains:
        harvester_data = run_theHarvester(domain)  # Run theHarvester

        # Extract emails and usernames
        emails = harvester_data.get("emails", [])
        usernames = harvester_data.get("users", [])

        # Store extracted data
        all_results[domain] = {
            "emails": emails,
            "usernames": usernames
        }

    # Save extracted data to a JSON file
    with open("final_results.json", "w") as f:
        json.dump(all_results, f, indent=4)

    print("\nAll data saved in final_results.json")
