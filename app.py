
from flask import Flask, render_template, json, redirect
from flask_mysqldb import MySQL
from flask import request
import os

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
    query = "DELETE FROM Gyms where id = '%s';"
    cur = mysql.connection.cursor()
    cur.execute(query, (id,)) 
    mysql.connection.commit() 

    #redirect back to gyms page 
    return redirect("/gyms") 

if __name__ == "__main__":
    app.run(port = 5280, debug = True)
