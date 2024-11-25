import sqlite3

# Connect to the database
conn = sqlite3.connect("items.db")
cursor = conn.cursor()

# Prompt the user to enter an SQL query
try:
    while True:
        query = input("Enter an SQL query (or type 'exit' to quit): ")
        if query.lower() == 'exit':
            break
        
        # Execute the query
        cursor.execute(query)

        # Fetch and display the results if it’s a SELECT query
        if query.strip().upper().startswith("SELECT"):
            results = cursor.fetchall()
            column_names = [description[0] for description in cursor.description]
            print(f"{' | '.join(column_names)}")
            print("-" * 40)
            for row in results:
                print(" | ".join(str(value) for value in row))
            print("\n")

except sqlite3.Error as e:
    print(f"An error occurred: {e}")

finally:
    # Close the database connection
    conn.close()