# Date: 11/16/2023
# Adapted from
# Source URL: https://github.com/osu-cs340-ecampus/flask-starter-app/blob/master/bsg_people_app/app.py
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os
from flask import flash

app = Flask(__name__)

# Database connection information

# Uncomment below for DK 
# app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
# app.config["MYSQL_USER"] = "cs340_kimda6"
# app.config["MYSQL_PASSWORD"] = "2371"
# app.config["MYSQL_DB"] = "cs340_kimda6"
# app.config["MYSQL_CURSORCLASS"] = "DictCursor"

# Uncomment below for Brian 
app.config["MYSQL_HOST"] = "classmysql.engr.oregonstate.edu"
app.config["MYSQL_USER"] = "cs340_hsiangb"
app.config["MYSQL_PASSWORD"] = "2174"
app.config["MYSQL_DB"] = "cs340_hsiangb"
app.config["MYSQL_CURSORCLASS"] = "DictCursor"

mysql = MySQL(app)

# Routes
# Homepage route to /gyms by default
@app.route("/")
def home():
    return redirect("/gyms")

# Route for Gyms page
@app.route("/gyms", methods = ["POST", "GET"])
def gyms():

    # Retrieve and display the data
    if request.method == "GET":
        # Query to get all information in Gyms entity (gym_ID, location, email, opening/closing time)
        query = "select * from Gyms"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("gyms.j2", data = data)

    # Add a new gym
    if request.method == "POST":
        # Add gym button is selected, get user input
        if request.form.get("Add_Gym"):
            location = request.form["location"]
            email = request.form["email"]
            opening_time = request.form["opening_time"]
            closing_time = request.form["closing_time"]

            query = "insert into Gyms(location, email, opening_time, closing_time) values (%s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (location, email, opening_time, closing_time))
            mysql.connection.commit()

            # Redirect back to Gyms page
            return redirect("/gyms")

@app.route("/delete_gym/<int:id>")
def delete_gym(id):
    #mySQL query to delete the gym with our passed id
    query = "DELETE FROM Gyms where gym_ID = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,)) 
    mysql.connection.commit() 

    #redirect back to gyms page 
    return redirect("/gyms") 

@app.route("/edit_gym/<int:id>", methods=["POST", "GET"])
def edit_gym(id):
    if request.method == 'GET':
        #mySQL query to grab the info of the person w/our passed id 
        query = "SELECT * from Gyms where gym_ID = %s" % (id) 
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("edit_gyms.j2", data=data)
    
    #the 'meat and potatoes' of our update functionality
    if request.method == 'POST': 
        #fire off if user clicks the Edit Person button
        if request.form.get("edit_gym"): 
            #grab user form inputs 
            id = request.form["gym_ID"]
            location = request.form["location"]
            email = request.form["email"]
            opening_time = request.form["opening_time"]
            closing_time = request.form["closing_time"] 

            #for testing purposes, do not put NULL for any of the input.
            query = "UPDATE Gyms SET Gyms.location = %s, Gyms.email = %s, Gyms.opening_time = %s, Gyms.closing_time = %s where gym_ID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (location, email, opening_time, closing_time, id))
            mysql.connection.commit() 
            
        return redirect("/gyms")


# Route for Members page
@app.route("/members", methods = ["POST", "GET"])
def members():
    if request.method == "GET":
        query = "select * from Members"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        return render_template("members.j2", data=data)


    if request.method == 'POST': 
        if request.form.get("Add_Member"): 
            first_name =request.form["first_name"]
            last_name = request.form["last_name"]
            age = request.form["age"]
            email = request.form["email"]
            gender = request.form["gender"]

            query = "insert into Members (first_name, last_name, age, email, gender) values (%s, %s, %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, age, email, gender))
            mysql.connection.commit()

            return redirect("/members")
        
@app.route("/delete_member/<int:id>")
def delete_member(id):
    query = "DELETE from Members where member_ID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/members")
        
@app.route("/edit_member/<int:id>", methods=["POST", "GET"])
def edit_member(id):
    if request.method == 'GET':
        query = "SELECT * from Members where member_ID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall() 

        return render_template("edit_members.j2", data=data)


    if request.method == 'POST':
        if request.form.get("edit_member"):
            id = request.form["member_ID"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            age = request.form['age']
            email = request.form['email']
            gender = request.form['gender']

            query = "update Members SET Members.first_name = %s, Members.last_name = %s, Members.age = %s, Members.email = %s, Members.gender = %s where member_ID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (first_name, last_name, age, email, gender, id))
            mysql.connection.commit() 

        return redirect("/members")


# Route for Courts page
@app.route("/courts", methods = ["POST", "GET"])
def courts():
    if request.method == "GET":
        query = "select * from Courts order by gym_ID asc"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Query to get a dropdown list of gym locations
        query2 = "select gym_ID, location from Gyms"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gym_location_data = cur.fetchall()

        return render_template("courts.j2", data=data, locations=gym_location_data)

    if request.method == 'POST': 
        if request.form.get("Add_Court"): 
            gym_ID =request.form["gym_ID"]
            court_name = request.form["court_name"]

            query = "insert into Courts (gym_ID, court_name) values (%s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (gym_ID, court_name))
            mysql.connection.commit()

            return redirect("/courts")

@app.route("/edit_court/<int:id>", methods=["POST", "GET"])
def edit_court(id):
    if request.method == 'GET':
        # SQL query to get info of Courts from court ID
        query = "SELECT * from Courts where court_ID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall() 

        # SQL query to get dropdown of gym locations
        query2 = "SELECT gym_ID, location from Gyms"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gym_location_data = cur.fetchall()

        # Return edit_courts page passing query data and gym location data to the edit_courts page
        return render_template("edit_courts.j2", data=data, locations=gym_location_data)

    if request.method == "POST":
        if request.form.get("edit_court"):
            id = request.form["court_ID"]
            court_name = request.form["court_name"]

            query = "update Courts set Courts.court_name = %s where court_ID = %s"
            cur = mysql.connection.cursor()
            cur.execute(query, (court_name, id))
            mysql.connection.commit()

        return redirect("/courts")

@app.route("/delete_court/<int:id>")
def delete_court(id):
    query = "DELETE from Courts where court_ID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/courts")

@app.route("/gymmemberships", methods = ["POST", "GET"])
def gymmemberships(): 
    if request.method == "GET":
        query = "select * from GymMemberships" 
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        #query to get the dropdown list of gym locations 
        query2 = "select gym_ID, location from Gyms"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        gym_location_data = cur.fetchall()
        
        return render_template("gymmemberships.j2", data=data, locations=gym_location_data)
    
    if request.method == "POST":
        if request.form.get("add_gymmembership"):
            gym_ID = request.form["gym_ID"]
            paid = request.form["payment_status"]

            first_name = request.form["first_name"]
            last_name = request.form["last_name"]

        query = "insert into GymMemberships (gym_ID, member_ID, gym_memberships_ID, paid) values (%s, (SELECT member_ID from Members where first_name = %s and last_name = %s), %s, %s)"
        cur = mysql.connection.cursor()
        cur.execute(query, (gym_ID, paid, first_name, last_name))
        mysql.connection.commit()

        return redirect("/gymmemberships")
            
    
@app.route("/edit_gymmembership/<int:id>", methods=["POST", "GET"])
def edit_gm(id):
    if request.method == 'GET':
        query = "SELECT * from GymMemberships where gym_memberships_ID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        query_show_person = "SELECT Members.first_name, Members.last_name from Members INNER JOIN GymMemberships on GymMemberships.member_ID = Members.member_ID where Members.member_ID = %s group by first_name" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query_show_person)
        data2 = cur.fetchall()

        return render_template("edit_gymmemberships.j2", data=data, data2=data2)
    
    if request.method == 'POST':
        # if request.form.get("edit_gymmembership"):
        id = request.form["gym_memberships_ID"]
        paid = request.form["payment_status"]

        query = "update GymMemberships SET GymMemberships.paid=%s where gym_memberships_ID = %s"
        cur = mysql.connection.cursor()
        cur.execute(query, (paid, id))
        mysql.connection.commit()

        return redirect("/gymmemberships") 

@app.route("/delete_gymmembership/<int:id>")
def delete_gm(id):
    query = "DELETE from GymMemberships where gym_memberships_ID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))   #putting , after id makes a difference here as tuple stays iterable with the , placed
    mysql.connection.commit()

    return redirect("/gymmemberships")
    
@app.route("/display_gymmembership/<int:gym_id>", methods=["POST", "GET"])
def display_gymmembership(id):
    if request.method == 'GET':
        query = "SELECT member_ID from GymMemberships where gym_ID = %s" % (id) 
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall() 

    return render_template("display_gymmemberships.j2", data=data)


# Route for Reservations page
@app.route("/reservations", methods = ["POST", "GET"])
def reservations():
    if request.method == "GET":
        query = "select * from Reservations"
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall()

        # Query to get a dropdown list of court ID and court names
        query2 = "select court_ID, court_name from Courts"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        court_name_data = cur.fetchall()

        return render_template("reservations.j2", data=data, court_name=court_name_data)

    if request.method == 'POST': 
        if request.form.get("add_reservation"): 
            court_ID =request.form["court_ID"]
            first_name = request.form["first_name"]
            last_name = request.form["last_name"]
            reservation_start = request.form["reservation_start"]
            reservation_end = request.form["reservation_end"]
            paid = request.form["paid"]

            query = "insert into Reservations (court_ID, member_ID, reservation_start, reservation_end, paid) values (%s, (SELECT member_ID FROM Members WHERE first_name = %s AND last_name = %s), %s, %s, %s)"
            cur = mysql.connection.cursor()
            cur.execute(query, (court_ID, first_name, last_name, reservation_start, reservation_end, paid))
            mysql.connection.commit()

            return redirect("/reservations")

# Route to edit reservation
@app.route("/edit_reservation/<int:id>", methods=["POST", "GET"])
def edit_reservation(id):
    if request.method == 'GET':
        # SQL query to get info of Reservations from reservation ID
        query = "SELECT * from Reservations where reservation_ID = %s" % (id)
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall() 

        # Query to get a dropdown list of court ID and court names
        query2 = "select court_ID, court_name from Courts"
        cur = mysql.connection.cursor()
        cur.execute(query2)
        court_name_data = cur.fetchall()

        # Return edit_Reservations page passing query data and court name data to the edit_reservations page
        return render_template("edit_reservations.j2", data=data, court_name=court_name_data)

    if request.method == "POST":
        if request.form.get("edit_reservation"):
            reservation_ID = request.form["reservation_ID"]
            court_ID = request.form["court_ID"]
            reservation_start = request.form["reservation_start"]
            reservation_end = request.form["reservation_end"]
            paid = request.form["paid"]

            # If "Cancel Reservation" (value of 0) is selected on the reserved court, it will set the court_ID (foreign key) to NULL
            if court_ID == "0":
                query = "Update Reservations set Reservations.court_ID = NULL, Reservations.reservation_start=%s, Reservations.reservation_end=%s, Reservations.paid=%s where Reservations.reservation_ID=%s"
                cur = mysql.connection.cursor()
                cur.execute(query, (reservation_start, reservation_end, paid, reservation_ID))
                mysql.connection.commit()
            else:
                query = "Update Reservations set Reservations.court_ID = %s, Reservations.reservation_start=%s, Reservations.reservation_end=%s, Reservations.paid=%s where Reservations.reservation_ID=%s"
                cur = mysql.connection.cursor()
                cur.execute(query, (court_ID, reservation_start, reservation_end, paid, reservation_ID))
                mysql.connection.commit()

        return redirect("/reservations")

# Route to delete reservation
@app.route("/delete_reservation/<int:id>")
def delete_reservation(id):
    query = "DELETE from Reservations where reservation_ID = %s;"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,))
    mysql.connection.commit()

    return redirect("/reservations")

if __name__ == "__main__":
    app.run(port = 5287, debug = True) 
    # Use local (specify port above^) or use 5282 for development / 5280 is for submission 
    # port 5280 was for the Proj step 4 submission. Make sure to start the app there when done.
    # you can also run app.py (change the port# i,e. to 5281) to have it run on local machine so that you don't have to kill gunicorn 
    # and re-run each time to show changes 