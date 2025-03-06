import subprocess
import json
import os

# Target domains to scan - replace with your .onion domains
target_domains = [
    "dreadytofatroptsdj6io7l3xptbet6onoyno2yv7jicoxxnyazubrad.onion",  # Example .onion link
    "nzdmnfcf22s5pd3wvyfy3jhwoubv6qunmdglspqhurqunvr52khattdad.onion"  # Another example
]

# Configure the Tor Proxy (make sure Tor is running on port 9050)
TOR_PROXY = "socks5h://127.0.0.1:9050"

def run_theHarvester(domain):
    print(f"Running theHarvester for: {domain}")
    output_file = f"{domain.replace('.', '_')}.json"
    
    # Modify the command to ensure theHarvester uses the Tor proxy
    command = f"theHarvester -b all -f {output_file} -d {domain} --proxy {TOR_PROXY}"
    
    result = subprocess.run(command, shell=True)
    if result.returncode != 0:
        print(f"Error running theHarvester for {domain}")
        return
    
    print(f"theHarvester finished for {domain}, output saved to {output_file}")

# Run theHarvester with JSON output
def parse_json_output(output_file):
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
        run_theHarvester(domain)  # Run theHarvester for each domain
        output_file = f"{domain.replace('.', '_')}.json"
        data = parse_json_output(output_file)
        
        # Ensure the data is extracted correctly
        all_results[domain] = {
            "emails": list(set(data.get("emails", []))),   # Remove duplicate emails
            "usernames": list(set(data.get("users", []))),  # Remove duplicate usernames
            "hosts": list(set(data.get("hosts", []))),      # Remove duplicate hosts
            "ips": list(set(data.get("ips", [])))           # Remove duplicate IPs
        }

    # Save results to JSON
    with open("final_results.json", "w") as f:
        json.dump(all_results, f, indent=4)

    print("\nAll data saved in final_results.json")
