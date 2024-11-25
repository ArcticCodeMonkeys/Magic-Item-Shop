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
                    WHEN 'very rare' THEN 4
                    WHEN 'legendary' THEN 5
                    WHEN 'artifact' THEN 6
                    ELSE 7
                END {sort_order}
        """.format(sort_order=sort_order)
    elif sort_by == "value":
        query += f" ORDER BY CAST(value AS REAL) {sort_order}"
    elif sort_by:
        query += f" ORDER BY {sort_by} {sort_order}"

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

# Fetch column names from the database
def get_column_names():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(Items)")
    columns = [column['name'] for column in cursor.fetchall()]
    conn.close()
    return columns

# Route for serving the front-end
@app.route("/")
def index():
    return render_template("index.html")

# Route for fetching available columns
@app.route("/get_columns", methods=["GET"])
def get_columns():
    columns = get_column_names()
    return jsonify(columns)

# Route for fetching items with sorting
@app.route("/get_items", methods=["GET"])
def get_items():
    columns = request.args.getlist('columns')
    sort_by = request.args.get('sort_by')
    sort_order = request.args.get('sort_order', 'ASC')
    
    if not columns:
        columns = ['name', 'rarity', 'value']
    
    data = query_items(columns, sort_by, sort_order)
    
    return jsonify(data)

if __name__ == "__main__":
    app.run(debug=True)