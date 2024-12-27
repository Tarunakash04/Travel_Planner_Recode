import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="RootUser@123",
        database="travel"
    )

def create_travelplans_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS travelplans (
            id INT AUTO_INCREMENT PRIMARY KEY,
            destination VARCHAR(100) NOT NULL,
            departure_date DATE NOT NULL,
            return_date DATE NOT NULL,
            flight_id INT,
            FOREIGN KEY (flight_id) REFERENCES flights(id)
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def add_plan(destination, departure_date, return_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO travelplans (destination, departure_date, return_date)
        VALUES (%s, %s, %s)
    """, (destination, departure_date, return_date))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_plans():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM travelplans")
    plans = cursor.fetchall()
    cursor.close()
    conn.close()
    return plans
