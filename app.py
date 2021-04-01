################ all imports ################
from flask import render_template, redirect, g, flash, url_for, session, request
from Manager import app
from Manager.form import Login, productImage
from Manager.validation import validateUser, validateProduct
from Manager.database import dbQuery, updateDb
import time
from datetime import datetime, date
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import uuid

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
# place order page
@app.route("/placeorder", methods=['GET', 'POST'])
def placeorder():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        allProduct = dbQuery().getProducts()
        allVendor = dbQuery().getAllvendor()
        return render_template("placeorder.html", username=g.user, role=g.role, date=date, time=time, product=allProduct, vendor=allVendor)
    else:
        return redirect(url_for('unauthenticated'))

# inventory page


@app.route("/inventory", methods=['GET', 'POST'])
def inventory():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        if request.method == "POST":
            specificProduct = dbQuery().getSpeProducts(request.form.get('search'))
            return render_template("inventory.html", username=g.user, role=g.role, date=date, time=time, products=specificProduct)
        allProduct = dbQuery().getProducts()
        return render_template("inventory.html", username=g.user, role=g.role, date=date, time=time, products=allProduct)
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
        if request.method == "POST":
            res = validateProduct(request.form, request.files)
            validate = res.startValidation()
            if validate == "error1":
                flash("Don't Do That", "error")
            elif validate == "error2":
                flash("You Can Not Upload This File", "error")
            elif validate == "error3":
                flash(
                    "This Product Already In Inventory Place Order From Order Page", "error")
            else:
                # upload image first
                extinsion = request.files['image'].filename.rsplit('.')
                originalFilename = extinsion[0]
                extinsion = extinsion[1].lower()
                rootPath = os.path.join(
                    app.root_path, 'static', 'uploads')
                newname = str(uuid.uuid4().hex)+'.'+str(extinsion)
                destination = "/".join([rootPath, newname])
                try:
                    request.files['image'].save(destination)
                except Exception as e:
                    flash("Unable To Upload Product Image. Contact Admin", "error")
                else:
                    # update database with new product
                    res = updateDb().addProduct(request.form, newname)
                    if res == "success":
                        flash("New Product Added Successfully", "success")
                    else:
                        flash("Can Not Update Database. Contact Admin", "error")
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        return render_template("add.html", username=g.user, role=g.role, date=date, time=time, form=form, vartype=types, catg=allCategory, seller=allSeller)
    else:
        return redirect(url_for('unauthenticated'))

# modify


@app.route("/modify/<product>", methods=['GET', 'POST'])
def modify(product):
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        product2modify = dbQuery().getThisproduct(product)
        types = dbQuery().getVarType()
        allCategory = dbQuery().getAllCatg()
        allSeller = dbQuery().getAllvendor()
        form = productImage()
        if request.method == "POST":
            if request.files['image'].filename != "":
                res = validateProduct(
                    request.form, request.files).imageValidate()
                if res == "success":
                    # upload image first
                    extinsion = request.files['image'].filename.rsplit('.')
                    originalFilename = extinsion[0]
                    extinsion = extinsion[1].lower()
                    rootPath = os.path.join(
                        app.root_path, 'static', 'uploads')
                    newname = str(uuid.uuid4().hex)+'.'+str(extinsion)
                    destination = "/".join([rootPath, newname])
                    try:
                        request.files['image'].save(destination)
                    except Exception as e:
                        flash(
                            "Unable To Upload Product Image. Contact Admin", "error")
                    else:
                        updateProduct = updateDb().updateProduct(
                            request.form, product, newname)
                        if updateProduct == "success":
                            flash("Product Updated Successfully", "success")
                        else:
                            flash(
                                "Unable To Update Product. Contact Admin!", "error")
                elif res == "error1":
                    flash("dowble ext", "error")
                elif res == "error2":
                    flash("other file", "error")
            else:
                updateProduct = updateDb().updateProduct(
                    request.form, product, product2modify[0]['image'])
                if updateProduct == "success":
                    flash("Product Updated Successfully", "success")
                else:
                    flash("Unable To Update Product. Contact Admin!", "error")
        return render_template("modify.html", form=form, username=g.user, role=g.role, date=date, time=time, pid=product, details=product2modify[0], vartype=types, catg=allCategory, seller=allSeller)
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
# chnage product status


@app.route("/statusToggle", methods=['GET', 'POST'])
def statusToggle():
    if g.user:
        if request.method == "POST":
            product = request.form.get("id")
            toggle = dbQuery().changeProduct(product)
            if toggle == "error":
                return "false"
            else:
                return toggle
    else:
        return "Please Login"


# delete product from db


@app.route("/removeProduct", methods=['GET', 'POST'])
def removeProduct():
    if g.user:
        if request.method == "POST":
            product = request.form.get("id")
            delPro = dbQuery().deleteProduct(product)
            if delPro == "success":
                return "True"
            else:
                return "False"
    else:
        return "Please Login"

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


# get product of certain seller endpoint
@app.route("/getProductofSeller", methods=['GET', 'POST'])
def getProductofSeller():
    if g.user:
        productDict = {
            "productname": [],
            "productid": []
        }
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        if request.method == "POST":
            data = request.form.get("data")
            allProducts = dbQuery().getSellerProduct(data)
            for x in allProducts:
                productDict['productname'].append(x['name'])
                productDict['productid'].append(x['productid'])
            return productDict
    else:
        return "Unauthenticated"


# get product details of selected producct
@app.route("/getSelectedDetails", methods=['GET', 'POST'])
def getSelectedDetails():
    if g.user:
        productDict = {
            "quantity": [],
            "price": [],
            "tax": []
        }
        if request.method == "POST":
            product = request.form.get("data")
            allProduct = dbQuery().getSelectedProduct(product)
            for x in allProduct:
                productDict['quantity'].append(x['quantity'])
                productDict['price'].append(x['sellprice'])
                productDict['tax'].append(x['tax'])
            return productDict
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
