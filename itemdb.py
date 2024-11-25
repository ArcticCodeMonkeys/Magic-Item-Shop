import sqlite3
import json

# Load JSON data from both files
with open('items.json') as f:
    data_first = json.load(f)

with open('prices.json') as f:
    data_second = json.load(f)

# Combine items from the second file with "value" into the first
values_map = {item["name"]: item.get("value") for item in data_second["item"]}
for item in data_first["item"]:
    item["value"] = values_map.get(item["name"], None)

# Find all unique keys (fields) across all items, serializing nested structures
all_keys = set()
for item in data_first["item"]:
    for key, value in item.items():
        # Serialize non-string fields (e.g., lists, dicts) to JSON strings
        if not isinstance(value, str):
            item[key] = json.dumps(value)
        all_keys.add(key)

# Connect to SQLite database
conn = sqlite3.connect("items.db")
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS Items")

# Create the table dynamically
columns = ", ".join(f"{key} TEXT" for key in all_keys)
cursor.execute(f"CREATE TABLE IF NOT EXISTS Items ({columns});")

# Insert data dynamically
for item in data_first["item"]:
    columns = ", ".join(item.keys())
    placeholders = ", ".join("?" for _ in item)
    values = tuple(item.values())
    cursor.execute(f"INSERT INTO Items ({columns}) VALUES ({placeholders})", values)

# Commit and close the connection
conn.commit()
conn.close()

print("Database created and data inserted successfully.")