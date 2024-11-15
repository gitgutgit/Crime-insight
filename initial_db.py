import sqlite3
import toml
################## secret1 is for server, secrets2 is for local, 
config = toml.load("secrets2.toml") 
DB_URL = config["database"]["DB_URL"]

def create_database():
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Crime(
            Crime_id INTEGER PRIMARY KEY,
            Crime_date DATE
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Category(
            Category_id INTEGER PRIMARY KEY,
            Category_name TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Criminal(
            Criminal_id INTEGER PRIMARY KEY,
            Criminal_name TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Categorize1(
            Crime_id INTEGER REFERENCES Crime(Crime_id),
            Category_id INTEGER REFERENCES Category(Category_id),
            PRIMARY KEY (Crime_id, Category_id)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Commited_by(
            Crime_id INTEGER REFERENCES Crime(Crime_id),
            Criminal_id INTEGER REFERENCES Criminal(Criminal_id),
            PRIMARY KEY (Crime_id, Criminal_id)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS categorize2(
            criminal_id INTEGER REFERENCES Criminal(Criminal_id),
            category_id INTEGER REFERENCES Category(Category_id),
            PRIMARY KEY (criminal_id, category_id)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS place_Lives_in(
            place_id INTEGER,
            street_address TEXT,
            post_code INTEGER,
            state TEXT,
            Gender TEXT,
            Criminal_id INTEGER REFERENCES Criminal(Criminal_id) ON DELETE CASCADE,
            PRIMARY KEY (place_id, Criminal_id)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
            user_id INTEGER PRIMARY KEY,
            user_name TEXT,
            user_email TEXT
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Report(
            user_id INTEGER REFERENCES users(user_id),
            Crime_id INTEGER REFERENCES Crime(Crime_id),
            Report_date DATE,
            Report_details TEXT,
            PRIMARY KEY (user_id, Crime_id)
        );
    ''')
    conn.commit()
    conn.close()
    print("Database and table(s) created successfully.")



def insert_crime(crime_id, crime_date):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()
    #check the crime_id is already exist or not
    cursor.execute('SELECT COUNT(*) FROM Crime WHERE Crime_id = ?', (crime_id,))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO Crime (Crime_id, Crime_date) VALUES (?, ?)', (crime_id, crime_date))
        print(f"Crime with ID {crime_id} inserted successfully.")
    else:
        print(f"Crime with ID {crime_id} already exists.")
    conn.commit()
    conn.close()
  

def insert_category(category_id, category_name):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()
    #check the category_id is already exist or not
    cursor.execute('SELECT COUNT(*) FROM Category WHERE Category_id = ?', (category_id,))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO Category (Category_id, Category_name) VALUES (?, ?)', (category_id, category_name))
        print(f"Category with ID {category_id} inserted successfully.")
    else:
        print(f"Category with ID {category_id} already exists.")
    conn.commit()
    conn.close()
def insert_categorize1(Crime_id,Category_id):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()
    #check the category_id is already exist or not
    cursor.execute('SELECT COUNT(*) FROM Categorize1 WHERE Crime_id = ? AND Category_id = ?', (Crime_id,Category_id))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO Categorize1 (Crime_id, Category_id) VALUES (?, ?)', (Crime_id, Category_id))
        print(f"Category with ID {Category_id} inserted successfully.")
    else:
        print(f"Category with ID {Category_id} already exists.")
    conn.commit()
    conn.close()

#####

def insert_criminal(criminal_id, criminal_name):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Criminal WHERE Criminal_id = ?', (criminal_id,))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO Criminal (Criminal_id, Criminal_name) VALUES (?, ?)', (criminal_id, criminal_name))
        print(f"Criminal with ID {criminal_id} inserted successfully.")
    else:
        print(f"Criminal with ID {criminal_id} already exists.")
    conn.commit()
    conn.close()


def insert_commited_by(crime_id, criminal_id):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Commited_by WHERE Crime_id = ? AND Criminal_id = ?', (crime_id, criminal_id))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO Commited_by (Crime_id, Criminal_id) VALUES (?, ?)', (crime_id, criminal_id))
        print(f"Crime ID {crime_id} linked to Criminal ID {criminal_id}.")
    else:
        print(f"Link between Crime ID {crime_id} and Criminal ID {criminal_id} already exists.")
    conn.commit()
    conn.close()


def insert_place_lives_in(place_id, street_address, post_code, state, gender, criminal_id):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM place_Lives_in WHERE place_id = ? AND Criminal_id = ?', (place_id, criminal_id))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO place_Lives_in (place_id, street_address, post_code, state, Gender, Criminal_id) VALUES (?, ?, ?, ?, ?, ?)', 
                       (place_id, street_address, post_code, state, gender, criminal_id))
        print(f"Place ID {place_id} added for Criminal ID {criminal_id}.")
    else:
        print(f"Place ID {place_id} for Criminal ID {criminal_id} already exists.")
    conn.commit()
    conn.close()


def insert_user(user_id, user_name, user_email):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM users WHERE user_id = ?', (user_id,))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO users (user_id, user_name, user_email) VALUES (?, ?, ?)', (user_id, user_name, user_email))
        print(f"User {user_name} with ID {user_id} inserted successfully.")
    else:
        print(f"User with ID {user_id} already exists.")
    conn.commit()
    conn.close()


def insert_report(user_id, crime_id, report_date, report_details):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM Report WHERE user_id = ? AND Crime_id = ?', (user_id, crime_id))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO Report (user_id, Crime_id, Report_date, Report_details) VALUES (?, ?, ?, ?)', 
                       (user_id, crime_id, report_date, report_details))
        print(f"Report for Crime ID {crime_id} by User ID {user_id} inserted successfully.")
    else:
        print(f"Report for Crime ID {crime_id} by User ID {user_id} already exists.")
    conn.commit()
    conn.close()


def insert_categorize2(criminal_id, category_id):
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()
    cursor.execute('SELECT COUNT(*) FROM categorize2 WHERE criminal_id = ? AND category_id = ?', (criminal_id, category_id))
    if cursor.fetchone()[0] == 0:
        cursor.execute('INSERT INTO categorize2 (criminal_id, category_id) VALUES (?, ?)', (criminal_id, category_id))
        print(f"Criminal ID {criminal_id} linked to Category ID {category_id}.")
    else:
        print(f"Link between Criminal ID {criminal_id} and Category ID {category_id} already exists.")
    conn.commit()
    conn.close()



if __name__ == "__main__":
    create_database()

    # Insert crimes
    for crime_id, crime_date in [
    (1000, '2023-10-26'),
    (1001, '2023-10-27'),
    (1002, '2023-10-28'),
    (1003, '2023-10-29'),
    (1004, '2023-10-30'),
    (1005, '2023-10-31'),
    (1006, '2023-11-01'),
    (1007, '2023-11-02'),
    (1008, '2023-11-03'),
    (1009, '2023-11-04'),
    ]:
        insert_crime(crime_id, crime_date)

    # Insert categories
    for category_id, category_name in [
    (1, 'Robbery'),
    (2, 'Assault'),
    (3, 'burglary'),
    (4, 'Vandalism'),
    (5, 'Drug-related'),
    ]:
        insert_category(category_id, category_name)

    # Link crimes to categories in Categorize1
    for crime_id, category_id in [
    (1000, 1),
    (1001, 2),
    (1002, 3),
    (1003, 4),
    (1004, 5),
    (1005, 1),
    (1006, 2),
    (1007, 3),
    (1008, 4),
    (1009, 5),
    ]:
        insert_categorize1(crime_id, category_id)

    




    # Insert criminals
    for i, name in enumerate(['John Doe', 'Jane Smith', 'Robert Brown', 'Emily Davis', 'Michael Wilson', 
                               'Sarah Garcia', 'David Rodriguez', 'Jessica Martinez', 'Christopher Anderson', 'Ashley Thomas'], 1):
        insert_criminal(i, name)


    # Link criminals to categories in Categorize2
    for criminal_id, category_id in [
    (1, 1),
    (2, 2),
    (3, 3),
    (4, 4),
    (5, 5),
    ]:
        insert_categorize2(criminal_id, category_id)

    # Insert Commited_by
    for crime_id, criminal_id in [(1000, 1), (1001, 2), (1002, 3), (1003, 4), (1004, 5), (1005, 6), (1006, 7), (1007, 8), (1008, 9), (1009, 10)]:
        insert_commited_by(crime_id, criminal_id)

    # Insert place_lives_in
    places = [
        (1, '123 Main St', 12345, 'NY', 'Male', 1),
        (2, '456 Oak Ave', 67890, 'CA', 'Female', 2),
        (3, '789 Pine Rd', 13579, 'TX', 'Male', 3),
        (4, '1011 Elm Ln', 24680, 'FL', 'Female', 4),
        (5, '1213 Birch Dr', 11223, 'IL', 'Male', 5),
        (6, '1415 Cedar Ct', 33445, 'PA', 'Female', 6),
        (7, '1617 Willow Pl', 55667, 'OH', 'Male', 7),
        (8, '1819 Maple Way', 77889, 'MI', 'Female', 8),
        (9, '2021 Redwood Ave', 99001, 'WA', 'Male', 9),
        (10, '2223 Spruce St', 11224, 'NY', 'Female', 10)
    ]
    for place in places:
        insert_place_lives_in(*place)

    # Insert users
    users = [
        (1, 'Admin User', 'admin@example.com'),
        (2, 'John Smith', 'john.smith@example.com'),
        (3, 'Jane Doe', 'jane.doe@example.com')
    ]
    for user in users:
        insert_user(*user)

    # Insert reports
    reports = [
    (1, 1000, '2023-10-27', 'Robbery at a convenience store'),
    (2, 1001, '2023-10-28', 'Assault near the park'),
    (3, 1002, '2023-10-29', 'Residential burglary'),
    (1, 1003, '2023-10-30', 'Graffiti on a public building'),
    (2, 1004, '2023-10-31', 'Drug possession arrest'),
    (3, 1005, '2023-11-01', 'Another robbery'),
    (1, 1006, '2023-11-02', 'Another assault'),
    (2, 1007, '2023-11-03', 'Another burglary'),
    (3, 1008, '2023-11-04', 'Another vandalism'),
    (1, 1009, '2023-11-05', 'Another drug possession arrest'),
    ]
    for report in reports:
        insert_report(*report)



    