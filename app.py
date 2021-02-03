# all imports
from flask import render_template, redirect, g, flash, url_for, session, request
from Manager import app
from Manager.form import Login
from Manager.validation import validateUser
import time
from datetime import datetime, date
# base root director(index page)


@app.route("/", methods=['GET', 'POST'])
def home():
    return redirect(url_for('login'))

# login page directory


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = Login()
    if form.validate_on_submit():
        session.pop('user', None)
        session.pop('role', None)
        username = form.username.data
        password = form.password.data
        validate = validateUser(username, password)
        validate = validate.validateNow()
        if validate == "error1":
            flash("Employee Does Not Exist! Contact Admin", "error")
        elif validate == "error2":
            flash(f"Password Did Not Match", "error")
        elif validate == "error3":
            flash("Profile Locked", "error")
        else:
            session['user'] = validate['username']
            session['role'] = validate['role']
            return redirect(url_for("dashboard"))

    return render_template("login.html", form=form)


# logout page
@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for("login"))


# dashboard page
@app.route("/dashboard", methods=['GET', 'POST'])
def dashboard():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        return render_template("dashboard.html", username=g.user, role=g.role, date=date, time=time)
    else:
        return redirect(url_for("unauthenticated"))


# unauthenticated url access deny
@app.route("/unauthenticated", methods=['GET', 'POST'])
def unauthenticated():
    return render_template("unauth.html")
# 404 error handel


@app.errorhandler(404)
def notFound(e):
    return render_template('404.html')


# global user details as g
@ app.before_request
def before_request_func():
    g.user = None
    if 'user' in session:
        g.user = session['user']
        g.role = session['role']


# send time endpoint
@app.route("/gettime", methods=['GET', 'POST'])
def gettime():
    time = datetime.now()
    time = time.strftime("%H:%M:%S")
    if request.method == "POST":
        data = request.form.get("data")
        if data == "gettime":
            return str(time)


if __name__ == "__main__":
    app.run(debug=True)
