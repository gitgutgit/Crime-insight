import os
import toml
import sqlite3
import psycopg2
from flask import Flask, render_template, request,session,redirect,url_for ,flash
from datetime import datetime
# Load database configuration from secrets.toml
config = toml.load("secrets2.toml")
DB_URL = config["database"]["DB_URL"]
FOLDER_NAME = "templates"  # template folder name

# Set up Flask application with specified template folder
tmpl_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), FOLDER_NAME)
app = Flask(__name__, template_folder=tmpl_dir)
app.secret_key = os.urandom(24)  # Secret key for session management

# Database connection function
def get_db_connection():
    conn = sqlite3.connect(DB_URL)
    conn.row_factory = sqlite3.Row  # Enable dictionary-like cursor
    return conn

#sign in
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
            WHERE user_name = ? AND user_email = ?;
        """
        cursor.execute(query, (username, useremail))
        user = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if user:
            # Login successful, set session and redirect to index page
            print("Login successful for user:", user)  # Debugging output
            session['user_id'] = user['user_id']
            session['username'] = user['user_name']
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
    query = """
        SELECT c.Crime_id, c.Crime_date, cat.Category_name
        FROM Crime c
        JOIN Categorize1 cat1 ON c.Crime_id = cat1.Crime_id
        JOIN Category cat ON cat1.Category_id = cat.Category_id
    """
    cursor.execute(query)
    rows = cursor.fetchall()
    crimes = [{'Crime_id': row['Crime_id'], 'Crime_date': row['Crime_date'], 'Crime_category': row['Category_name']} for row in rows]
    conn.close()
    return render_template("index.html", crimes=crimes, username=session.get('username'))

# Route for criminal information based on search type
@app.route('/criminal_info', methods=["GET", "POST"])
def criminal_info():
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
            WHERE cr.Criminal_name = ?;
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
            WHERE c.Crime_id = ?;
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
            WHERE c.Crime_date = ?;
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
            WHERE p.state = ?;
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
        WHERE cat.Category_name = ?;
        """
        cursor.execute(query, (search_value,))
        data = [{'Crime_id': row[0], 'Crime_date': row[1], 'Criminal_id': row[2], 'Criminal_name': row[3], 'State': row[4], 'Category': row[5]} for row in cursor.fetchall()]


    cursor.close()
    conn.close()
    return render_template("criminal_info.html", data=data)




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
# Route to get criminal detail information
@app.route('/criminal_detail/<int:criminal_id>', methods=["GET"])
def criminal_detail(criminal_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT cr.Criminal_name, p.street_address, p.post_code, p.state, p.Gender
        FROM Criminal cr
        JOIN place_Lives_in p ON cr.Criminal_id = p.Criminal_id
        WHERE cr.Criminal_id = ?;
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
    return render_template("criminal_detail.html", data=data)



# Report page
@app.route('/report', methods=["GET"])
def report():
    conn = get_db_connection()
    cursor = conn.cursor()
    #list of Category
    cursor.execute("SELECT Category_id, Category_name FROM Category")
    categories = cursor.fetchall()

    #list of states
    cursor.execute("SELECT state FROM  place_Lives_in")  # 예시로 State 테이블과 컬럼명 사용
    states = cursor.fetchall()

    cursor.close()
    conn.close()
    return render_template("report.html", categories=categories,states=states)


# Insert Report
@app.route('/submit_report', methods=["POST"])
def submit_report():
    crime_date = request.form["crime_date"]
    criminal_name = request.form["criminal_name"]
    category_id = request.form["category_id"]
    state = request.form["state"]
    street_address = request.form["street_address"]
    post_code = request.form["post_code"]
    gender = request.form["gender"]
    report_details = request.form["report_details"]

    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()

    # Get new Crime_id
    cursor.execute("SELECT MAX(Crime_id) FROM Crime")
    max_crime_id = cursor.fetchone()[0]
    new_crime_id = max_crime_id + 1 if max_crime_id is not None else 1000

    # Insert new Crime
    cursor.execute("INSERT INTO Crime (Crime_id, Crime_date) VALUES (?, ?)", (new_crime_id, crime_date))

    # Get new Criminal_id
    cursor.execute("SELECT MAX(Criminal_id) FROM Criminal")
    max_criminal_id = cursor.fetchone()[0]
    new_criminal_id = max_criminal_id + 1 if max_criminal_id is not None else 1

    # Insert new Criminal
    cursor.execute("INSERT INTO Criminal (Criminal_id, Criminal_name) VALUES (?, ?)", (new_criminal_id, criminal_name))

    # Insert into Commited_by
    cursor.execute("INSERT INTO Commited_by (Crime_id, Criminal_id) VALUES (?, ?)", (new_crime_id, new_criminal_id))

    # Insert into Categorize1
    cursor.execute("INSERT INTO Categorize1 (Crime_id, Category_id) VALUES (?, ?)", (new_crime_id, category_id))

    # Insert into Categorize2
    cursor.execute("INSERT INTO Categorize2 (criminal_id, category_id) VALUES (?, ?)", (new_criminal_id, category_id))

    # Get new Place_id
    cursor.execute("SELECT MAX(place_id) FROM Place_Lives_in")
    max_place_id = cursor.fetchone()[0]
    new_place_id = max_place_id + 1 if max_place_id is not None else 1

    # Insert into Place_Lives_in
    cursor.execute("""
        INSERT INTO Place_Lives_in (place_id, street_address, post_code, state, Gender, Criminal_id)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (new_place_id, street_address, post_code, state, gender, new_criminal_id))

    # Insert into Report
    user_id = session.get("user_id", 1)  # 기본값 1
    report_date = datetime.now().date()
    cursor.execute("""
        INSERT INTO Report (User_id, Crime_id, Report_date, Report_details)
        VALUES (?, ?, ?, ?)
    """, (user_id, new_crime_id, report_date, report_details))

    conn.commit()
    cursor.close()
    conn.close()

    return redirect(url_for("index"))

#demo
@app.route('/crime/<int:crime_id>', methods=["GET"])
def crime_detail(crime_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Crime table join Report Table
    cursor.execute("""
        SELECT c.Crime_id, r.Report_date, c.Crime_Date, r.Report_details 
        FROM Crime c
        JOIN Report r ON c.Crime_id = r.Crime_id
        WHERE c.Crime_id = ?
    """, (crime_id,))
    
    crime_report_detail = cursor.fetchone()
    
    cursor.close()
    conn.close()
    
    
    return render_template("crime_detail.html", crime=crime_report_detail)

# Run the Flask app
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8111, debug=True)