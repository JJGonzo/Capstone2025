import json

def load_results(filename="results.json"):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading results file: {e}")
        return []

def search_osint(data, query, field):
    query = query.lower()
    field_map = {
        'email': 'emails',
        'bitcoin': 'bitcoin_addresses',
        'monero': 'monero_addresses',
        'username': 'usernames',
        'ip': 'ips'
    }

    if field not in field_map:
        print(f"Invalid field: {field}")
        return []

    key = field_map[field]
    matches = []

    for entry in data:
        values = entry.get(key, [])
        if any(query in str(value).lower() for value in values):
            matches.append(entry)

    return matches

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

if __name__ == "__main__":
    data = load_results()

    if not data:
        print("No data to search.")
        exit(0)

    field = choose_field()
    if not field:
        print("Invalid selection. Exiting.")
        exit(1)

    query = input(f"🔍 Enter search term for {field}: ").strip()
    results = search_osint(data, query, field)

    if results:
        print(f"\n✅ Found {len(results)} matching result(s):\n")
        for r in results:
            print(f"URL: {r['url']}")
            if r['emails']: print(f"  Emails: {r['emails']}")
            if r['bitcoin_addresses']: print(f"  Bitcoin: {r['bitcoin_addresses']}")
            if r['monero_addresses']: print(f"  Monero: {r['monero_addresses']}")
            if r['usernames']: print(f"  Usernames: {r['usernames']}")
            if r['ips']: print(f"  IPs: {r['ips']}")
            print("-" * 60)
    else:
        print("No matches found.")
