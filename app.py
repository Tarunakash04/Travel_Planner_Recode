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

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/view_plans')
def view_plans():
    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM travelplans")
    plans = cursor.fetchall()
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_plans.html', plans=plans, flights=flights)

@app.route('/plan_travel', methods=['GET', 'POST'])
def plan_travel():
    if request.method == 'POST':
        # Collect travel details from the form
        destination = request.form['destination']
        departure_date = request.form['departure_date']
        return_date = request.form['return_date']
        
        # Save the travel plan to the database
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO travelplans (destination, departure_date, return_date)
            VALUES (%s, %s, %s)
        """, (destination, departure_date, return_date))
        conn.commit()
        cursor.close()
        conn.close()

        # Redirect to the flight booking page with the destination
        return redirect(url_for('flight_booking', destination=destination))
    return render_template('plan_travel.html')

@app.route('/flight_booking', methods=['GET', 'POST'])
def flight_booking():
    # Get the destination passed from the plan_travel or view_plans page
    destination = request.args.get('destination')

    conn = connect_db()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM flights WHERE from_location = %s OR to_location = %s", (destination, destination))
    flights = cursor.fetchall()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        # Get the flight selection from the form
        flight_id = request.form['flight_id']

        # Insert the flight into the travel plan
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE travelplans
            SET flight_id = %s
            WHERE destination = %s AND flight_id IS NULL
        """, (flight_id, destination))
        conn.commit()
        cursor.close()
        conn.close()

        return redirect(url_for('view_plans'))

    return render_template('flight_booking.html', flights=flights, destination=destination)

if __name__ == '__main__':
    app.run(debug=True)
