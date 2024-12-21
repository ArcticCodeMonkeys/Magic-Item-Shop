from flask import Flask, render_template, request, jsonify
import sqlite3

app = Flask(__name__)

# Connect to SQLite database
def get_db_connection():
    conn = sqlite3.connect('items.db')
    conn.row_factory = sqlite3.Row  # So that we can access columns by name
    return conn

# Query items from the database
def query_items(columns, sort_by=None, sort_order="ASC"):
    columns_str = ', '.join(columns)
    query = f"SELECT {columns_str} FROM Items"
    
    if sort_by == "rarity":
        query += """
            ORDER BY
                CASE rarity
                    WHEN 'common' THEN 1
                    WHEN 'uncommon' THEN 2
                    WHEN 'rare' THEN 3
                    WHEN 'epic' THEN 4
                    WHEN 'legendary' THEN 5
                END
        """
    query += f" {sort_order}"

    conn = get_db_connection()
    items = conn.execute(query).fetchall()
    conn.close()
    return items

# Get column names from the database
def get_column_names():
    conn = get_db_connection()
    cursor = conn.execute('SELECT * FROM Items LIMIT 1')
    column_names = [description[0] for description in cursor.description]
    conn.close()
    return column_names

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/get_columns', methods=['GET'])
def get_columns():
    column_names = get_column_names()
    return jsonify({'columns': column_names})

@app.route('/load_items', methods=['POST'])
def load_items():
    data = request.get_json()
    columns = data.get('columns', [])
    if not columns:
        return jsonify({'error': 'No columns selected'}), 400

    conn = get_db_connection()
    items = query_items(columns)
    conn.close()

    items_list = [dict(item) for item in items]
    return jsonify({'items': items_list})

if __name__ == "__main__":
    app.run(debug=True)