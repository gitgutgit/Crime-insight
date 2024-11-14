import psycopg2
import toml
config = toml.load("secrets.toml")
DB_URL = config["database"]["DB_URL"]

def reset_database():
    conn = psycopg2.connect(DB_URL)
    cursor = conn.cursor()

    # delete previous table
    drop_commands = [
        "DROP TABLE IF EXISTS Report CASCADE",
        "DROP TABLE IF EXISTS Categorize1 CASCADE",
        "DROP TABLE IF EXISTS Categorize2 CASCADE",
        "DROP TABLE IF EXISTS Commited_by CASCADE",
        "DROP TABLE IF EXISTS Place_Lives_in CASCADE",
        "DROP TABLE IF EXISTS Criminal CASCADE",
        "DROP TABLE IF EXISTS Category CASCADE",
        "DROP TABLE IF EXISTS Crime CASCADE",
        "DROP TABLE IF EXISTS Users CASCADE"
    ]

    for command in drop_commands:
        cursor.execute(command)

    # create all tables
    create_commands = [
        """
        CREATE TABLE IF NOT EXISTS Crime (
            Crime_id SERIAL PRIMARY KEY,
            Crime_date DATE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Category (
            Category_id SERIAL PRIMARY KEY,
            Category_name TEXT UNIQUE NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Categorize1 (
            Crime_id INTEGER REFERENCES Crime(Crime_id) ON DELETE CASCADE,
            Category_id INTEGER REFERENCES Category(Category_id) ON DELETE CASCADE,
            PRIMARY KEY (Crime_id, Category_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Criminal (
            Criminal_id SERIAL PRIMARY KEY,
            Criminal_name TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Commited_by (
            Crime_id INTEGER REFERENCES Crime(Crime_id) ON DELETE CASCADE,
            Criminal_id INTEGER REFERENCES Criminal(Criminal_id) ON DELETE CASCADE,
            PRIMARY KEY (Crime_id, Criminal_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Categorize2 (
            Criminal_id INTEGER REFERENCES Criminal(Criminal_id) ON DELETE CASCADE,
            Category_id INTEGER REFERENCES Category(Category_id) ON DELETE CASCADE,
            PRIMARY KEY (Criminal_id, Category_id)
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Place_Lives_in (
            Place_id SERIAL PRIMARY KEY,
            Street_address TEXT NOT NULL,
            Post_code INTEGER NOT NULL,
            State TEXT NOT NULL,
            Gender TEXT NOT NULL,
            Criminal_id INTEGER REFERENCES Criminal(Criminal_id) ON DELETE CASCADE
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Users (
            User_id SERIAL PRIMARY KEY,
            User_name TEXT NOT NULL,
            User_email TEXT NOT NULL
        );
        """,
        """
        CREATE TABLE IF NOT EXISTS Report (
            User_id INTEGER REFERENCES Users(User_id) ON DELETE CASCADE,
            Crime_id INTEGER REFERENCES Crime(Crime_id) ON DELETE CASCADE,
            Report_date DATE NOT NULL,
            Report_details TEXT,
            PRIMARY KEY (User_id, Crime_id)
        );
        """
    ]

    for command in create_commands:
        cursor.execute(command)

    # # start with 1000
    # cursor.execute("ALTER SEQUENCE crime_crime_id_seq RESTART WITH 1000;")

    conn.commit()
    cursor.close()
    conn.close()
    print("All tables dropped, recreated successfully, and Crime_id sequence set to start at 1000.")

# 함수 실행
if __name__ == "__main__":
    reset_database()
