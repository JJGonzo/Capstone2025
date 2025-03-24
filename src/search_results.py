import json

def load_results(filename="results.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading results file: {e}")
        return []

def choose_field():
    fields = {
        '1': 'email',
        '2': 'bitcoin',
        '3': 'monero',
        '4': 'username',
        '5': 'ip'
    }

    print("\nWhich field do you want to search?")
    for k, v in fields.items():
        print(f"  {k}. {v.title()}")

    choice = input("Enter field number: ").strip()
    return fields.get(choice)

def list_unique_values(data, field_key):
    unique_values = set()
    for entry in data:
        for value in entry.get(field_key, []):
            unique_values.add(value)
    return sorted(unique_values)

def filter_results(data, field_key, query):
    query = query.lower()
    matches = []
    for entry in data:
        values = entry.get(field_key, [])
        if any(query in value.lower() for value in values):
            matches.append(entry)
    return matches

def display_results(results):
    print(f"\n✅ Found {len(results)} matching result(s):\n")
    for r in results:
        print(f"URL: {r['url']}")
        if r['emails']: print(f"  Emails: {r['emails']}")
        if r['bitcoin_addresses']: print(f"  Bitcoin: {r['bitcoin_addresses']}")
        if r['monero_addresses']: print(f"  Monero: {r['monero_addresses']}")
        if r['usernames']: print(f"  Usernames: {r['usernames']}")
        if r['ips']: print(f"  IPs: {r['ips']}")
        print("-" * 60)

if __name__ == "__main__":
    data = load_results()
    if not data:
        print("No data to search.")
        exit(0)

    field = choose_field()
    if not field:
        print("Invalid selection. Exiting.")
        exit(1)

    field_map = {
        'email': 'emails',
        'bitcoin': 'bitcoin_addresses',
        'monero': 'monero_addresses',
        'username': 'usernames',
        'ip': 'ips'
    }

    field_key = field_map[field]
    all_values = list_unique_values(data, field_key)

    print(f"\n📋 Found {len(all_values)} unique values in the {field.title()} field:")
    for val in all_values:
        print(f"  - {val}")

    query = input(f"\n🔍 Enter a search term to filter, or press Enter to list all: ").strip()

    if query:
        results = filter_results(data, field_key, query)
    else:
        # Return all results that have at least one value in the selected field
        results = [entry for entry in data if entry.get(field_key)]

    if results:
        display_results(results)
    else:
        print("No matches found.")
