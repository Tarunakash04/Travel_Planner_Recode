import mysql.connector

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
    conn = connect_db()
    cursor = conn.cursor()
    cursor.executemany("""
        INSERT INTO flights (flight_number, airline, from_location, to_location, departure_time, arrival_time)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, [
        ("AA101", "American Airlines", "New York", "London", "2024-12-28 10:00:00", "2024-12-28 18:00:00"),
        ("BA202", "British Airways", "London", "Paris", "2024-12-28 14:00:00", "2024-12-28 15:30:00"),
        ("DL303", "Delta Airlines", "Los Angeles", "Tokyo", "2024-12-29 09:00:00", "2024-12-29 20:00:00"),
        ("UA404", "United Airlines", "San Francisco", "Sydney", "2024-12-30 11:00:00", "2024-12-31 07:00:00"),
        ("AF505", "Air France", "Paris", "New York", "2024-12-28 16:00:00", "2024-12-28 22:00:00"),
        ("LH606", "Lufthansa", "Frankfurt", "Dubai", "2024-12-29 12:00:00", "2024-12-29 20:00:00"),
        ("EK707", "Emirates", "Dubai", "Singapore", "2024-12-28 23:00:00", "2024-12-29 07:00:00"),
        ("SQ808", "Singapore Airlines", "Singapore", "Tokyo", "2024-12-28 19:00:00", "2024-12-28 23:00:00"),
        ("QF909", "Qantas", "Sydney", "Melbourne", "2024-12-29 08:00:00", "2024-12-29 09:30:00"),
        ("NH010", "ANA", "Tokyo", "Osaka", "2024-12-28 17:00:00", "2024-12-28 18:30:00"),
        ("AF111", "Air France", "Paris", "Madrid", "2024-12-29 10:00:00", "2024-12-29 11:30:00"),
        ("BA222", "British Airways", "London", "Dubai", "2024-12-30 12:00:00", "2024-12-30 20:00:00"),
        ("DL333", "Delta Airlines", "Los Angeles", "London", "2024-12-31 15:00:00", "2024-12-31 23:00:00"),
        ("UA444", "United Airlines", "San Francisco", "New York", "2024-12-30 18:00:00", "2024-12-30 22:00:00"),
        ("AF555", "Air France", "Paris", "Rome", "2024-12-28 13:00:00", "2024-12-28 14:30:00"),
        ("LH666", "Lufthansa", "Frankfurt", "London", "2024-12-29 14:00:00", "2024-12-29 16:00:00"),
        ("EK777", "Emirates", "Dubai", "Tokyo", "2024-12-29 21:00:00", "2024-12-30 06:00:00"),
        ("SQ888", "Singapore Airlines", "Singapore", "Los Angeles", "2024-12-30 16:00:00", "2024-12-30 22:00:00"),
        ("QF999", "Qantas", "Sydney", "New York", "2024-12-29 09:00:00", "2024-12-29 14:00:00"),
        ("NH111", "ANA", "Tokyo", "Hong Kong", "2024-12-28 10:00:00", "2024-12-28 12:30:00"),
        ("AF123", "Air France", "Paris", "Los Angeles", "2024-12-30 08:00:00", "2024-12-30 18:00:00"),
        ("BA234", "British Airways", "London", "Singapore", "2024-12-28 07:00:00", "2024-12-28 15:00:00"),
        ("DL345", "Delta Airlines", "Los Angeles", "Paris", "2024-12-31 09:00:00", "2024-12-31 17:00:00"),
        ("UA456", "United Airlines", "San Francisco", "Tokyo", "2024-12-28 21:00:00", "2024-12-29 05:00:00"),
        ("AF567", "Air France", "Paris", "Melbourne", "2024-12-29 12:00:00", "2024-12-29 19:30:00"),
        ("LH678", "Lufthansa", "Frankfurt", "Singapore", "2024-12-28 16:00:00", "2024-12-28 22:30:00"),
        ("EK789", "Emirates", "Dubai", "Sydney", "2024-12-29 18:00:00", "2024-12-30 07:00:00"),
        ("SQ890", "Singapore Airlines", "Singapore", "New York", "2024-12-28 22:00:00", "2024-12-29 06:00:00"),
        ("QF101", "Qantas", "Sydney", "Dubai", "2024-12-28 11:00:00", "2024-12-28 19:00:00"),
        ("NH212", "ANA", "Tokyo", "Los Angeles", "2024-12-29 20:00:00", "2024-12-30 04:30:00"),
        ("AF323", "Air France", "Paris", "Dubai", "2024-12-29 10:00:00", "2024-12-29 18:00:00")
    ])
    conn.commit()
    cursor.close()
    conn.close()

# Create the table and add dummy flights when this script is imported
create_flights_table()
add_dummy_flights()
