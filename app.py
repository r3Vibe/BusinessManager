################ all imports ################
from flask import render_template, redirect, g, flash, url_for, session, request
from Manager import app
from Manager.form import Login, productImage
from Manager.validation import validateUser, validateProduct
from Manager.database import dbQuery, updateDb
import time
from datetime import datetime, date

################ home page ################


@app.route("/", methods=['GET', 'POST'])
def home():
    return redirect(url_for('login'))

################  login page ################


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


################ dashboard page ################
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


################ inventory management page ################

# inventory page
@app.route("/inventory", methods=['GET', 'POST'])
def inventory():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        return render_template("inventory.html", username=g.user, role=g.role, date=date, time=time)
    else:
        return redirect(url_for('unauthenticated'))


# inventory page add to master data section
@app.route("/addmasterdata", methods=['GET', 'POST'])
def addmasterdata():
    if g.user:
        form = productImage()
        types = dbQuery().getVarType()
        allCategory = dbQuery().getAllCatg()
        allSeller = dbQuery().getAllvendor()
        if form.validate_on_submit():
            res = validateProduct(form.data)
            validate = res.startValidation()
            if validate == "error1":
                flash("Don't Do That", "error")
            elif validate == "error2":
                flash("You Can Not Upload This File", "error")
            elif validate == "error3":
                flash(
                    "This Product Already In Inventory Place Order From Order Page", "error")
            else:
                res = updateDb().addProduct(form.data)
                if res == "success":
                    flash("New Product Added Successfully", "success")
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        return render_template("add.html", username=g.user, role=g.role, date=date, time=time, form=form, vartype=types, catg=allCategory, seller=allSeller)
    else:
        return redirect(url_for('unauthenticated'))


################ remove session variable and redirect ################
# logout page


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for("login"))


################ redirect if not login ################
# unauthenticated url access deny
@app.route("/unauthenticated", methods=['GET', 'POST'])
def unauthenticated():
    return render_template("unauth.html")

############### api ##############

# get variations endpoint


@app.route("/getvars", methods=['GET', 'POST'])
def getvars():
    if g.user:
        if request.method == 'POST':
            data = request.form.get('data')
            allVars = dbQuery().getAllVars(data)[0]['variations']
            return(allVars)
    else:
        return "PLease Login"

# send time endpoint


@app.route("/gettime", methods=['GET', 'POST'])
def gettime():
    if g.user:
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        if request.method == "POST":
            data = request.form.get("data")
            if data == "gettime":
                return str(time)
    else:
        return "Unauthenticated"


################ Errors ################
# 404 error handel


@app.errorhandler(404)
def notFound(e):
    return render_template('404.html')

################ Session Variables ################
# global user details as g


@ app.before_request
def before_request_func():
    g.user = None
    if 'user' in session:
        g.user = session['user']
        g.role = session['role']


if __name__ == "__main__":
    app.run(debug=True)
