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


class updateDb():
    def addProduct(self, details, imagename):
        today = date.today()
        todate = today.strftime("%m/%d/%y")
        barcode = details['barcode']
        dimension = f"{details['length']}x{details['bredth']}x{details['height']} {details['measure']}"
        weight = f"{details['weight']} {details['weightmeasure']}"
        if barcode == "":
            barcode = "nocode"
        cursor.execute(
            f"INSERT INTO products(name,productid,barcode,vartype,vars,category,seller,quantity,unitprice,sellprice,tax,dimension,weight,image,date) VALUES('{details['name']}','{details['productid']}','{barcode}','{details['vartype']}','{details['vars']}','{details['catg']}','{details['seller']}','{details['quantity']}','{details['cost']}','{details['sellprice']}','{details['tax']}','{dimension}','{weight}','{imagename}','{todate}')")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            return "success"
