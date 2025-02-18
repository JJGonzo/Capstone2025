import subprocess
import json

# List of target domains to scan
target_domains = ["uwsp.edu"]

# Function to run theHarvester and capture JSON output
def run_theHarvester(domain):
    print(f"\nRunning theHarvester for: {domain}")
    command = f"theHarvester -d {domain} -b bing -j"  # Use bing explicitly

    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        
        # Print outputs for debugging
        print(f"STDOUT: {result.stdout}")  
        print(f"STDERR: {result.stderr}")  

        # Ensure stdout is not empty before parsing JSON
        if result.stdout.strip():
            return json.loads(result.stdout)
        else:
            print(f"No valid JSON output for {domain}")
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
