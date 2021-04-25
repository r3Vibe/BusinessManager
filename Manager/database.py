# all importd
import mysql.connector
import os
from datetime import date
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

            # update purchaseorder database
            cursor.execute(
                f"INSERT INTO purchaseorder(orderid,vendor,date,status) VALUES('{orderid}','{vendor}','{date}','processing')")
            cursor.execute(
                f"INSERT INTO orderprocess(orderid,product,quantity) VALUES('{orderid}','{product}','{qt}')")
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

            # update purchaseorder database
            cursor.execute(
                f"INSERT INTO purchaseorder(orderid,vendor,date,status) VALUES('{orderid}','{vendor}','{date}','processing')")
            cursor.execute(
                f"INSERT INTO orderprocess(orderid,product,quantity) VALUES('{orderid}','{prodDb}','{qtDb}')")
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
