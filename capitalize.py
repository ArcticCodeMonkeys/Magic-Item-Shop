import sqlite3

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('items.db')
    conn.row_factory = sqlite3.Row  # So that we can access columns by name
    return conn

# Function to capitalize the first letter of each word in the rarity column
def capitalize_rarity_words():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get all rows in the Items table
    cursor.execute("SELECT name, rarity FROM Items")  # Changed 'id' to 'name' as the unique column
    rows = cursor.fetchall()

    # Iterate over each row and update the rarity column
    for row in rows:
        name = row['name']  # Using 'name' as the unique identifier
        rarity = row['rarity']

        if rarity:  # Ensure rarity is not None or empty
            # Capitalize each word in the rarity string
            capitalized_rarity = ' '.join([word.capitalize() for word in rarity.split()])
            
            # Update the rarity column with the capitalized value
            cursor.execute("UPDATE Items SET rarity = ? WHERE name = ?", (capitalized_rarity, name))  # Changed to 'name'
    
    # Commit the changes and close the connection
    conn.commit()
    conn.close()
    print("Rarity column updated successfully.")

# Run the function to capitalize the rarity column
if __name__ == "__main__":
    capitalize_rarity_words()