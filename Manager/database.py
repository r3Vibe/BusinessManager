# all importd
import mysql.connector
import os
from datetime import date, datetime
import uuid
import xlsxwriter

# connect to database
db = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='',
    database='businessmanager',
    auth_plugin='mysql_native_password'
)

# database curso
cursor = db.cursor(dictionary=True)


class dbQuery():
    def addCustomer(self, details):
        today = date.today()
        todate = today.strftime("%d-%m-%Y")
        dob = details['dob']
        dateArr = dob.split('-')
        dateArr.reverse()
        newdate = ""
        for x in dateArr:
            newdate += f"{x}-"
        dob = newdate.rstrip("-")
        cursor.execute(
            f"INSERT INTO customer(name,phone,custid,address,gender,birthday,joindate) VALUES('{details['name']}','{details['phoneno']}','{details['phoneno']}','{details['custaddr']}','{details['gender']}','{dob}','{todate}')")
        try:
            db.commit()
        except Exception as e:
            return "False"
        else:
            return "success"

    def makeNewInvoice(self, product):
        print(product)
        print(product['totoalrow'])
        print(product['unitpricef'])
        return "success"

    def getCustomerDetails(self, num):
        cursor.execute(f"SELECT * FROM customer WHERE custid='{num}'")
        details = cursor.fetchall()
        if len(details) == 0:
            return "error"
        else:
            name = details[0]['name']
            addr = details[0]['address']
            returnn = f"{name}:{addr}"
            return returnn

    def generateInvoiceid(self):
        d = datetime.now()
        monthasnum = d.strftime("%m")
        time = d.strftime('%H%M%S')
        return f"Inv/{monthasnum}/{time}"

    def checkBalance(self, data):
        grandtotal = int(data)
        cursor.execute(f"SELECT * FROM transaction ORDER BY id DESC")
        lastBal = cursor.fetchall()
        if len(lastBal) == 0:
            lastBal = 0
        else:
            lastBal = int(lastBal[0]['balance'])

        if grandtotal > lastBal:
            return "error"
        else:
            return "available"

    def checkBal(self, data):
        grandtotal = int(data['totalpricef'])
        cursor.execute(f"SELECT * FROM transaction ORDER BY id DESC")
        lastBal = cursor.fetchall()
        if len(lastBal) == 0:
            lastBal = 0
        else:
            lastBal = int(lastBal[0]['balance'])

        if grandtotal > lastBal:
            return "error"
        else:
            return "available"

    def clearDue(self, ref):
        today = date.today()
        todate = today.strftime("%d-%m-%Y")
        cursor.execute(f"SELECT * FROM alldues WHERE reference = '{ref}'")
        allDues = cursor.fetchall()
        cursor.execute(f"SELECT * FROM transaction ORDER BY id DESC")
        lastBal = cursor.fetchall()
        if len(lastBal) == 0:
            lastBal = 0
        else:
            lastBal = int(lastBal[0]['balance'])
        balance = lastBal + int(allDues[0]['amount'])
        cursor.execute(
            f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{todate}','{allDues[0]['reference']}','{allDues[0]['account']}','{allDues[0]['amount']}','0','{balance}')")
        try:
            db.commit()
        except Exception as e:
            return "False"
        else:
            cursor.execute(f"DELETE FROM alldues WHERE reference = '{ref}'")
            try:
                db.commit()
            except Exception as e:
                return "False"
            else:
                return "success"

    def getTotalDues(self):
        total = 0
        cursor.execute("SELECT amount FROM alldues")
        alltrans = cursor.fetchall()
        for x in alltrans:
            total = total + int(x['amount'])
        return total

    def getAllDues(self, param):
        if param == "all":
            cursor.execute("SELECT * FROM alldues")
            alltrans = cursor.fetchall()
            return alltrans
        else:
            cursor.execute(
                f"SELECT * FROM alldues WHERE name LIKE '%{param}%'")
            alltrans = cursor.fetchall()
            return alltrans

    def getTransaction(self, param):
        if param == "all":
            cursor.execute("SELECT * FROM transaction")
            alltrans = cursor.fetchall()
            return alltrans
        elif param == "debit":
            cursor.execute("SELECT * FROM transaction WHERE debit != '0'")
            alltrans = cursor.fetchall()
            return alltrans
        elif param == "credit":
            cursor.execute("SELECT * FROM transaction WHERE credit != '0'")
            alltrans = cursor.fetchall()
            return alltrans
        elif param == "bal":
            cursor.execute("SELECT * FROM transaction ORDER BY id DESC")
            alltrans = cursor.fetchall()
            return alltrans
        else:
            cursor.execute(
                f"SELECT * FROM transaction WHERE account = '{param}' OR reference LIKE '%{param}%'")
            alltrans = cursor.fetchall()
            return alltrans

    def addTransaction(self, entry):
        today = date.today()
        todate = today.strftime("%d-%m-%Y")
        types = entry.get('type')
        account = entry.get('account')
        amount = entry.get('amount')
        cursor.execute(f"SELECT * FROM transaction ORDER BY id DESC")
        lastBal = cursor.fetchall()
        if len(lastBal) == 0:
            lastBal = 0
        else:
            lastBal = int(lastBal[0]['balance'])
        if types == "debit":
            getRef = f"refdebit{account}{datetime.now().strftime('%H%M%S')}"
            balance = lastBal + int(amount)
            cursor.execute(
                f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{todate}','{getRef}','{account}','{amount}','0','{balance}')")
            try:
                db.commit()
            except Exception as e:
                return "False"
            else:
                return "success"
        elif types == "credit":
            getRef = f"refcredit{account}{today.yeardatetime.now().strftime('%H%M%S')}"
            balance = lastBal - int(amount)
            cursor.execute(
                f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{todate}','{getRef}','{account}','0','{amount}','{balance}')")
            try:
                db.commit()
            except Exception as e:
                return "False"
            else:
                return "success"
        elif types == "due":
            custname = entry.get('customer')
            getRef = f"refdue{custname}{account}{datetime.now().strftime('%H%M%S')}"
            cursor.execute(
                f"INSERT INTO alldues(date,reference,account,name,amount) VALUES('{todate}','{getRef}','{account}','{custname}','{amount}')")
            try:
                db.commit()
            except Exception as e:
                return "False"
            else:
                return "success"
        else:
            return "False"

    def getVarType(self):
        cursor.execute(f"SELECT * FROM variation")
        types = cursor.fetchall()
        return types

    def getAllVars(self, typess):
        cursor.execute(f"SELECT * FROM variation WHERE type = '{typess}'")
        allvars = cursor.fetchall()
        return allvars

    def getAllCatg(self):
        cursor.execute(f"SELECT * FROM category")
        catgs = cursor.fetchall()
        return catgs

    def getAllvendor(self):
        cursor.execute(f"SELECT * FROM seller")
        seller = cursor.fetchall()
        return seller

    def checkPid(self, pid):
        cursor.execute(f"SELECT * FROM products WHERE productid = '{pid}'")
        pids = cursor.fetchall()
        return pids

    def getProducts(self):
        cursor.execute("SELECT * FROM products")
        product = cursor.fetchall()
        return product

    def getSpeProducts(self, keys):
        cursor.execute(
            f"SELECT * FROM products WHERE name LIKE '%{keys}%' OR productid LIKE '%{keys}%' OR category LIKE '%{keys}%' OR vars LIKE '%{keys}%' OR sellprice LIKE '%{keys}%' OR date LIKE '%{keys}%'")
        product = cursor.fetchall()
        return product

    def getThisproduct(self, pid):
        product = pid.split('=')
        cursor.execute(
            f"SELECT * FROM products WHERE id = '{product[1]}'")
        product = cursor.fetchall()
        return product

    def getProd(self, pid):
        cursor.execute(
            f"SELECT * FROM products WHERE productid = '{pid}'")
        product = cursor.fetchall()
        return f"{product[0]['sellprice']}"

    def deleteProduct(self, pid):
        cursor.execute(f"DELETE FROM products WHERE id = '{pid}'")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            return "success"

    def changeProduct(self, pid):
        cursor.execute(f"SELECT * FROM products WHERE id = '{pid}'")
        product = cursor.fetchall()
        currentStatus = product[0]['status']
        if currentStatus == "active":
            newstatus = "stopped"
        else:
            newstatus = "active"
        cursor.execute(
            f"UPDATE  products SET status = '{newstatus}' WHERE id = '{pid}'")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            return newstatus

    def getSellerProduct(self, seller):
        cursor.execute(f"SELECT * FROM products WHERE seller = '{seller}'")
        product = cursor.fetchall()
        return product

    def getSelectedProduct(self, pid):
        cursor.execute(f"SELECT * FROM products WHERE productid = '{pid}'")
        product = cursor.fetchall()
        return product

    def getNewOrderID(self):
        cursor.execute("SELECT * FROM purchaseorder ORDER BY id DESC")
        allOrder = cursor.fetchall()
        if len(allOrder) == 0:
            return "2287655"
        else:
            return str(int(allOrder[0]['orderid']) + 1)

    def getCurrentOrders(self, parameter):
        if parameter == 'all':
            cursor.execute(f"SELECT * FROM purchaseorder")
            product = cursor.fetchall()
            return product
        else:
            cursor.execute(
                f"SELECT * FROM purchaseorder WHERE status = '{parameter}'")
            product = cursor.fetchall()
            return product

    def makePurchaseOrder(self, products):
        if int(products['totoalrow']) == 1:
            orderid = products['orderid']
            vendor = products['vendor']
            date = products['date']
            dateArr = date.split('-')
            dateArr.reverse()
            newdate = ""
            for x in dateArr:
                newdate += f"{x}-"
            date = newdate.rstrip("-")
            product = products['product']
            qt = products['qt']
            price = products['price']
            tax = products['tax']
            total = products['sttl']
            grandtotal = products['totalpricef']

            cursor.execute(
                f"SELECT * FROM products WHERE productid = '{product}'")
            productName = cursor.fetchall()[0]['name']

            # create workbook
            workbook = xlsxwriter.Workbook(
                filename=f'./Manager/static/purchaseorder/{orderid}.xlsx')

            # create worksheet
            worksheet = workbook.add_worksheet(name='purchaseorder')

            # widen columns
            worksheet.set_column('A:F', 20)

            # Create a format to use in the merged range.
            merge_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'})
            # increase font size
            merge_format.set_font_size(16)

            # merge top cells heaser
            worksheet.merge_range('A1:E1', 'Purchase Order', merge_format)

            # add compuulsury details to worksheet
            worksheet.write('A3', 'Order ID', merge_format)
            worksheet.write('D3', 'Date', merge_format)
            worksheet.write('A4', 'Vendor', merge_format)

            # add data to compulsury details of worksheet
            worksheet.write('B3', f'{orderid}', merge_format)
            worksheet.write('E3', f'{date}', merge_format)
            worksheet.write('B4', f'{vendor}', merge_format)

            # make purchase details table
            worksheet.write('A6', 'Product', merge_format)
            worksheet.write('B6', 'Quantity', merge_format)
            worksheet.write('C6', 'Unit Price', merge_format)
            worksheet.write('D6', 'Tax', merge_format)
            worksheet.write('E6', 'Subtotal', merge_format)

            # add data to table
            worksheet.write('A7', f'{productName}', merge_format)
            worksheet.write_number('B7', int(qt), merge_format)
            worksheet.write_number('C7', int(price), merge_format)
            worksheet.write_number('D7', int(tax), merge_format)
            worksheet.write_number('E7', int(total), merge_format)

            # merge grand total cells
            worksheet.merge_range('A8:D8', 'Grand Total', merge_format)

            # grad total
            worksheet.write_number('E8', int(grandtotal), merge_format)

            # close
            workbook.close()
            # get balance
            cursor.execute(f"SELECT * FROM transaction ORDER BY id DESC")
            lastBal = cursor.fetchall()
            if len(lastBal) == 0:
                lastBal = 0
            else:
                lastBal = int(lastBal[0]['balance'])
            # make balance
            balance = lastBal - int(grandtotal)

            # update purchaseorder database
            cursor.execute(
                f"INSERT INTO purchaseorder(orderid,vendor,date,status) VALUES('{orderid}','{vendor}','{date}','processing')")
            cursor.execute(
                f"INSERT INTO orderprocess(orderid,product,quantity) VALUES('{orderid}','{product}','{qt}')")
            cursor.execute(
                f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{date}','{orderid}','purchase','0','{grandtotal}','{balance}')")
            try:
                db.commit()
            except Exception as e:
                return "error"
            else:
                return "success"

        else:
            i = 2

            orderid = products[f'orderid']
            vendor = products[f'vendor']
            date = products[f'date']
            grandtotal = products['totalpricef']

            # create workbook
            workbook = xlsxwriter.Workbook(
                filename=f'./Manager/static/purchaseorder/{orderid}.xlsx')

            # create worksheet
            worksheet = workbook.add_worksheet(name='purchaseorder')

            # widen columns
            worksheet.set_column('A:F', 20)

            # Create a format to use in the merged range.
            merge_format = workbook.add_format({
                'bold': 1,
                'border': 1,
                'align': 'center',
                'valign': 'vcenter'})
            # increase font size
            merge_format.set_font_size(16)

            # merge top cells heaser
            worksheet.merge_range('A1:E1', 'Purchase Order', merge_format)

            # add compuulsury details to worksheet
            worksheet.write('A3', 'Order ID', merge_format)
            worksheet.write('D3', 'Date', merge_format)
            worksheet.write('A4', 'Vendor', merge_format)

            # add data to compulsury details of worksheet
            worksheet.write('B3', f'{orderid}', merge_format)
            worksheet.write('E3', f'{date}', merge_format)
            worksheet.write('B4', f'{vendor}', merge_format)

            # make purchase details table
            worksheet.write('A6', 'Product', merge_format)
            worksheet.write('B6', 'Quantity', merge_format)
            worksheet.write('C6', 'Unit Price', merge_format)
            worksheet.write('D6', 'Tax', merge_format)
            worksheet.write('E6', 'Subtotal', merge_format)

            # first product
            product = products[f'product']
            qt = products[f'qt']
            price = products[f'price']
            tax = products[f'tax']
            total = products[f'sttl']

            cursor.execute(
                f"SELECT * FROM products WHERE productid = '{product}'")
            productName = cursor.fetchall()[0]['name']

            # first product entry
            worksheet.write(f'A{7}', f'{productName}', merge_format)
            worksheet.write_number(f'B{7}', int(qt), merge_format)
            worksheet.write_number(f'C{7}', int(price), merge_format)
            worksheet.write_number(f'D{7}', int(tax), merge_format)
            worksheet.write_number(f'E{7}', int(total), merge_format)

            prodDb = product
            qtDb = qt

            # add data to table
            while i <= int(products['totoalrow']):
                product = products[f'product{i}']
                qt = products[f'qt{i}']
                price = products[f'price{i}']
                tax = products[f'tax{i}']
                total = products[f'sttl{i}']

                cursor.execute(
                    f"SELECT * FROM products WHERE productid = '{product}'")
                productName = cursor.fetchall()[0]['name']

                prodDb += f':{product}'
                qtDb += f':{qt}'

                worksheet.write(f'A{6+i}', f'{productName}', merge_format)
                worksheet.write_number(f'B{6+i}', int(qt), merge_format)
                worksheet.write_number(f'C{6+i}', int(price), merge_format)
                worksheet.write_number(f'D{6+i}', int(tax), merge_format)
                worksheet.write_number(f'E{6+i}', int(total), merge_format)

                # merge grand total cells
                worksheet.merge_range(
                    f'A{6+i+1}:D{6+i+1}', 'Grand Total', merge_format)

                # grad total
                worksheet.write_number(
                    f'E{6+i+1}', int(grandtotal), merge_format)

                # close
                workbook.close()

                i += 1

                if i > int(products['totoalrow']):
                    break

            # get balance
            cursor.execute(f"SELECT * FROM transaction ORDER BY id DESC")
            lastBal = cursor.fetchall()
            if len(lastBal) == 0:
                lastBal = 0
            else:
                lastBal = int(lastBal[0]['balance'])
            # make balance
            balance = lastBal - int(grandtotal)

            # update purchaseorder database
            cursor.execute(
                f"INSERT INTO purchaseorder(orderid,vendor,date,status) VALUES('{orderid}','{vendor}','{date}','processing')")
            cursor.execute(
                f"INSERT INTO orderprocess(orderid,product,quantity) VALUES('{orderid}','{prodDb}','{qtDb}')")
            cursor.execute(
                f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{date}','{orderid}','purchase','0','{grandtotal}','{balance}')")
            try:
                db.commit()
            except Exception as e:
                return "error"
            else:
                return "success"

        return "ok"

    def updateReceived(self, order):
        cursor.execute(f"SELECT * FROM orderprocess WHERE orderid = '{order}'")
        orderDetails = cursor.fetchall()[0]

        # update respective products
        totalProducts = len(orderDetails['product'].split(':'))
        print(totalProducts)
        Products = orderDetails['product'].split(':')
        quantity = orderDetails['quantity'].split(':')
        i = 0
        while i < int(totalProducts):
            cursor.execute(
                f"SELECT * FROM products WHERE productid = '{Products[i]}'")
            quantityDb = cursor.fetchall()[0]['quantity']
            newQt = int(quantityDb) + int(quantity[i])
            cursor.execute(
                f"UPDATE products SET quantity='{newQt}' WHERE productid = '{Products[i]}'")
            try:
                db.commit()
            except Exception as e:
                return "Unable To Update Please Contact System Admin"
            else:
                i += 1
            if i > totalProducts:
                break

        # change status of orderlist
        cursor.execute(
            f"UPDATE purchaseorder SET status='Received' WHERE orderid = '{order}'")
        cursor.execute(
            f"UPDATE orderprocess SET status='Received' WHERE orderid = '{order}'")
        try:
            db.commit()
        except Exception as e:
            return "Unable To Update Please Contact System Admin"
        else:
            return "success"

    def updateCancelled(self, order):
        cursor.execute(
            f"UPDATE orderprocess SET status='Cancelled' WHERE orderid = '{order}'")
        cursor.execute(
            f"UPDATE purchaseorder SET status='Cancelled' WHERE orderid = '{order}'")
        try:
            db.commit()
        except Exception as e:
            return "Unable To Update Please Contact System Admin"
        else:
            return "success"


class updateDb():
    def addProduct(self, details, imagename):
        cursor.execute("SELECT * FROM purchaseorder ORDER BY id DESC")
        allOrder = cursor.fetchall()
        if len(allOrder) == 0:
            orderid = "2287655"
        else:
            orderid = str(int(allOrder[0]['orderid']) + 1)
        today = date.today()
        todate = today.strftime("%d-%m-%Y")
        barcode = details['barcode']
        dimension = f"{details['length']}x{details['bredth']}x{details['height']} {details['measure']}"
        weight = f"{details['weight']} {details['weightmeasure']}"
        if barcode == "":
            barcode = "nocode"
        grandtotal = int(details['quantity']) * int(details['cost'])
        # get balance
        cursor.execute(f"SELECT * FROM transaction ORDER BY id DESC")
        lastBal = cursor.fetchall()
        if len(lastBal) == 0:
            lastBal = 0
        else:
            lastBal = int(lastBal[0]['balance'])
        # make balance
        balance = lastBal - int(grandtotal)
        cursor.execute(
            f"INSERT INTO products(name,productid,status,barcode,vartype,vars,category,seller,quantity,unitprice,sellprice,tax,dimension,weight,image,date) VALUES('{details['name']}','{details['productid']}','active','{barcode}','{details['vartype']}','{details['vars']}','{details['catg']}','{details['seller']}','{details['quantity']}','{details['cost']}','{details['sellprice']}','{details['tax']}','{dimension}','{weight}','{imagename}','{todate}')")
        cursor.execute(
            f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{todate}','{orderid}','purchase','0','{grandtotal}','{balance}')")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            return "success"

    def updateProduct(self, details, proid, imagename):
        product = proid.split('=')
        today = date.today()
        todate = today.strftime("%d-%m-%Y")
        barcode = details['barcode']
        dimension = f"{details['length']}x{details['bredth']}x{details['height']} {details['measure']}"
        weight = f"{details['weight']} {details['weightmeasure']}"
        if barcode == "":
            barcode = "nocode"
        cursor.execute(
            f"UPDATE products SET name='{details['name']}',productid='{details['productid']}',barcode='{details['barcode']}',vartype='{details['vartype']}',vars='{details['vars']}',category='{details['catg']}',seller='{details['seller']}',quantity='{details['quantity']}',unitprice='{details['cost']}',sellprice='{details['sellprice']}',tax='{details['tax']}',dimension='{dimension}',weight='{weight}',image='{imagename}',date='{todate}' WHERE id = '{product[1]}'")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            return "success"
