import subprocess
import json
import os

# Target domains to scan
target_domains = ["uwsp.edu"]

def run_theHarvester(domain):
    print(f"\nRunning theHarvester for: {domain}")
    output_file = f"{domain.replace('.', '_')}.json"

    # Run theHarvester with JSON output
    command = f"theHarvester -d {domain} -b bing -f {output_file}"
    subprocess.run(command, shell=True)

    if not os.path.exists(output_file):
        print(f"Error: JSON file {output_file} not found.")
        return {}

    try:
        with open(output_file, "r") as f:
            return json.load(f)  # Return parsed JSON data
    except json.JSONDecodeError as e:
        print(f"Error parsing {output_file}: {e}")
        return {}

if __name__ == "__main__":
    all_results = {}

    for domain in target_domains:
        data = run_theHarvester(domain)

        all_results[domain] = {
            "emails": list(set(data.get("emails", []))),      # Remove duplicate emails
            "usernames": list(set(data.get("users", []))),    # Remove duplicate usernames
            "hosts": list(set(data.get("hosts", []))),        # Remove duplicate hosts
            "ips": list(set(data.get("ips", [])))             # Remove duplicate IPs
        }

    # Save results to JSON
    with open("final_results.json", "w") as f:
        json.dump(all_results, f, indent=4)

    print("\nAll data saved in final_results.json")
