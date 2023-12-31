import os

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///birthdays.db")


@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response

@app.route("/", methods=["GET", "POST"])
def index():
    bd = db.execute("SELECT * FROM birthdays ORDER BY id DESC;")
    monthList = ["January", "February", "March", "April", "May",
                 "June", "July", "August", "September", "October", "November", "December"]
    if request.method == "POST":

        # TODO: Add the user's entry into the database
        name = request.form.get("name")
        month = monthList[int(request.form.get("month")) - 1]
        day = request.form.get("day")

        db.execute("INSERT INTO birthdays (name, month, day) VALUES (?, ?, ?);", name, month, day)
        return redirect("/")

    else:

        # TODO: Display the entries in the database on index.html

        return render_template("index.html", birthdays=bd)

@app.route("/remove", methods=["POST"])
def remove():
    id = request.form.get("id")
    if id:
        db.execute("DELETE FROM birthdays WHERE id = (?)", id)
        return redirect("/")

if __name__ == '__main__':
    app.run(debug=True, port=8000)