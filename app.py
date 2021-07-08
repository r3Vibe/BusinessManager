################ all imports ################
from flask import render_template, redirect, g, flash, url_for, session, request, send_file
from Manager.form import Login, productImage
from Manager.validation import validateUser, validateProduct
from Manager.database import dbQuery, updateDb
import time
from datetime import datetime, date
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
import os
import uuid
from Manager import app


################ home page ################


@app.route("/", methods=['GET', 'POST'])
def home():
    if g.user:
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))
################  login page ################


@app.route("/login", methods=['GET', 'POST'])
def login():
    if not g.user:
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
    else:
        return redirect(url_for('dashboard'))

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
        newOrderID = dbQuery().getNewOrderID()
        return render_template("placeorder.html", username=g.user, role=g.role, date=date, time=time, product=allProduct, vendor=allVendor, orderid=newOrderID)
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
        dbQuery().checkQtStat()
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
            balance = dbQuery().checkBalance(int(request.form.get("cost"))
                                             * int(request.form.get("quantity")))
            if validate == "error1":
                flash("Don't Do That", "error")
            elif validate == "error2":
                flash("You Can Not Upload This File", "error")
            elif validate == "error3":
                flash(
                    "This Product Already In Inventory Place Order From Order Page", "error")
            elif balance != "available":
                flash(
                    "You Dont Have Sufficient Balance To Add This Product", "error")
            else:
                # upload image first
                extinsion = request.files['image'].filename.rsplit('.')
                extinsion = extinsion[1].lower()
                rootPath = os.path.join(
                    app.root_path, 'static', 'productimage')
                newname = str(uuid.uuid4().hex)+'.'+str(extinsion)
                destination = "/".join([rootPath, newname])
                try:
                    request.files['image'].save(destination)
                except Exception as e:
                    print(e)
                    flash("Unable To Upload Product Image. Contact Admin", "error")
                else:
                    # update database with new product
                    res = updateDb().addProduct(request.form, newname)
                    if res == "success":
                        return redirect(url_for("inventory"))
                    else:
                        flash("Can Not Update Database. Contact Admin", "error")
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        return render_template("add.html", username=g.user, role=g.role, date=date, time=time, form=form, vartype=types, catg=allCategory, seller=allSeller)
    else:
        return redirect(url_for('unauthenticated'))

# inventory page modify product


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

# inventory page order list


@app.route("/orderlist", methods=['GET', 'POST'])
def orderlist():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        if request.method == "GET":
            currentOrders = dbQuery().getCurrentOrders('all')
            return render_template("orderlist.html", username=g.user, role=g.role, date=date, time=time, orders=currentOrders)
        if request.method == "POST":
            param = request.form.get('sort')
            currentOrders = dbQuery().getCurrentOrders(param)
            return render_template("orderlist.html", username=g.user, role=g.role, date=date, time=time, orders=currentOrders)
    else:
        return redirect(url_for('unauthenticated'))


################ Accounts management page ################
#### main page ####
@app.route("/accounting", methods=['GET', 'POST'])
def accounting():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        balance = dbQuery().getTransaction("bal")
        dues = dbQuery().getTotalDues()
        return render_template("account.html", username=g.user, role=g.role, date=date, time=time, bal=balance, due=dues)
    else:
        return redirect(url_for('unauthenticated'))


#####################################
#### transactions page ####
@app.route("/transactions", methods=['GET', 'POST'])
def transactions():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        if request.method == "GET":
            trans = dbQuery().getTransaction("all")
            return render_template("transaction.html", username=g.user, role=g.role, date=date, time=time, trans=trans)
        if request.method == "POST":
            param = request.form.get('sort')
            trans = dbQuery().getTransaction(param)
            return render_template("transaction.html", username=g.user, role=g.role, date=date, time=time, trans=trans)
    else:
        return redirect(url_for('unauthenticated'))


##########################
#### newtransaction page ####
@app.route("/newtransaction", methods=['GET', 'POST'])
def newtransaction():
    if g.user:
        if request.method == "POST":
            data = request.form
            status = dbQuery().addTransaction(data)
            if status == "False":
                flash("Error Adding Entry! Try Later", "error")
            else:
                flash("Entry Added", "success")
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        return render_template("new.html", username=g.user, role=g.role, date=date, time=time)
    else:
        return redirect(url_for('unauthenticated'))


##########################
#### dues page ####
@app.route("/alldues", methods=['GET', 'POST'])
def alldues():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        if request.method == "GET":
            dues = dbQuery().getAllDues("all")
            return render_template("due.html", username=g.user, role=g.role, date=date, time=time, dues=dues)
        if request.method == "POST":
            values = request.form.get("search")
            dues = dbQuery().getAllDues(values)
            return render_template("due.html", username=g.user, role=g.role, date=date, time=time, dues=dues)
    else:
        return redirect(url_for('unauthenticated'))


################ invoicing management page ################
#### invoice page ####
@app.route("/invoice", methods=['GET', 'POST'])
def invoice():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        dbQuery().changeRefundPolicy()
        if request.method == "GET":
            allInv = dbQuery().getInvoices("all")
            return render_template("invoice.html", username=g.user, role=g.role, date=date, time=time, invoice=allInv)
        if request.method == "POST":
            parameter = request.form.get("search")
            allInv = dbQuery().getInvoices(parameter)
            return render_template("invoice.html", username=g.user, role=g.role, date=date, time=time, invoice=allInv)
    else:
        return redirect(url_for('unauthenticated'))


##########################
#### makeinvoice page ####
@app.route("/makeinvoice", methods=['GET', 'POST'])
def makeinvoice():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        allProd = dbQuery().getProducts()
        invoice = dbQuery().generateInvoiceid()
        return render_template("create.html", username=g.user, role=g.role, date=date, time=time, prods=allProd, invid=invoice)
    else:
        return redirect(url_for('unauthenticated'))
#############################
####### serviceinvoice ######


@app.route("/serviceinvoice", methods=['GET', 'POST'])
def serviceinvoice():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        allProd = dbQuery().getServices()
        invoice = dbQuery().generateInvoiceid()
        return render_template("servicecreate.html", username=g.user, role=g.role, date=date, time=time, prods=allProd, invid=invoice)
    else:
        return redirect(url_for('unauthenticated'))


#####################################################################
##########################  customer management #####################
#####################################################################

####################################################
################ customer order list ##################
@app.route("/orders/<cust>", methods=['GET', 'POST'])
def orders(cust):
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        if request.method == "GET":
            orders = dbQuery().getSellOrder(cust)
            customer = dbQuery().getCustomerDetails(cust)
            customer = customer.split(":")[0]
            return render_template("custorder.html", username=g.user, role=g.role, date=date, time=time, orders=orders, cname=customer)
        elif request.method == "POST":
            param = request.form.get("search")
            orders = dbQuery().getCertOrder(param)
            customer = dbQuery().getCustomerDetails(cust)
            customer = customer.split(":")[0]
            return render_template("custorder.html", username=g.user, role=g.role, date=date, time=time, orders=orders, cname=customer)
    else:
        return redirect(url_for('unauthenticated'))

####################################################
################ list of customer ##################


@app.route("/custmanager", methods=['GET', 'POST'])
def custmanager():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        if request.method == "GET":
            allCust = dbQuery().getAllCust("all")
            return render_template("customermanager.html", username=g.user, role=g.role, date=date, time=time, cust=allCust)
        elif request.method == "POST":
            param = request.form.get("search")
            allCust = dbQuery().getAllCust(param)
            return render_template("customermanager.html", username=g.user, role=g.role, date=date, time=time, cust=allCust)
    else:
        return redirect(url_for('unauthenticated'))
####################################################
################ add new customer ##################


@app.route("/addcustomer", methods=['GET', 'POST'])
def addcustomer():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        if request.method == "GET":
            return render_template("addcustomer.html", username=g.user, role=g.role, date=date, time=time)
        elif request.method == "POST":
            data = request.form
            pstatus = dbQuery().addCustomer(data)
            if pstatus == "success":
                flash("Customer Added", "success")
                return render_template("addcustomer.html", username=g.user, role=g.role, date=date, time=time)
            else:
                flash("Something Went Wrong", "error")
                return render_template("addcustomer.html", username=g.user, role=g.role, date=date, time=time)

    else:
        return redirect(url_for('unauthenticated'))


##############################################
##################recharge###################
@app.route("/recharge", methods=['GET', 'POST'])
def recharge():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        carrier = dbQuery().getCarrier()
        if request.method == "GET":
            return render_template("recharge.html", username=g.user, role=g.role, date=date, time=time, carrier=carrier)
        if request.method == "POST":
            status = dbQuery().addRecharge(request.form)
            if status == "success":
                flash("New Reccord Added", "success")
            else:
                flash("Something Went Wrong", "error")
            return render_template("recharge.html", username=g.user, role=g.role, date=date, time=time, carrier=carrier)
    else:
        return redirect(url_for('unauthenticated'))


@app.route("/rechargelist", methods=['GET', 'POST'])
def rechargelist():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        if request.method == "GET":
            lists = dbQuery().getAllrc("all")
            return render_template("rechargelist.html", username=g.user, role=g.role, date=date, time=time, lists=lists)
        if request.method == "POST":
            lists = dbQuery().getAllrc(request.form.get('search'))
            return render_template("rechargelist.html", username=g.user, role=g.role, date=date, time=time, lists=lists)
    else:
        return redirect(url_for('unauthenticated'))


######################################################################
########################### management page ##########################
######################################################################
@app.route("/management", methods=['GET', 'POST'])
def management():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        emply = dbQuery().getEmply()
        privi = dbQuery().getPrivi()
        if request.method == "GET":
            return render_template("management.html", username=g.user, role=g.role, date=date, time=time, emply=emply, privi=privi)
        if request.method == "POST":
            userDetails = request.form
            extinsion = request.files['image'].filename.rsplit('.')
            extinsion = extinsion[1].lower()
            rootPath = os.path.join(
                app.root_path, 'static', 'userimage')
            newname = str(uuid.uuid4().hex)+'.'+str(extinsion)
            destination = "/".join([rootPath, newname])
            try:
                request.files['image'].save(destination)
            except Exception as e:
                flash("Something Went Wrong", "error")
            else:
                status = dbQuery().addEmploy(userDetails, newname)
                if status == "success":
                    flash("Employee Added", "success")
                else:
                    flash("Something Went Wrong", "error")
            return redirect(url_for("management"))
    else:
        return redirect(url_for('unauthenticated'))
######################################################################
########################### allservices page ##########################
######################################################################


@app.route("/services", methods=['GET', 'POST'])
def services():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        services = dbQuery().getServices()
        if request.method == "GET":
            return render_template("services.html", username=g.user, role=g.role, date=date, time=time, services=services)
        if request.method == "POST":
            serviceDetails = request.form

            status = dbQuery().addService(serviceDetails)
            if status == "success":
                return redirect(url_for("services"))
    else:
        return redirect(url_for('unauthenticated'))


######################################################################
########################### category page ##########################
######################################################################


@app.route("/category", methods=['GET', 'POST'])
def category():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        category = dbQuery().getCategory()
        if request.method == "GET":
            return render_template("category.html", username=g.user, role=g.role, date=date, time=time, category=category)
        if request.method == "POST":
            categoryDetails = request.form

            status = dbQuery().addCategory(categoryDetails)
            if status == "success":
                return redirect(url_for("category"))
    else:
        return redirect(url_for('unauthenticated'))


######################################################################
########################### Commission page ##########################
######################################################################


@app.route("/commission", methods=['GET', 'POST'])
def commission():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        comm = dbQuery().getcommission()
        if request.method == "GET":
            return render_template("commission.html", username=g.user, role=g.role, date=date, time=time, comm=comm)
        if request.method == "POST":
            commDetails = request.form
            print(commDetails)
            status = dbQuery().addComm(commDetails)
            if status == "success":
                return redirect(url_for("commission"))
    else:
        return redirect(url_for('unauthenticated'))


######################################################################
###################### privilages ####################################


@app.route("/privilages", methods=['GET', 'POST'])
def privilages():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        privi = dbQuery().getPrivi()
        if request.method == "GET":
            return render_template("priv.html", username=g.user, role=g.role, date=date, time=time, privi=privi)
        if request.method == "POST":
            privform = request.form
            status = dbQuery().addPriv(privform)
            if status == "error":
                flash("Something Went Wrong", "error")
            else:
                return redirect(url_for("privilages"))
    else:
        return redirect(url_for('unauthenticated'))


######################################################################
###################### vendors ####################################


@app.route("/vendors", methods=['GET', 'POST'])
def vendors():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        vendor = dbQuery().getVendor()
        if request.method == "GET":
            return render_template("vendors.html", username=g.user, role=g.role, date=date, time=time, vendor=vendor)
        if request.method == "POST":
            venform = request.form
            status = dbQuery().addVendor(venform)
            if status == "error":
                flash("Something Went Wrong", "error")
            else:
                return redirect(url_for("vendors"))
    else:
        return redirect(url_for('unauthenticated'))


######################################################################
###################### variations ####################################


@app.route("/variations", methods=['GET', 'POST'])
def variations():
    if g.user:
        date = datetime.today()
        date = date.strftime("%d/%m/%Y")
        time = datetime.now()
        time = time.strftime("%H:%M:%S")
        variations = dbQuery().getvariations()
        if request.method == "GET":
            return render_template("variations.html", username=g.user, role=g.role, date=date, time=time, variations=variations)
        if request.method == "POST":
            variationsform = request.form
            status = dbQuery().addVariations(variationsform)
            if status == "error":
                flash("Something Went Wrong", "error")
            else:
                return redirect(url_for("variations"))
    else:
        return redirect(url_for('unauthenticated'))


################ remove session variable and redirect ################
# logout page


@app.route("/logout", methods=['GET', 'POST'])
def logout():
    session.pop('user', None)
    session.pop('role', None)
    session.clear()
    return redirect(url_for("login"))


################ redirect if not login ################
# unauthenticated url access deny
@app.route("/unauthenticated", methods=['GET', 'POST'])
def unauthenticated():
    return render_template("unauth.html")

############### api ##############


@app.route("/removeVariation", methods=['GET', 'POST'])
def removeVariation():
    if g.user:
        if request.method == "POST":
            details = request.form.get("varid")
            return dbQuery().delVar(details)
    else:
        return "Please Login"


@app.route("/removeVendor", methods=['GET', 'POST'])
def removeVendor():
    if g.user:
        if request.method == "POST":
            details = request.form.get("venid")
            return dbQuery().delVen(details)
    else:
        return "Please Login"


@app.route("/removeUser", methods=['GET', 'POST'])
def removeUser():
    if g.user:
        if request.method == "POST":
            details = request.form.get("userid")
            return dbQuery().delUser(details)
    else:
        return "Please Login"


@app.route("/deleteComm", methods=['GET', 'POST'])
def deleteComm():
    if g.user:
        if request.method == "POST":
            details = request.form.get("commid")
            return dbQuery().delComm(details)
    else:
        return "Please Login"


@app.route("/deleteCategory", methods=['GET', 'POST'])
def deleteCategory():
    if g.user:
        if request.method == "POST":
            details = request.form.get("catid")
            return dbQuery().delCatg(details)
    else:
        return "Please Login"


@app.route("/deleteService", methods=['GET', 'POST'])
def deleteService():
    if g.user:
        if request.method == "POST":
            details = request.form.get("servid")
            return dbQuery().delServ(details)
    else:
        return "Please Login"
################################################
############### feature product on site ########


@app.route("/featurethis", methods=['GET', 'POST'])
def featurethis():
    if g.user:
        if request.method == "POST":
            details = request.form.get("id")
            status = dbQuery().featureThis(details)
            return status
    else:
        return "Please Login"


@app.route("/unfeaturethis", methods=['GET', 'POST'])
def unfeaturethis():
    if g.user:
        if request.method == "POST":
            details = request.form.get("id")
            status = dbQuery().unfeatureThis(details)
            return status
    else:
        return "Please Login"


# delete privilage


@app.route("/delPriv", methods=['GET', 'POST'])
def delPriv():
    if g.user:
        if request.method == "POST":
            details = request.form.get("privid")

            return dbQuery().delPriv(details)
    else:
        return "Please Login"


############################################
############# updateCustomer ##################


@app.route("/updateCustomer", methods=['GET', 'POST'])
def updateCustomer():
    if g.user:
        if request.method == "POST":
            details = request.form
            status = dbQuery().custUpdate(details)
            return status
    else:
        return "Please Login"
############################################
############# refundOrder ##################


@app.route("/refundOrder", methods=['GET', 'POST'])
def refundOrder():
    if g.user:
        if request.method == "POST":
            details = request.form.get("data")
            status = dbQuery().refundOrder(details)
            return status
    else:
        return "Please Login"
#############################################
###########   cancelOrder ###################


@app.route("/cancelOrder", methods=['GET', 'POST'])
def cancelOrder():
    if g.user:
        if request.method == "POST":
            details = request.form.get("data")
            status = dbQuery().cancelOrder(details)
            return status
    else:
        return "Please Login"
###############################################
############# newServiceInvoice ###############


@app.route("/newServiceInvoice", methods=['GET', 'POST'])
def newServiceInvoice():
    if g.user:
        if request.method == "POST":
            details = request.form
            status = dbQuery().makeInvoiceforService(details)
            return "success"
    else:
        return "Please Login"

###############################################
###########  markAsSold  ######################


@app.route("/markAsSold", methods=['GET', 'POST'])
def markAsSold():
    if g.user:
        if request.method == "POST":
            details = request.form.get("data")
            status = dbQuery().markAsSold(details)
            if status == "success":
                return "success"
            else:
                return "error"
    else:
        return "Please Login"


#######################################
##########checkAvailable################


@app.route("/checkAvailable", methods=['GET', 'POST'])
def checkAvailable():
    if g.user:
        if request.method == "POST":
            details = request.form
            status = dbQuery().checkAvailable(details)
            if status == "success":
                return "success"
            else:
                return "error"
    else:
        return "Please Login"
###################################
######## make customer invoice ####


@app.route("/newInvoice", methods=['GET', 'POST'])
def newInvoice():
    if g.user:
        if request.method == "POST":
            details = request.form
            status = dbQuery().makeNewInvoice(details)
            if status == "success":
                return "success"
            else:
                return "error"
    else:
        return "Please Login"

#################################
#########getThisproduct#########


@app.route("/getProd", methods=['GET', 'POST'])
def getProd():
    if g.user:
        if request.method == "POST":
            pid = request.form.get("data")
            status = dbQuery().getProd(pid)
            return status
    else:
        return "Please Login"


@app.route("/getServ", methods=['GET', 'POST'])
def getServ():
    if g.user:
        if request.method == "POST":
            pid = request.form.get("data")
            status = dbQuery().getServ(pid)
            return status
    else:
        return "Please Login"


###################################
############addCustomer############
@app.route("/addCustomer", methods=['GET', 'POST'])
def addCustomer():
    if g.user:
        if request.method == "POST":
            data = request.form
            status = dbQuery().addCustomer(data)
            if status == "success":
                return "Customer Added"
            else:
                return "Unable To Add New Customer"
    else:
        return "Please Login"

######################################
######### getCustomerDetails #########


@app.route("/getCustomerDetails", methods=['GET', 'POST'])
def getCustomerDetails():
    if g.user:
        if request.method == "POST":
            phonenumber = request.form.get("data")
            status = dbQuery().getCustomerDetails(phonenumber)
            if status == False:
                return "error"
            else:
                return status
    else:
        return "Please Login"


##############################
#####  clear dues  ###########
@app.route("/clearDues", methods=['GET', 'POST'])
def clearDues():
    if g.user:
        if request.method == "POST":
            reference = request.form.get("data")
            status = dbQuery().clearDue(reference)
            if status == 'success':
                return "ok"
            else:
                flash("Something Went Wrong!", "error")
                return "error"
    else:
        return "Please Login"

# receive products from order list


@app.route("/receiveit", methods=['GET', 'POST'])
def receiveit():
    if g.user:
        if request.method == "POST":
            orderid = request.form.get("id")
            status = dbQuery().updateReceived(orderid)
            if status == 'success':
                return "ok"
            else:
                return "error"
    else:
        return "Please Login"

# cancel products from order list


@app.route("/cancelit", methods=['GET', 'POST'])
def cancelit():
    if g.user:
        if request.method == "POST":
            orderid = request.form.get("id")
            status = dbQuery().updateCancelled(orderid)
            if status == 'success':
                return "ok"
            else:
                return "error"
    else:
        return "Please Login"

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

###################################################
##### get product details of selected producct#####


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
                productDict['price'].append(x['unitprice'])
                productDict['tax'].append(x['tax'])
            return productDict
    else:
        return "Unauthenticated"

# create xlsx file with details given


@app.route("/makePurchaseOrder", methods=['GET', 'POST'])
def makePurchaseOrder():
    if g.user:
        if request.method == "POST":
            details = request.form
            makeOrder = dbQuery().makePurchaseOrder(details)
            return makeOrder
    else:
        return "Unauthenticated"

# check for available balance


@app.route("/checkBalance", methods=['GET', 'POST'])
def checkBalance():
    if g.user:
        if request.method == "POST":
            details = request.form
            makeOrder = dbQuery().checkBal(details)
            return makeOrder
    else:
        return "Unauthenticated"

# download xlsx file


@app.route("/downloadOrder/<filename>", methods=['GET', 'POST'])
def downloadOrder(filename):
    if g.user:
        filename = filename.split('=')
        fileee = f"static/purchaseorder/{filename[1]}.xlsx"
        return send_file(fileee, as_attachment=True)
    else:
        return "Unauthenticated"


# print file


@app.route("/printFile/<filename>", methods=['GET', 'POST'])
def printFile(filename):
    if g.user:
        filename = filename.split('=')
        location = os.getcwd()
        filee = f"{location}/Manager/static/purchaseorder/{filename[1]}.xlsx"
        os.startfile(filee, "print")
        return redirect(url_for('orderlist'))
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
