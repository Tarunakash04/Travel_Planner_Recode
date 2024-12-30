import mysql.connector
from random import choice
from datetime import datetime, timedelta

def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="RootUser@123",
        database="travel"
    )

def create_flights_table():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS flights (
            id INT AUTO_INCREMENT PRIMARY KEY,
            flight_number VARCHAR(20) NOT NULL,
            airline VARCHAR(50) NOT NULL,
            from_location VARCHAR(100) NOT NULL,
            to_location VARCHAR(100) NOT NULL,
            departure_time DATETIME NOT NULL,
            arrival_time DATETIME NOT NULL
        )
    """)
    conn.commit()
    cursor.close()
    conn.close()

def get_flights_by_route(destination):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT * FROM flights
        WHERE to_location = %s
    """, (destination,))
    flights = cursor.fetchall()
    cursor.close()
    conn.close()
    return flights

def add_dummy_flights():
    airlines = [
        "American Airlines", "British Airways", "Delta Airlines", "United Airlines",
        "Air France", "Lufthansa", "Emirates", "Singapore Airlines", "Qantas", "ANA"
    ]
    locations = [
        ("New York", "London"), ("London", "Paris"), ("Los Angeles", "Tokyo"), 
        ("San Francisco", "Sydney"), ("Paris", "New York"), ("Frankfurt", "Dubai"),
        ("Dubai", "Singapore"), ("Singapore", "Tokyo"), ("Sydney", "Melbourne"),
        ("Tokyo", "Osaka"), ("Paris", "Madrid"), ("London", "Dubai"),
        ("Los Angeles", "London"), ("San Francisco", "New York"), ("Paris", "Rome"),
        ("Frankfurt", "London"), ("Dubai", "Tokyo"), ("Singapore", "Los Angeles"),
        ("Sydney", "New York"), ("Tokyo", "Hong Kong"), ("Paris", "Los Angeles")
    ]
    
    flights_data = []
    base_date = datetime(2024, 12, 28)

    for i in range(150):
        airline = choice(airlines)
        from_location, to_location = choice(locations)
        departure_time = base_date + timedelta(hours=i % 24, minutes=(i % 60) * 30)
        arrival_time = departure_time + timedelta(hours=8, minutes=30)  # Assuming an average flight duration
        flight_number = f"{choice(['AA', 'BA', 'DL', 'UA', 'AF', 'LH', 'EK', 'SQ', 'QF', 'NH'])}{100 + i}"
        
        flights_data.append((flight_number, airline, from_location, to_location, departure_time.strftime('%Y-%m-%d %H:%M:%S'), arrival_time.strftime('%Y-%m-%d %H:%M:%S')))

    conn = connect_db()
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO flights (flight_number, airline, from_location, to_location, departure_time, arrival_time)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, flights_data)
    conn.commit()
    cursor.close()
    conn.close()

# Create the table and add dummy flights when this script is imported
create_flights_table()
add_dummy_flights()
