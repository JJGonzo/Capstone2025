import sqlite3

def search_database(keyword):
    conn = sqlite3.connect("../data/osint_data.db")
    cursor = conn.cursor()
    
    query = "SELECT * FROM ThreatData WHERE forum_post LIKE ?"
    cursor.execute(query, ('%' + keyword + '%',))

    results = cursor.fetchall()
    conn.close()
    
    return results

# Example usage
keyword = input("Enter search keyword: ")
results = search_database(keyword)
for row in results:
    print(f"Username: {row[1]}, Post: {row[2]}")
