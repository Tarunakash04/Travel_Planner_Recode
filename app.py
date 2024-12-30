from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection function
def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="RootUser@123",
        database="travel"
    )

# Get flights by "from", "to", and "departure_date"
def get_flights_by_route(from_location, to_location, departure_date=None):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    if departure_date:
        cursor.execute("""
            SELECT * FROM flights 
            WHERE from_location = %s AND to_location = %s 
            AND DATE(departure_time) = %s
        """, (from_location, to_location, departure_date))
    else:
        cursor.execute("""
            SELECT * FROM flights WHERE from_location = %s AND to_location = %s
        """, (from_location, to_location))

    flights = cursor.fetchall()
    cursor.close()
    conn.close()
    return flights


# Get all travel plans
def get_all_plans():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM travelplans")
    plans = cursor.fetchall()
    cursor.close()
    conn.close()
    return plans

# Add a new travel plan to the database
# Add a new travel plan to the database
def add_plan(from_location, destination, departure_date, return_date):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO travelplans (from_location, destination, departure_date, return_date)
        VALUES (%s, %s, %s, %s)
    """, (from_location, destination, departure_date, return_date))
    conn.commit()
    cursor.close()
    conn.close()

# Update a travel plan with a flight ID after booking
def update_plan_with_flight(plan_id, flight_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE travelplans
        SET flight_id = %s
        WHERE id = %s
    """, (flight_id, plan_id))
    conn.commit()
    cursor.close()
    conn.close()

# Home route
@app.route('/')
def home():
    return render_template('home.html')

# View travel plans route
@app.route('/view_plans')
def view_plans():
    plans = get_all_plans()
    return render_template('view_plans.html', plans=plans)

# Plan a trip route
# Plan a trip route
@app.route('/plan_travel', methods=['GET', 'POST'])
def plan_travel():
    if request.method == 'POST':
        from_location = request.form['from_location']
        destination = request.form['destination']
        departure_date = request.form['departure_date']
        return_date = request.form['return_date']
        add_plan(from_location, destination, departure_date, return_date)
        return redirect(url_for('view_plans'))
    return render_template('plan_travel.html')


# Book a flight for a specific travel plan
@app.route('/book_trip/<int:plan_id>', methods=['GET', 'POST'])
def book_trip(plan_id):
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)

    # Get the travel plan using plan_id
    cursor.execute("SELECT * FROM travelplans WHERE id = %s", (plan_id,))
    plan = cursor.fetchone()

    if plan is None:
        # If no plan was found for the given plan_id
        return "Plan not found", 404

    # Get the user input (from_location, to_location, departure_date)
    if request.method == 'POST':
        from_location = request.form['from_location']
        to_location = request.form['to_location']
        departure_date = request.form['departure_date']
        
        # Get flights for the provided locations and date
        flights = get_flights_by_route(from_location, to_location, departure_date)

        # If no flights are found, return an error or handle appropriately
        if not flights:
            return "No flights found for the selected criteria.", 404

        # Proceed with the booking logic here (e.g., selecting a flight, etc.)
        flight_id = request.form.get('flight_id')

        # Update the travel plan with the selected flight ID
        update_plan_with_flight(plan['destination'], flight_id)

        # Redirect to view_plans page after booking
        return redirect(url_for('view_plans'))

    cursor.close()
    conn.close()

    # Initial flight listing when GET request is made
    flights = get_flights_by_route(plan['from_location'], plan['destination'], plan['departure_date'])
    return render_template('book_trip.html', flights=flights, plan=plan)


if __name__ == '__main__':
    app.run(debug=True)
