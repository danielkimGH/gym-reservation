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

        # Query to grab gym location for dropdown
        # query2 = "select id, location from Gyms"
        # cur = mysql.connection.cursor()
        # cur.execute(query2)
        # gym_location_data = cur.fetchall()

        # return render_template("gyms.j2", data = data, gym_location = gym_location_data)
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
def edit_people(id):
    if request.method == 'GET':
        #mySQL query to grab the info of the person w/our passed id 
        query = "SELECT * from Gyms where gym_ID = %s" % (id) 
        cur = mysql.connection.cursor()
        cur.execute(query)
        data = cur.fetchall() 
    
    # dropdowwn code here 

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


if __name__ == "__main__":
    app.run(port = 5282, debug = True) 
    # 5282 is for development / 5280 is for submission 
    # port 5280 was for the Proj step 4 submission. Make sure to start the app there when done.
    # you can also run app.py (change the port#) to have it run on local machine so that you don't have to kill gunicorn 
    # and re-run each time to show changes 
