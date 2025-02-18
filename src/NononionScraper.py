import subprocess
import json
import os

# List of target domains to scan
target_domains = ["uwsp.edu"]

# Function to run theHarvester and read the generated JSON file
def run_theHarvester(domain):
    print(f"\nRunning theHarvester for: {domain}")

    output_file = f"{domain.replace('.', '_')}.json"
    command = f"theHarvester -d {domain} -b bing -f {output_file}"  # Use Google instead of "all"

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Print outputs for debugging
        print(f"STDOUT: {result.stdout}")  
        print(f"STDERR: {result.stderr}")  

        # Check if the JSON file exists before reading it
        if os.path.exists(output_file):
            with open(output_file, "r") as file:
                return json.load(file)
        else:
            print(f"Error: JSON file {output_file} not found.")
            return {}

    except json.JSONDecodeError as e:
        print(f"Error parsing JSON output for {domain}: {e}")
        return {}
    except Exception as e:
        print(f"Error running theHarvester for {domain}: {e}")
        return {}

# Main function
if __name__ == "__main__":
    all_results = {}

    for domain in target_domains:
        harvester_data = run_theHarvester(domain)  # Run theHarvester
        
        if harvester_data and "emails" in harvester_data and "users" in harvester_data:
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

    print("\nAll data saved in final_results.json")
