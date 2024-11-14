#!/usr/bin/env python3

import os
import toml
import psycopg2
from flask import Flask, render_template, request,session,redirect,url_for ,flash

# Load database configuration from secrets.toml
config = toml.load("secrets.toml")
DB_URL = config["database"]["DB_URL"]
FOLDER_NAME = "templates"  # template folder name

# Set up Flask application with specified template folder
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), FOLDER_NAME)
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = os.urandom(24)  # Secret key for session management

# Database connection function
def get_db_connection():
    conn = psycopg2.connect(DB_URL)
    return conn

#demo
@app.route('/signin', methods=["GET", "POST"])
def signin():
    if request.method == "POST":
        username = request.form.get("username")
        useremail = request.form.get("useremail")
        
        if not username or not useremail:
            flash("Username and email are required.")
            return render_template("signin.html")
        
        conn = get_db_connection()
        cursor = conn.cursor()
        query = """
            SELECT user_id, user_name, user_email FROM users
            WHERE user_name = %s AND user_email = %s;
        """
        cursor.execute(query, (username, useremail))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            # Login successful, set session and redirect to index page
            print("Login successful for user:", user)  # Debugging output
            session['user_id'] = user[0]
            session['username'] = user[1]
            return redirect(url_for('index'))
        else:
            # Login failed, stay on signin page with an error message
            print("Login failed for username:", username, "and useremail:", useremail)  # Debugging output
            flash("Invalid username or email.")
            return render_template("signin.html")
    
    return render_template("signin.html")

# Index route to display Crime data
@app.route('/', methods=["GET"])
def index():
    if 'user_id' not in session:
        return redirect(url_for('signin'))
    
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
    return render_template("index.html", crimes=crimes, username=session.get('username'))

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
            SELECT c.Crime_id, c.Crime_date, cr.Criminal_id, cr.Criminal_name, p.state, cat.Category_name
            FROM Crime c
            JOIN Commited_by cb ON c.Crime_id = cb.Crime_id
            JOIN Criminal cr ON cb.Criminal_id = cr.Criminal_id
            JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
            JOIN Categorize1 cat1 ON c.Crime_id = cat1.Crime_id
            JOIN Category cat ON cat1.Category_id = cat.Category_id
            WHERE cr.Criminal_name = %s;
        """
        cursor.execute(query, (search_value,))
        data = [{'Crime_id': row[0], 'Crime_date': row[1], 'Criminal_id': row[2], 'Criminal_name': row[3], 'State': row[4], 'Category': row[5]} for row in cursor.fetchall()]

    # Search by crime ID
    elif search_type == "crime_id":
        query = """
            SELECT c.Crime_id, c.Crime_date, cr.Criminal_id, cr.Criminal_name, p.state, cat.Category_name
            FROM Crime c
            JOIN Commited_by cb ON c.Crime_id = cb.Crime_id
            JOIN Criminal cr ON cb.Criminal_id = cr.Criminal_id
            JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
            JOIN Categorize1 cat1 ON c.Crime_id = cat1.Crime_id
            JOIN Category cat ON cat1.Category_id = cat.Category_id
            WHERE c.Crime_id = %s;
        """
        cursor.execute(query, (search_value,))
        data = [{'Crime_id': row[0], 'Crime_date': row[1], 'Criminal_id': row[2], 'Criminal_name': row[3], 'State': row[4], 'Category': row[5]} for row in cursor.fetchall()]

    # Search by specific date
    elif search_type == "specific_date":
        query = """
            SELECT c.Crime_id, c.Crime_date, cr.Criminal_id, cr.Criminal_name, p.state, cat.Category_name
            FROM Crime c
            JOIN Commited_by cb ON c.Crime_id = cb.Crime_id
            JOIN Criminal cr ON cb.Criminal_id = cr.Criminal_id
            JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
            JOIN Categorize1 cat1 ON c.Crime_id = cat1.Crime_id
            JOIN Category cat ON cat1.Category_id = cat.Category_id
            WHERE c.Crime_date = %s;
        """
        cursor.execute(query, (search_value,))
        data = [{'Crime_id': row[0], 'Crime_date': row[1], 'Criminal_id': row[2], 'Criminal_name': row[3], 'State': row[4], 'Category': row[5]} for row in cursor.fetchall()]

    # Search by state
    elif search_type == "state":
        query = """
            SELECT c.Crime_id, c.Crime_date, cr.Criminal_id, cr.Criminal_name, p.state, cat.Category_name
            FROM Crime c
            JOIN Commited_by cb ON c.Crime_id = cb.Crime_id
            JOIN Criminal cr ON cb.Criminal_id = cr.Criminal_id
            JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
            JOIN Categorize1 cat1 ON c.Crime_id = cat1.Crime_id
            JOIN Category cat ON cat1.Category_id = cat.Category_id
            WHERE p.state = %s;
        """
        cursor.execute(query, (search_value,))
        data = [{'Crime_id': row[0], 'Crime_date': row[1], 'Criminal_id': row[2], 'Criminal_name': row[3], 'State': row[4], 'Category': row[5]} for row in cursor.fetchall()]
    elif search_type == "category":
        query = """
        SELECT c.Crime_id, c.Crime_date, cr.Criminal_id, cr.Criminal_name, p.state, cat.Category_name
        FROM Crime c
        JOIN Categorize1 cat1 ON c.Crime_id = cat1.Crime_id
        JOIN Category cat ON cat1.Category_id = cat.Category_id
        JOIN Commited_by cb ON c.Crime_id = cb.Crime_id
        JOIN Criminal cr ON cb.Criminal_id = cr.Criminal_id
        JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
        WHERE cat.Category_name = %s;
        """
        cursor.execute(query, (search_value,))
        data = [{'Crime_id': row[0], 'Crime_date': row[1], 'Criminal_id': row[2], 'Criminal_name': row[3], 'State': row[4], 'Category': row[5]} for row in cursor.fetchall()]


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


# demo version
@app.route('/criminal_info/<int:criminal_id>', methods=["GET"])
def criminal_info(criminal_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT cr.Criminal_name, p.street_address, p.post_code, p.state, p.Gender
        FROM Criminal cr
        JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
        WHERE cr.Criminal_id = %s;
    """
    cursor.execute(query, (criminal_id,))
    result = cursor.fetchone()

    # Criminal detail information
    if result:
        data = {
            'Criminal_name': result[0],
            'Street_address': result[1],
            'Post_code': result[2],
            'State': result[3],
            'Gender': result[4]
        }
    else:
        data = None

    cursor.close()
    conn.close()
    return render_template("criminal_info.html", data=data)


# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8111, debug=True)