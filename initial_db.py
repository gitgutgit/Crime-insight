import sqlite3
DB_URL = 'db.db'
def create_database():
    # connect database( if db.db not exist then create)
    conn = sqlite3.connect(DB_URL)
    cursor = conn.cursor()

    # crime Table execute
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Crime(
            Crime_id INTEGER PRIMARY KEY,
            Crime_date DATE
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Category (
        Category_id Integer PRIMARY KEY,
        Category_name text
);
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Criminal(
           Category_id Integer PRIMARY KEY,
           Category_name text
        );
    ''')
    cursor.execute('''
       CREATE TABLE IF NOT EXISTS Categorize1(
            Crime_id Integer REFERENCES Crime(Crime_id),
            Category_id Integer REFERENCES Category(Category_id),
            PRIMARY KEY (Crime_id, Category_id)
        );
    ''')

    cursor.execute('''
     CREATE TABLE IF NOT EXISTS Criminal(
        Criminal_id Integer PRIMARY KEY,
        Criminal_name text);    
    ''')
    cursor.execute('''
          CREATE TABLE IF NOT EXISTS Commited_by (
            Crime_id INTEGER REFERENCES Crime(Crime_id),
            Criminal_id INTEGER REFERENCES Criminal(Criminal_id),
            PRIMARY KEY (Crime_id, Criminal_id)
);         
''')
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS categorize2(
            criminal_id Integer REFERENCES Criminal(Criminal_id),
            category_id Integer REFERENCES Category(Category_id),
            PRIMARY KEY (criminal_id, category_id)
);
''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS place_Lives_in (
    place_id Integer,
    street_address text,
    post_code Integer,
    state text,
    Gender text,
    Criminal_id Integer,
    PRIMARY KEY (place_id, Criminal_id),
    FOREIGN KEY (Criminal_id) REFERENCES Criminal(Criminal_id) ON DELETE CASCADE
);
''')

    cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
  user_id INTEGER PRIMARY KEY,
  user_name TEXT,
  user_email TEXT
);
                   ''')
    
    cursor.execute('''
CREATE TABLE IF NOT EXISTS Report (
    user_id INTEGER REFERENCES users(user_id),
    Crime_id INTEGER REFERENCES Crime(Crime_id),
    Report_date DATE,
    Report_details TEXT,
    PRIMARY KEY (user_id, Crime_id)
);
                   ''')

    # commit and close
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

if __name__ == "__main__":
    create_database()
    #inser_crime
    insert_crime(1000, '2023-10-26')
    insert_crime(1001, '2023-10-27')
    insert_crime(1002, '2023-10-28')
    insert_crime(1003, '2023-10-29')
    insert_crime(1004, '2023-10-30')
    insert_crime(1005, '2023-10-31')
    insert_crime(1006, '2023-11-01')
    insert_crime(1007, '2023-11-02')
    insert_crime(1008, '2023-11-03')
    insert_crime(1009, '2023-11-04')
    insert_crime(1010, '2023-11-05')
    #insert_category
    insert_category(1, 'Robbery')
    insert_category(2, 'Assault')
    insert_category(3, 'Burglary')
    insert_category(4, 'Vandalism')
    insert_category(5, 'Drug Possession')
    #insert_categorize1
    insert_categorize1(1000,1)
    insert_categorize1(1001,2)
    insert_categorize1(1002,3)
    insert_categorize1(1003,4)
    insert_categorize1(1004,5)
    insert_categorize1(1005,1)
    insert_categorize1(1006,2)
    insert_categorize1(1007,3)
    insert_categorize1(1008,4)
    insert_categorize1(1009,5)
    #nothing