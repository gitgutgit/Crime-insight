#!/usr/bin/env python3

import os
import toml
import psycopg2
from flask import Flask, render_template, request

# Load database configuration from secrets.toml
config = toml.load("secrets.toml")
DB_URL = config["database"]["DB_URL"]
FOLDER_NAME = "templates"  # 템플릿 폴더 이름

# Set up Flask application with specified template folder
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), FOLDER_NAME)
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
    query ="""
            SELECT c.Crime_id, c.Crime_date, cat.Category_name
            FROM Crime c
            JOIN Categorize1 cat1 ON c.Crime_id = cat1.Crime_id
            JOIN Category cat ON cat1.Category_id = cat.Category_id
        """
    cursor.execute(query)
    rows = cursor.fetchall()
    crimes = [{'Crime_id': row[0], 'Crime_date': row[1], 'Crime_category': row[2]} for row in rows]
    cursor.close()
    conn.close()
    return render_template("index.html", crimes=crimes)

# Route for offender information based on search type
@app.route('/offender_info', methods=["GET", "POST"])
def offender_info():
    conn = get_db_connection()
    cursor = conn.cursor()
    search_type = request.form.get("search_type")
    search_value = request.form.get("search_value")

    data = []

    # Search by criminal name
    if search_type == "criminal_name":
        query = """
            SELECT c.Crime_id, c.Crime_date, cr.Criminal_name, p.state
            FROM Crime c
            JOIN Commited_by cb ON c.Crime_id = cb.Crime_id
            JOIN Criminal cr ON cb.Criminal_id = cr.Criminal_id
            JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
            WHERE cr.Criminal_name = %s;
        """
        cursor.execute(query, (search_value,))
        data = [{'Crime_id': row[0], 'Crime_date': row[1], 'Criminal_name': row[2], 'State': row[3]} for row in cursor.fetchall()]

    # Search by crime ID
    elif search_type == "crime_id":
        query = """
            SELECT c.Crime_id, c.Crime_date, cr.Criminal_name, p.state
            FROM Crime c
            JOIN Commited_by cb ON c.Crime_id = cb.Crime_id
            JOIN Criminal cr ON cb.Criminal_id = cr.Criminal_id
            JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
            WHERE c.Crime_id = %s;
        """
        cursor.execute(query, (search_value,))
        data = [{'Crime_id': row[0], 'Crime_date': row[1], 'Criminal_name': row[2], 'State': row[3]} for row in cursor.fetchall()]
    # do diffrent way to show the  Categorize2!
    elif search_type == "category":
        query = """
        SELECT DISTINCT c.Crime_id, c.Crime_date, cr.Criminal_name, p.state
        FROM Criminal cr
        JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
        JOIN categorize2 cat2 ON cr.Criminal_id = cat2.criminal_id
        JOIN Category cat ON cat2.category_id = cat.category_id
        JOIN categorize1 cat1 ON cat.category_id = cat1.category_id
        JOIN Crime c ON cat1.crime_id = c.crime_id
        WHERE cat.Category_name = %s;
        """
        cursor.execute(query, (search_value,))
        data = [{'Crime_id': row[0], 'Crime_date': row[1], 'Criminal_name': row[2], 'State': row[3]} for row in cursor.fetchall()]

    # Search by specific date
    elif search_type == "specific_date":
        query = """
            SELECT c.Crime_id, c.Crime_date, cr.Criminal_name, p.state
            FROM Crime c
            JOIN Commited_by cb ON c.Crime_id = cb.Crime_id
            JOIN Criminal cr ON cb.Criminal_id = cr.Criminal_id
            JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
            WHERE c.Crime_date = %s;
        """
        cursor.execute(query, (search_value,))
        data = [{'Crime_id': row[0], 'Crime_date': row[1], 'Criminal_name': row[2], 'State': row[3]} for row in cursor.fetchall()]

    # Search by state
    elif search_type == "state":
        query = """
            SELECT c.Crime_id, c.Crime_date, cr.Criminal_name, p.state
            FROM Crime c
            JOIN Commited_by cb ON c.Crime_id = cb.Crime_id
            JOIN Criminal cr ON cb.Criminal_id = cr.Criminal_id
            JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
            WHERE p.state = %s;
        """
        cursor.execute(query, (search_value,))
        data = [{'Crime_id': row[0], 'Crime_date': row[1], 'Criminal_name': row[2], 'State': row[3]} for row in cursor.fetchall()]

    cursor.close()
    conn.close()
    return render_template("offender_info.html", data=data)



#aggregatiron!!

# Route to get the count of crimes by category
@app.route('/crime_category_count', methods=["GET"])
def crime_category_count():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT cat.Category_name, COUNT(c.Crime_id) AS Number_of_Crimes
        FROM Category cat
        JOIN Categorize1 cat1 ON cat.Category_id = cat1.Category_id
        JOIN Crime c ON cat1.Crime_id = c.Crime_id
        GROUP BY cat.Category_name;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    data = [{'Category_name': row[0], 'Number_of_Crimes': row[1]} for row in results]
    cursor.close()
    conn.close()
    return render_template("crime_category_count.html", data=data)

# Route to get the number of offenders by state
@app.route('/offender_count_by_state', methods=["GET"])
def offender_count_by_state():
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT p.state, COUNT(cr.Criminal_id) AS Number_of_Criminals
        FROM place_Lives_in p
        JOIN Criminal cr ON p.Criminal_id = cr.Criminal_id
        GROUP BY p.state;
    """
    cursor.execute(query)
    results = cursor.fetchall()
    data = [{'State': row[0], 'Number_of_Criminals': row[1]} for row in results]
    cursor.close()
    conn.close()
    return render_template("offender_count_by_state.html", data=data)

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8111, debug=True)
