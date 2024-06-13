import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from helpers import apology, login_required, lookup, usd,days_to_date
from flask import jsonify

# Configure application
app = Flask(__name__)

# Custom filter
app.jinja_env.filters["usd"] = usd

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///data.db")




@app.after_request
def after_request(response):
    """Ensure responses aren't cached"""
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/clock")
@login_required
def timer():
    """Show portfolio of stocks"""
    if request.method == "GET":
        info = db.execute("SELECT * FROM timers WHERE userid = ? ", session.get("user_id"))
        info_t = db.execute("SELECT * FROM trackers WHERE userid = ? ", session.get("user_id"))

        return render_template("my_timer.html",info=info,info_t =info_t)
    return apology("TODO")

@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Show portfolio of stocks"""
    if request.method == "GET":
        return render_template("index.html")
    if request.method == "POST":
        if request.form.get("action") == "add_timer":
            return redirect("/add_timer")
        elif request.form.get("action") == "add_event":
            return redirect("/add_event")
        elif request.form.get("action") == "add_task":
            return redirect("/add_task")

    return apology("TODO")


@app.route("/add_timer", methods=["GET", "POST"])
@login_required
def add_timer():
    """Show portfolio of stocks"""
    if request.method == "GET":
        return render_template("add_timer.html")
    if request.method == "POST":
        title = request.form.get("title")
        hours = request.form.get("hours")
        number = request.form.get("minutes")
        db.execute("INSERT INTO trackers (userid, title, hours, minutes,rhours,rminutes,start_time,end_time) values(?,?,?,?,?,?,?,?)",
                   session.get("user_id"),title,hours,number,hours,number,"1234-01-01","1234-01-01")
        db.execute("INSERT INTO timers (userid, title, hours, minutes,rhours,rminutes) values(?,?,?,?,?,?)",
                   session.get("user_id"),title,hours,number,hours,number)

        return redirect("/clock")

    return apology("TODO")

@app.route("/update_timer", methods=["POST"])
@login_required
def update_timer():
    """Update timer in database"""
    data = request.json
    hours = data.get("hours")
    minutes = data.get("minutes")
    title = data.get("title")

    # Update timer in database
    db.execute("UPDATE timers SET hours = ?, minutes = ? WHERE userid = ? AND title = ?",
               hours, minutes, session.get("user_id"),title)
    db.execute("UPDATE trackers SET hours = ?, minutes = ? WHERE userid = ? AND title = ?",
               hours, minutes, session.get("user_id"),title)
    Hours = db.execute("SELECT rhours FROM trackers WHERE userid = ? AND title = ?",
                       session.get("user_id"),title)
    Minutes = db.execute("SELECT rminutes FROM trackers WHERE userid = ? AND title = ?",
                       session.get("user_id"),title)
    Date = db.execute("SELECT end_time FROM trackers WHERE userid = ? AND title = ?",
                       session.get("user_id"),title)
    Date = days_to_date(Date[0]["end_time"][:10])
    if Minutes:
        Hours = int(Hours[0]["rhours"])
        Minutes = int(Minutes[0]["rminutes"])
        p = (1.00 - (hours*60 + minutes)/(Hours*60 + Minutes))
        p = round(p*100,2)
        db.execute("UPDATE trackers SET progress = ? WHERE userid = ? AND title = ?",
                   p, session.get("user_id"),title)
        db.execute("UPDATE trackers SET left = ? WHERE userid = ? AND title = ?",
                   Date, session.get("user_id"),title)

    return jsonify(success=True)

@app.route("/add_task", methods=["GET", "POST"])
@login_required
def add_task():
    if request.method == "GET":
        return render_template("add_task.html")
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        hours = request.form.get("hours")
        minutes = request.form.get("minutes")

        db.execute("INSERT INTO trackers (userid, title, description, start_time, end_time,rhours,rminutes,hours,minutes) VALUES (?, ?, ?, ?, ?, ?, ?,?,?)",
                   session.get("user_id"), title, description, start_time, end_time, hours, minutes,hours,minutes)
        Hours = db.execute("SELECT rhours FROM trackers WHERE userid = ? AND title = ?",
                       session.get("user_id"),title)
        Minutes = db.execute("SELECT rminutes FROM trackers WHERE userid = ? AND title = ?",
                        session.get("user_id"),title)
        Date = db.execute("SELECT end_time FROM trackers WHERE userid = ? AND title = ?",
                        session.get("user_id"),title)
        Date = days_to_date(Date[0]["end_time"][:10])
        if Minutes:
            Hours = int(Hours[0]["rhours"])
            Minutes = int(Minutes[0]["rminutes"])
            p = (1.00 - (int(hours)*60 + int(minutes))/(Hours*60 + Minutes))
            p = round(p*100,2)
            db.execute("UPDATE trackers SET progress = ? WHERE userid = ? AND title = ?",
                    p, session.get("user_id"),title)
            db.execute("UPDATE trackers SET left = ? WHERE userid = ? AND title = ?",
                    Date, session.get("user_id"),title)

        return redirect("/progress_tracker")

@app.route("/add_event", methods=["GET", "POST"])
@login_required
def add_event():
    if request.method == "GET":
        return render_template("add_event.html")
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        db.execute("INSERT INTO calendars (userid, title, description, start_time, end_time) VALUES (?, ?, ?, ?, ?)",
                   session.get("user_id"), title, description, start_time, end_time)
        db.execute("INSERT INTO trackers (userid, title, description, start_time, end_time) VALUES (?, ?, ?, ?, ?)",
                   session.get("user_id"), title, description, start_time, end_time)
        Date = db.execute("SELECT end_time FROM trackers WHERE userid = ? AND title = ?",
                        session.get("user_id"),title)
        Date = days_to_date(Date[0]["end_time"][:10])
        db.execute("UPDATE trackers SET left = ? WHERE userid = ? AND title = ?",
                    Date, session.get("user_id"),title)


        return redirect("/calendar")


@app.route("/progress_tracker" , methods=["GET", "POST"])
@login_required
def progress_tracker():
    if request.method == "GET":
        tasks = db.execute("SELECT * FROM trackers WHERE userid = ?", session.get("user_id"))
        return render_template("progress_tracker.html", tasks = tasks)
    if request.method == "POST":
        if request.form.get("action") == "add_task":
            return redirect("/add_task")


# View Calendar Events
@app.route("/calendar")
@login_required
def calendar():
    if request.method == "GET":
        events = db.execute("SELECT * FROM calendars WHERE userid = ?", session.get("user_id"))
        return render_template("calendar.html", events=events)
    if request.method == "POST":
        if request.form.get("action") == "add_event":
            return redirect("/add_event")

# Update Calendar Event
@app.route("/update_task/<int:task_id>", methods=["GET", "POST"])
@login_required
def update_task(task_id):
    if request.method == "GET":
        task = db.execute("SELECT * FROM trackers WHERE id = ? AND userid = ?", task_id, session.get("user_id"))
        if not task:
            return apology("Event not found", 404)
        return render_template("update_task.html", task=task[0])
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")
        minutes = request.form.get("minutes")
        hours = request.form.get("hours")

        db.execute("UPDATE trackers SET title = ?, description = ?, start_time = ?, end_time = ?,minutes = ?, hours= ?,rhours=?,rminutes=? WHERE id = ? AND userid = ?",
                   title, description, start_time, end_time,minutes,hours,hours , minutes, task_id, session.get("user_id"))

        return redirect("/progress_tracker")

@app.route("/update_event/<int:event_id>", methods=["GET", "POST"])
@login_required
def update_event(event_id):
    if request.method == "GET":
        event = db.execute("SELECT * FROM calendars WHERE id = ? AND userid = ?", event_id, session.get("user_id"))
        if not event:
            return apology("Event not found", 404)
        return render_template("update_event.html", event=event[0])
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        start_time = request.form.get("start_time")
        end_time = request.form.get("end_time")

        db.execute("UPDATE calendars SET title = ?, description = ?, start_time = ?, end_time = ? WHERE id = ? AND userid = ?",
                   title, description, start_time, end_time, event_id, session.get("user_id"))

        return redirect("/calendar")

# Delete Calendar Event
@app.route("/delete_task/<int:task_id>", methods=["POST"])
@login_required
def delete_task(task_id):
    db.execute("DELETE FROM trackers WHERE id = ? AND userid = ?", task_id, session.get("user_id"))
    return redirect("/progress_tracker")

@app.route("/delete_event/<int:event_id>", methods=["POST"])
@login_required
def delete_event(event_id):
    db.execute("DELETE FROM calendars WHERE id = ? AND userid = ?", event_id, session.get("user_id"))
    return redirect("/calendar")

@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", request.form.get("username")
        )

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(
            rows[0]["hash"], request.form.get("password")
        ):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()


    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":
        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 400)
        if not request.form.get("password"):
            return apology("must provide password", 400)
        if not request.form.get("confirmation"):
            return apology("must provide password", 400)
        Username = request.form.get("username")
        Password = request.form.get("password")
        Password2 = request.form.get("confirmation")
        rows = db.execute(
            "SELECT * FROM users WHERE username = ?", Username
        )
        if rows:
            return apology("username exists")
        if not Password == Password2:
            return apology("passwords do not match")
        Password_hash = generate_password_hash(Password, method='scrypt', salt_length=16)
        db.execute("INSERT INTO users (username, hash) VALUES (?, ?)", Username,Password_hash )
        return redirect("/login")
    if request.method == "GET":
        return render_template("register.html")

    return apology("TODO")


