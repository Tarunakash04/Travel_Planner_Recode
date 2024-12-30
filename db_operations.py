import mysql.connector

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="RootUser@123",
        database="travel"
    )

def get_flights_by_route(destination):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM flights WHERE to_location = %s
    """, (destination,))
    flights = cursor.fetchall()
    cursor.close()
    conn.close()
    return flights

def get_all_plans():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM travelplans")
    plans = cursor.fetchall()
    cursor.close()
    conn.close()
    return plans

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

def update_plan_with_flight(destination, flight_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE travelplans
        SET flight_id = %s
        WHERE destination = %s
    """, (flight_id, destination))
    conn.commit()
    cursor.close()
    conn.close()
