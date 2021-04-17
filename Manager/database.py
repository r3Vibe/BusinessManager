# all importd
import mysql.connector
import os
from datetime import date
import uuid

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
        return "#2287655"

    def makePurchaseOrder(self, products):
        if int(products['totoalrow']) == 1:
            orderid = products['orderid']
            vendor = products['vendor']
            date = products['date']
            product = products['product']
            qt = products['qt']
            price = products['price']
            tax = products['tax']
            total = products['sttl']
            print(
                f"Order ID: {orderid} Vendor: {vendor} Date: {date} Product: {product} Quantity: {qt} Price: {price} Tax: {tax} Total: {total}")
        else:
            i = 2
            while i <= int(products['totoalrow']):
                orderid = products[f'orderid']
                vendor = products[f'vendor']
                date = products[f'date']
                product = products[f'product{i}']
                qt = products[f'qt{i}']
                price = products[f'price{i}']
                tax = products[f'tax{i}']
                total = products[f'sttl']
                print(
                    f"Order ID: {orderid} Vendor: {vendor} Date: {date} Product: {product} Quantity: {qt} Price: {price} Tax: {tax} Total: {total}")
                i += 1
                if i > int(products['totoalrow']):
                    break

        return "ok"


class updateDb():
    def addProduct(self, details, imagename):
        print(details)
        today = date.today()
        todate = today.strftime("%m/%d/%y")
        barcode = details['barcode']
        dimension = f"{details['length']}x{details['bredth']}x{details['height']} {details['measure']}"
        weight = f"{details['weight']} {details['weightmeasure']}"
        if barcode == "":
            barcode = "nocode"
        cursor.execute(
            f"INSERT INTO products(name,productid,status,barcode,vartype,vars,category,seller,quantity,unitprice,sellprice,tax,dimension,weight,image,date) VALUES('{details['name']}','{details['productid']}','active','{barcode}','{details['vartype']}','{details['vars']}','{details['catg']}','{details['seller']}','{details['quantity']}','{details['cost']}','{details['sellprice']}','{details['tax']}','{dimension}','{weight}','{imagename}','{todate}')")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            return "success"

    def updateProduct(self, details, proid, imagename):
        product = proid.split('=')
        today = date.today()
        todate = today.strftime("%m/%d/%y")
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
