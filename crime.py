#!/usr/bin/env python3

import os
import toml
import psycopg2
from flask import Flask, render_template

config = toml.load("secrets.toml")
DB_URL = config["database"]["DB_URL"]

tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), './')
app = Flask(__name__, template_folder=tmpl_dir)

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

# Index route to display Crime data
@app.route('/', methods=["GET"])
def index():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Get Crime table data
    cursor.execute("SELECT Crime_id, Crime_date FROM Crime")
    rows = cursor.fetchall()
    crimes = [{'Crime_id': row[0], 'Crime_date': row[1]} for row in rows]

    cursor.close()
    conn.close()
    return render_template("index.html", crimes=crimes)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8111, debug=True)
