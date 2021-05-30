# all importd
import mysql.connector
import os
from datetime import date, datetime
import uuid
import xlsxwriter
from fpdf import FPDF

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


class Makepdf2():
    def make(self, details):
        global detailsar
        detailsar = details
        pdf = PDF2()
        pdf.add_page()
        pdf.body()
        try:
            pdf.output(f"./Manager/static/invoices/{detailsar['invid']}.pdf")
        except Exception as e:
            print(e)
            return "error"
        else:
            return "success"


class Makepdf():
    def make(self, details):
        global detailsar
        detailsar = details
        pdf = PDF()
        pdf.add_page()
        pdf.body()
        try:
            pdf.output(f"./Manager/static/invoices/{detailsar['invid']}.pdf")
        except Exception as e:
            print(e)
            return "error"
        else:
            return "success"


class PDF(FPDF):
    def header(self):
        self.set_font('helvetica', '', 30)
        self.cell(w=0, h=10, txt="Rever Design", align="L")

        self.set_font('helvetica', "", 15)
        self.cell(0, 10, "Call:7044287686", ln=1, align="R")
        self.set_font('helvetica', '', 15)
        self.cell(0, 10, "Make Your Dream Design", align="L")
        self.set_font('helvetica', '', 15)
        self.cell(0, 10, "Wapp:7003391137", ln=1, align="R")
        self.set_font('helvetica', '', 15)
        self.cell(0, 10, f"Invoice: {detailsar['invid']}", 0, 0, "L")
        self.cell(0, 10, "Email:reverdesign125@gmail.com", ln=1, align="R")
        self.set_font('helvetica', 'B', 10)
        self.set_fill_color(255, 265, 55)
        self.cell(0, 8, "BILL OF SUPPLY", ln=1,
                  align="C", border=1, fill=True)
        self.ln(3)
        self.set_font('helvetica', '', 25)
        self.cell(0, 10, "Customer Details:-", 0, 1, "L")
        self.set_font('helvetica', '', 15)
        self.cell(
            0, 10, f"Name: {(detailsar['custname']).capitalize()}", 0, 1, "L")
        self.cell(0, 10, f"Contact: {detailsar['phone']}", 0, 1, "L")
        self.cell(
            0, 10, f"Address: {(detailsar['address']).capitalize()}", 0, 1, "L")
        self.ln(3)
    # Page footer

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-40)
        self.set_font('Times', '', 15)
        self.cell(110, 6, "* Terms & Conditions *", 0, 1, "L")
        self.cell(110, 6, "1.lorem ipsom dolor sit amet", 0, 0, "L")
        self.cell(20)
        self.cell(40, 6, "(Autorized Signature)", 0, 1, "C", False)
        self.cell(110, 6, "2.lorem ipsom dolor sit amet", 0, 0, "L")
        self.cell(20)
        self.cell(40, 6, "............................................................",
                  0, 1, "C", False)
        self.cell(110, 6, "3.lorem ipsom dolor sit amet", 0, 1, "L")
        self.ln(4)
        # helvetica italic 8
        self.set_font('helvetica', '', 10)
        self.set_fill_color(255, 265, 55)
        # Page number
        self.cell(
            0, 8, '1st Floor Binapani Market Colony More Barasat kol-700124', 1, 0, 'C', fill=True)

    def body(self):
        if detailsar['totoalrow'] == "1":
            cursor.execute(
                f"SELECT * FROM products WHERE productid = '{(detailsar['product']).capitalize()}'")
            productname = cursor.fetchall()
            self.set_font('Times', '', 12)
            self.set_fill_color(10, 191, 219)
            # header of table
            self.cell(60, 8, "Item", 1, 0, "C", True)
            self.cell(30, 8, "Quantity", 1, 0, "C", True)
            self.cell(35, 8, "Unit Price", 1, 0, "C", True)
            self.cell(30, 8, "Tax (%)", 1, 0, "C", True)
            self.cell(35, 8, "Total Price", 1, 1, "C", True)
            # contrent of table

            self.cell(
                60, 8, f"{(productname[0]['name']).capitalize()}", 1, 0, "C", False)
            self.cell(30, 8, f"{detailsar['quantity']}", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['unitpricef']}", 1, 0, "C", False)
            self.cell(30, 8, f"{productname[0]['tax']}", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['totalpricef']}", 1, 1, "C", False)

            self.set_font('Times', '', 12)
            self.set_fill_color(0, 255, 0)
            self.cell(155, 8, "Grand total", 1, 0, "C", True)
            self.cell(35, 8, f"{detailsar['gto']}", 1, 1, "C", True)
            self.set_font('Times', '', 15)
            self.cell(120)
            self.cell(35, 8, "Payment", 1, 0, "C", False)
            self.cell(
                35, 8, f"{(detailsar['pmode']).capitalize()}", 1, 1, "C", False)
            self.cell(120)
            self.cell(35, 8, "Paid", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['paid']}", 1, 1, "C", False)
            self.cell(120)
            self.cell(35, 8, "Due", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['dues']}", 1, 1, "C", False)
        else:
            cursor.execute(
                f"SELECT * FROM products WHERE productid = '{detailsar['product']}'")
            productname = cursor.fetchall()
            i = 2
            self.set_font('Times', '', 12)
            self.set_fill_color(10, 191, 219)
            # header of table
            self.cell(60, 8, "Item", 1, 0, "C", True)
            self.cell(30, 8, "Quantity", 1, 0, "C", True)
            self.cell(35, 8, "Unit Price", 1, 0, "C", True)
            self.cell(30, 8, "Tax", 1, 0, "C", True)
            self.cell(35, 8, "Total Price", 1, 1, "C", True)
            # first row
            self.cell(60, 8, f"{productname[0]['name']}", 1, 0, "C", False)
            self.cell(30, 8, f"{detailsar['quantity']}", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['unitpricef']}", 1, 0, "C", False)
            self.cell(30, 8, f"{productname[0]['tax']}", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['totalpricef']}", 1, 1, "C", False)
            # next rows
            while i <= int(detailsar['totoalrow']):
                cursor.execute(
                    f"SELECT * FROM products WHERE productid = '{detailsar[f'product{i}']}'")
                productname = cursor.fetchall()
                self.cell(60, 8, f"{productname[0]['name']}", 1, 0, "C", False)
                self.cell(
                    30, 8, f"{detailsar[f'quantity{i}']}", 1, 0, "C", False)
                self.cell(
                    35, 8, f"{detailsar[f'unitpricef{i}']}", 1, 0, "C", False)
                self.cell(30, 8, f"{productname[0]['tax']}", 1, 0, "C", False)
                self.cell(
                    35, 8, f"{detailsar[f'totalpricef{i}']}", 1, 1, "C", False)
                i += 1
            # last part
            self.set_font('Times', '', 12)
            self.set_fill_color(0, 255, 0)
            self.cell(155, 8, "Grand total", 1, 0, "C", True)
            self.cell(35, 8, f"{detailsar['gto']}", 1, 1, "C", True)
            self.set_font('Times', '', 15)
            self.cell(120)
            self.cell(35, 8, "Payment", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['pmode']}", 1, 1, "C", False)
            self.cell(120)
            self.cell(35, 8, "Paid", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['paid']}", 1, 1, "C", False)
            self.cell(120)
            self.cell(35, 8, "Due", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['dues']}", 1, 1, "C", False)


class PDF2(FPDF):
    def header(self):
        self.set_font('helvetica', '', 30)
        self.cell(w=0, h=10, txt="Rever Design", align="L")

        self.set_font('helvetica', "", 15)
        self.cell(0, 10, "Call:7044287686", ln=1, align="R")
        self.set_font('helvetica', '', 15)
        self.cell(0, 10, "Make Your Dream Design", align="L")
        self.set_font('helvetica', '', 15)
        self.cell(0, 10, "Wapp:7003391137", ln=1, align="R")
        self.set_font('helvetica', '', 15)
        self.cell(0, 10, f"Invoice: {detailsar['invid']}", 0, 0, "L")
        self.cell(0, 10, "Email:reverdesign125@gmail.com", ln=1, align="R")
        self.set_font('helvetica', 'B', 10)
        self.set_fill_color(255, 265, 55)
        self.cell(0, 8, "BILL OF SUPPLY", ln=1,
                  align="C", border=1, fill=True)
        self.ln(3)
        self.set_font('helvetica', '', 25)
        self.cell(0, 10, "Customer Details:-", 0, 1, "L")
        self.set_font('helvetica', '', 15)
        self.cell(
            0, 10, f"Name: {(detailsar['custname']).capitalize()}", 0, 1, "L")
        self.cell(0, 10, f"Contact: {detailsar['phone']}", 0, 1, "L")
        self.cell(
            0, 10, f"Address: {(detailsar['address']).capitalize()}", 0, 1, "L")
        self.ln(3)
    # Page footer

    def footer(self):
        # Position at 1.5 cm from bottom
        self.set_y(-40)
        self.set_font('Times', '', 15)
        self.cell(110, 6, "* Terms & Conditions *", 0, 1, "L")
        self.cell(110, 6, "1.lorem ipsom dolor sit amet", 0, 0, "L")
        self.cell(20)
        self.cell(40, 6, "(Autorized Signature)", 0, 1, "C", False)
        self.cell(110, 6, "2.lorem ipsom dolor sit amet", 0, 0, "L")
        self.cell(20)
        self.cell(40, 6, "............................................................",
                  0, 1, "C", False)
        self.cell(110, 6, "3.lorem ipsom dolor sit amet", 0, 1, "L")
        self.ln(4)
        # helvetica italic 8
        self.set_font('helvetica', '', 10)
        self.set_fill_color(255, 265, 55)
        # Page number
        self.cell(
            0, 8, '1st Floor Binapani Market Colony More Barasat kol-700124', 1, 0, 'C', fill=True)

    def body(self):
        if detailsar['totoalrow'] == "1":
            cursor.execute(
                f"SELECT * FROM services WHERE serviceid = '{(detailsar['service'])}'")
            productname = cursor.fetchall()
            self.set_font('Times', '', 12)
            self.set_fill_color(10, 191, 219)
            # header of table
            self.cell(60, 8, "Item", 1, 0, "C", True)
            self.cell(30, 8, "Quantity", 1, 0, "C", True)
            self.cell(35, 8, "Unit Price", 1, 0, "C", True)
            self.cell(30, 8, "Tax (%)", 1, 0, "C", True)
            self.cell(35, 8, "Total Price", 1, 1, "C", True)
            # contrent of table

            self.cell(
                60, 8, f"{(productname[0]['name']).capitalize()}", 1, 0, "C", False)
            self.cell(30, 8, f"{detailsar['quantity']}", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['unitpricef']}", 1, 0, "C", False)
            self.cell(30, 8, f"{productname[0]['tax']}", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['totalpricef']}", 1, 1, "C", False)

            self.set_font('Times', '', 12)
            self.set_fill_color(0, 255, 0)
            self.cell(155, 8, "Grand total", 1, 0, "C", True)
            self.cell(35, 8, f"{detailsar['gto']}", 1, 1, "C", True)
            self.set_font('Times', '', 15)
            self.cell(120)
            self.cell(35, 8, "Payment", 1, 0, "C", False)
            self.cell(
                35, 8, f"{(detailsar['pmode']).capitalize()}", 1, 1, "C", False)
            self.cell(120)
            self.cell(35, 8, "Paid", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['paid']}", 1, 1, "C", False)
            self.cell(120)
            self.cell(35, 8, "Due", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['dues']}", 1, 1, "C", False)
        else:
            cursor.execute(
                f"SELECT * FROM services WHERE serviceid = '{detailsar['service']}'")
            productname = cursor.fetchall()
            i = 2
            self.set_font('Times', '', 12)
            self.set_fill_color(10, 191, 219)
            # header of table
            self.cell(60, 8, "Item", 1, 0, "C", True)
            self.cell(30, 8, "Quantity", 1, 0, "C", True)
            self.cell(35, 8, "Unit Price", 1, 0, "C", True)
            self.cell(30, 8, "Tax", 1, 0, "C", True)
            self.cell(35, 8, "Total Price", 1, 1, "C", True)
            # first row
            self.cell(60, 8, f"{productname[0]['name']}", 1, 0, "C", False)
            self.cell(30, 8, f"{detailsar['quantity']}", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['unitpricef']}", 1, 0, "C", False)
            self.cell(30, 8, f"{productname[0]['tax']}", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['totalpricef']}", 1, 1, "C", False)
            # next rows
            while i <= int(detailsar['totoalrow']):
                cursor.execute(
                    f"SELECT * FROM services WHERE serviceid = '{detailsar[f'service{i}']}'")
                productname = cursor.fetchall()
                self.cell(60, 8, f"{productname[0]['name']}", 1, 0, "C", False)
                self.cell(
                    30, 8, f"{detailsar[f'quantity{i}']}", 1, 0, "C", False)
                self.cell(
                    35, 8, f"{detailsar[f'unitpricef{i}']}", 1, 0, "C", False)
                self.cell(30, 8, f"{productname[0]['tax']}", 1, 0, "C", False)
                self.cell(
                    35, 8, f"{detailsar[f'totalpricef{i}']}", 1, 1, "C", False)
                i += 1
            # last part
            self.set_font('Times', '', 12)
            self.set_fill_color(0, 255, 0)
            self.cell(155, 8, "Grand total", 1, 0, "C", True)
            self.cell(35, 8, f"{detailsar['gto']}", 1, 1, "C", True)
            self.set_font('Times', '', 15)
            self.cell(120)
            self.cell(35, 8, "Payment", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['pmode']}", 1, 1, "C", False)
            self.cell(120)
            self.cell(35, 8, "Paid", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['paid']}", 1, 1, "C", False)
            self.cell(120)
            self.cell(35, 8, "Due", 1, 0, "C", False)
            self.cell(35, 8, f"{detailsar['dues']}", 1, 1, "C", False)


class dbQuery():
    def addPriv(self, pform):
        cursor.execute(f"INSERT INTO privilage(privilage,access) VALUES('{pform['privilage']}','{pform['access']}')")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            return "success"

    def getPrivi(self):
        cursor.execute(f"SELECT * FROM privilage")
        return cursor.fetchall()

    def getEmply(self):
        cursor.execute("SELECT * FROM employee ORDER BY id DESC")
        return cursor.fetchall()

    def getAllrc(self, param):
        if param == "all":
            cursor.execute("SELECT * FROM rechargelist ORDER BY id DESC")
        else:
            cursor.execute(
                f"SELECT * FROM rechargelist WHERE number LIKE '%{param}%'")
        return cursor.fetchall()

    def getCarrier(self):
        cursor.execute("SELECT * FROM commission")
        return cursor.fetchall()

    def addRecharge(self, rc):
        cursor.execute(
            f"SELECT * FROM commission WHERE carrier = '{rc['carrier']}'")
        comm = cursor.fetchall()[0]['comm']
        amount = rc['amount']
        profit = (int(amount)*float(comm))/100
        cursor.execute(
            f"INSERT INTO rechargelist(number,carrier,amount,profit) VALUES('{rc['number']}','{rc['carrier']}','{rc['amount']}','{profit}')")
        today = date.today()
        todate = today.strftime("%d-%m-%Y")
        orderid = dbQuery().generateInvoiceid()
        cursor.execute(
            f"SELECT * FROM customer WHERE phone = '{rc['number']}'")
        available = int(len(cursor.fetchall()))
        if available == 0:
            custname = rc['number']
        elif available > 0:
            custname = cursor.fetchall()[0]['name']
        cursor.execute(
            f"INSERT INTO alldues(date,reference,account,name,amount) VALUES('{todate}','{orderid}','recharge','{custname}','{rc['amount']}')")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            return "success"

    def getCertOrder(self, param):
        cursor.execute(
            f"SELECT * FROM sellorder WHERE invid LIKE '%{param}%' OR status LIKE '%{param}%'  ORDER BY id DESC")
        allOrders = cursor.fetchall()
        return allOrders

    def getSellOrder(self, cid):
        cursor.execute(
            f"SELECT * FROM sellorder WHERE custid = '{cid}' ORDER BY id DESC")
        allOrders = cursor.fetchall()
        return allOrders

    def custUpdate(self, details):
        print(details)
        if details['type'] == "phone":
            cursor.execute(
                f"UPDATE customer SET phone = '{details['number']}', custid = '{details['number']}' WHERE custid = '{details['custid']}'")
            cursor.execute(
                f"UPDATE sellorder SET custid = '{details['number']}' WHERE custid = '{details['custid']}'")
            try:
                db.commit()
            except Exception as e:
                return "error"
            else:
                return "success"
        elif details['type'] == "addr":
            cursor.execute(
                f"UPDATE customer SET address = '{details['address']}' WHERE custid = '{details['custid']}'")
            try:
                db.commit()
            except Exception as e:
                return "error"
            else:
                return "success"

    def getAllCust(self, param):
        if param == "all":
            cursor.execute("SELECT * FROM customer ORDER BY id DESC")
            allcust = cursor.fetchall()
            return allcust
        else:
            cursor.execute(
                f"SELECT * FROM customer WHERE name LIKE '%{param}%' OR custid LIKE '%{param}%' OR phone LIKE '%{param}%' ORDER BY id DESC")
            allcust = cursor.fetchall()
            return allcust

    def changeRefundPolicy(self):
        today = date.today()
        todate = today.strftime("%d-%m-%Y")
        cursor.execute("SELECT * FROM sellorder")
        orders = cursor.fetchall()
        for x in orders:
            orderdate = x['date']
            days1 = int(orderdate.split("-")[0])
            mnt1 = int(orderdate.split("-")[1])
            year1 = int(orderdate.split("-")[2])

            orderDate = date(year1, mnt1, days1)

            days2 = int(todate.split("-")[0])
            mnt2 = int(todate.split("-")[1])
            year2 = int(todate.split("-")[2])

            todaysDate = date(year2, mnt2, days2)

            deltas = todaysDate - orderDate
            if int(deltas.days) > 7:
                cursor.execute(
                    f"UPDATE sellorder SET refundable = 'no' WHERE invid = '{x['invid']}'")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            return "success"

    def refundOrder(self, pid):
        today = date.today()
        todate = today.strftime("%d-%m-%Y")
        cursor.execute(
            f"UPDATE orderprocess SET status = 'Refunded' WHERE orderid = '{pid}'")
        cursor.execute(
            f"UPDATE sellorder SET status = 'Refunded' WHERE invid = '{pid}'")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            cursor.execute(
                f"SELECT * FROM transaction WHERE reference = '{pid}'")
            transaction = cursor.fetchall()
            if int(len(transaction)) == 0:
                cursor.execute(
                    f"DELETE FROM alldues WHERE reference = '{pid}'")
                try:
                    db.commit()
                except Exception as e:
                    return "error"
                else:
                    return "success"
            else:
                cursor.execute(f"SELECT * FROM transaction ORDER BY id DESC")
                lastamnt = int(cursor.fetchall()[0]['balance'])
                debitamt = int(transaction[0]['debit'])
                finalbal = lastamnt - debitamt
                cursor.execute(
                    f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{todate}','{pid}','refund','0','{debitamt}','{finalbal}')")
                try:
                    db.commit()
                except Exception as e:
                    return "error"
                else:
                    cursor.execute(
                        f"SELECT * FROM alldues WHERE reference = '{pid}'")
                    duess = cursor.fetchall()
                    if int(len(duess)) == 0:
                        return "success"
                    else:
                        cursor.execute(
                            f"DELETE FROM alldues WHERE reference = '{pid}'")
                        try:
                            db.commit()
                        except Exception as e:
                            return "error"
                        else:
                            return "success"

    def cancelOrder(self, id):
        today = date.today()
        todate = today.strftime("%d-%m-%Y")
        cursor.execute(
            f"UPDATE orderprocess SET status = 'Cancelled' WHERE orderid = '{id}'")
        cursor.execute(
            f"UPDATE sellorder SET status = 'Cancelled' WHERE invid = '{id}'")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            cursor.execute(
                f"SELECT * FROM transaction WHERE reference = '{id}'")
            transaction = cursor.fetchall()
            if int(len(transaction)) == 0:
                cursor.execute(f"DELETE FROM alldues WHERE reference = '{id}'")
                try:
                    db.commit()
                except Exception as e:
                    return "error"
                else:
                    return "success"
            else:
                cursor.execute(f"SELECT * FROM transaction ORDER BY id DESC")
                lastamnt = int(cursor.fetchall()[0]['balance'])
                debitamt = int(transaction[0]['debit'])
                finalbal = lastamnt - debitamt
                cursor.execute(
                    f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{todate}','{id}','refund','0','{debitamt}','{finalbal}')")
                try:
                    db.commit()
                except Exception as e:
                    return "error"
                else:
                    cursor.execute(
                        f"SELECT * FROM alldues WHERE reference = '{id}'")
                    duess = cursor.fetchall()
                    if int(len(duess)) == 0:
                        return "success"
                    else:
                        cursor.execute(
                            f"DELETE FROM alldues WHERE reference = '{id}'")
                        try:
                            db.commit()
                        except Exception as e:
                            return "error"
                        else:
                            return "success"

    def makeInvoiceforService(self, services):
        # make date in proper formate
        date = services['date']
        dateArr = date.split('-')
        dateArr.reverse()
        newdate = ""
        for x in dateArr:
            newdate += f"{x}-"
        date = newdate.rstrip("-")
        # get customer id
        custid = services['phone']
        # get payment mode
        pmode = services['pmode']
        # get customer name
        custname = services['custname']
        # get invoice id
        orderid = services['invid']
        # check which database to update
        paid = int(services['paid'])
        dues = int(services['dues'])
        if paid == 0:
            # update dues database
            cursor.execute(
                f"INSERT INTO alldues(date,reference,account,name,amount) VALUES('{date}','{orderid}','service','{custname}','{dues}')")
            # sell order db update
            cursor.execute(
                f"INSERT INTO sellorder(pmode,invid,custid,date,status,refundable) VALUES('{pmode}','{orderid}','{custid}','{date}','sold','no')")
            try:
                db.commit()
            except Exception as e:
                return "error"
            else:
                status = Makepdf2().make(services)
                if status == "success":
                    return "success"
                else:
                    return "error"
        elif dues == 0:
            # find current balance
            cursor.execute("SELECT * FROM transaction ORDER BY id DESC")
            balance = int(cursor.fetchall()[0]['balance'])
            newbalance = balance + paid
            # update transactions db
            cursor.execute(
                f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{date}','{orderid}','service','{paid}','0','{newbalance}')")
            # sell order db update
            cursor.execute(
                f"INSERT INTO sellorder(pmode,invid,custid,date,status,refundable) VALUES('{pmode}','{orderid}','{custid}','{date}','sold','no')")
            try:
                db.commit()
            except Exception as e:
                return "error"
            else:
                status = Makepdf2().make(services)
                if status == "success":
                    return "success"
                else:
                    return "error"
        else:
            # find current balance
            cursor.execute("SELECT * FROM transaction ORDER BY id DESC")
            balance = int(cursor.fetchall()[0]['balance'])
            newbalance = balance + paid
            # update transactions db
            cursor.execute(
                f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{date}','{orderid}','service','{paid}','0','{newbalance}')")
            # sell order db update
            cursor.execute(
                f"INSERT INTO sellorder(pmode,invid,custid,date,status,refundable) VALUES('{pmode}','{orderid}','{custid}','{date}','sold','no')")
            # update dues database
            cursor.execute(
                f"INSERT INTO alldues(date,reference,account,name,amount) VALUES('{date}','{orderid}','service','{custname}','{dues}')")
            try:
                db.commit()
            except Exception as e:
                return "error"
            else:
                status = Makepdf2().make(services)
                if status == "success":
                    return "success"
                else:
                    return "error"

    def getServices(self):
        cursor.execute("SELECT * FROM services")
        allServ = cursor.fetchall()
        return allServ

    def checkQtStat(self):
        cursor.execute(
            "UPDATE products SET status = 'stopped' WHERE quantity = 0")
        try:
            db.commit()
        except Exception as e:
            print(e)
            return False
        else:
            cursor.execute(
                "UPDATE products SET status = 'active' WHERE quantity > 5")
            try:
                db.commit()
            except Exception as e:
                print(e)
                return False
            else:
                cursor.execute(
                    "UPDATE products SET status = 'attention' WHERE quantity <= 5 AND quantity > 0")
                try:
                    db.commit()
                except Exception as e:
                    print(e)
                    return False
                else:
                    return True

    def markAsSold(self, invoice):
        # get product id and quantity
        cursor.execute(
            f"SELECT * FROM orderprocess WHERE orderid = '{invoice}'")
        details = cursor.fetchall()[0]
        products = details['product']
        quantity = details['quantity']
        singleProd = products.split(":")
        singleQt = quantity.split(":")
        i = 0
        # update quantity from database
        while i < len(singleProd):
            # get current quantity iof product
            cursor.execute(
                f"SELECT * FROM products WHERE productid = '{singleProd[i]}'")
            currentqt = int(cursor.fetchall()[0]['quantity'])
            newqt = currentqt - int(singleQt[i])
            cursor.execute(
                f"UPDATE products SET quantity = '{newqt}' WHERE productid = '{singleProd[i]}'")
            print(f"{singleProd[i]}:{singleQt[i]}")
            i += 1
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            cursor.execute(
                f"UPDATE sellorder SET status = 'sold' WHERE invid = '{invoice}'")
            cursor.execute(
                f"UPDATE orderprocess SET status = 'sold' WHERE orderid = '{invoice}'")
            try:
                db.commit()
            except Exception as e:
                return "error"
            else:
                return "success"
        # # get current quantity
        # cursor.execute("SELECT * FROM products WHERE productid = {}")

    def checkAvailable(self, details):
        rows = int(details['totoalrow'])
        if rows == 1:
            quantity = details['quantity']
            product = details['product']
            cursor.execute(
                f"SELECT * FROM products WHERE productid = '{product}'")
            quantityatdb = cursor.fetchall()[0]['quantity']
            if int(quantity) > int(quantityatdb):
                return "error"
            else:
                return "success"
        else:
            quantity = details['quantity']
            product = details['product']
            cursor.execute(
                f"SELECT * FROM products WHERE productid = '{product}'")
            quantityatdb = cursor.fetchall()[0]['quantity']
            if int(quantity) > int(quantityatdb):
                return "error"
            else:
                i = 2
                while i <= int(rows):
                    quantity = details[f'quantity{i}']
                    product = details[f'product{i}']
                    cursor.execute(
                        f"SELECT * FROM products WHERE productid = '{product}'")
                    quantityatdb = cursor.fetchall()[0]['quantity']

                    i += 1
                    if int(quantity) > int(quantityatdb):
                        return "error"
                return "success"

    def getInvoices(self, param):
        if param == "all":
            cursor.execute(f"SELECT * FROM sellorder ORDER BY id DESC")
            allinv = cursor.fetchall()
            return allinv
        else:
            cursor.execute(
                f"SELECT * FROM sellorder WHERE invid LIKE '%{param}%' OR custid LIKE '%{param}%'")
            allinv = cursor.fetchall()
            return allinv

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
        # make date in proper formate
        date = product['date']
        dateArr = date.split('-')
        dateArr.reverse()
        newdate = ""
        for x in dateArr:
            newdate += f"{x}-"
        date = newdate.rstrip("-")
        # get customer id
        custid = product['phone']
        # get payment mode
        pmode = product['pmode']
        # get customer name
        custname = product['custname']
        # get invoice id
        orderid = product['invid']
        # make single string product and quantity
        rows = int(product['totoalrow'])
        if rows == 1:
            productid = product['product']
            productqt = product['quantity']
        else:
            i = 2
            productid = product['product']
            productqt = product['quantity']
            while i <= rows:
                productid += f":{product[f'product{i}']}"
                productqt += f":{product[f'quantity{i}']}"
                i += 1
        # update orderlist database
        cursor.execute(
            f"INSERT INTO orderprocess(orderid,product,quantity,status) VALUES('{orderid}','{productid}','{productqt}','Processing')")
        try:
            db.commit()
        except Exception as e:
            return "error"
        else:
            # check which database to update
            paid = int(product['paid'])
            dues = int(product['dues'])
            if paid == 0:
                # update dues database
                cursor.execute(
                    f"INSERT INTO alldues(date,reference,account,name,amount) VALUES('{date}','{orderid}','sale','{custname}','{dues}')")
                # sell order db update
                cursor.execute(
                    f"INSERT INTO sellorder(pmode,invid,custid,date,status,refundable) VALUES('{pmode}','{orderid}','{custid}','{date}','Processing','yes')")
                try:
                    db.commit()
                except Exception as e:
                    return "error"
                else:
                    status = Makepdf().make(product)
                    if status == "success":
                        return "success"
                    else:
                        return "error"
            elif dues == 0:
                # find current balance
                cursor.execute("SELECT * FROM transaction ORDER BY id DESC")
                balance = int(cursor.fetchall()[0]['balance'])
                newbalance = balance + paid
                # update transactions db
                cursor.execute(
                    f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{date}','{orderid}','sale','{paid}','0','{newbalance}')")
                # sell order db update
                cursor.execute(
                    f"INSERT INTO sellorder(pmode,invid,custid,date,status,refundable) VALUES('{pmode}','{orderid}','{custid}','{date}','Processing','yes')")
                try:
                    db.commit()
                except Exception as e:
                    return "error"
                else:
                    status = Makepdf().make(product)
                    if status == "success":
                        return "success"
                    else:
                        return "error"
            else:
                # find current balance
                cursor.execute("SELECT * FROM transaction ORDER BY id DESC")
                balance = int(cursor.fetchall()[0]['balance'])
                newbalance = balance + paid
                # update transactions db
                cursor.execute(
                    f"INSERT INTO transaction(date,reference,account,debit,credit,balance) VALUES('{date}','{orderid}','sale','{paid}','0','{newbalance}')")
                # sell order db update
                cursor.execute(
                    f"INSERT INTO sellorder(pmode,invid,custid,date,status,refundable) VALUES('{pmode}','{orderid}','{custid}','{date}','Processing','yes')")
                # update dues database
                cursor.execute(
                    f"INSERT INTO alldues(date,reference,account,name,amount) VALUES('{date}','{orderid}','sale','{custname}','{dues}')")
                try:
                    db.commit()
                except Exception as e:
                    return "error"
                else:
                    status = Makepdf().make(product)
                    if status == "success":
                        return "success"
                    else:
                        return "error"

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
        day = d.strftime("%d")
        time = d.strftime('%H%M%S')
        return f"Inv-{day}-{monthasnum}-{time}"

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
            cursor.execute("SELECT * FROM alldues ORDER BY id DESC")
            alltrans = cursor.fetchall()
            return alltrans
        else:
            cursor.execute(
                f"SELECT * FROM alldues WHERE name LIKE '%{param}%'")
            alltrans = cursor.fetchall()
            return alltrans

    def getTransaction(self, param):
        if param == "all":
            cursor.execute("SELECT * FROM transaction ORDER BY id DESC")
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
        cursor.execute("SELECT * FROM products ORDER BY id DESC")
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
        tax = product[0]['tax']
        price = product[0]['sellprice']
        return f"{price}:{tax}"

    def getServ(self, pid):
        print(pid)
        cursor.execute(
            f"SELECT * FROM services WHERE serviceid = '{pid}'")
        service = cursor.fetchall()
        print(service)
        tax = service[0]['tax']
        price = service[0]['price']
        return f"{price}:{tax}"

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
        d = datetime.now()
        monthasnum = d.strftime("%m")
        day = d.strftime("%d")
        time = d.strftime('%H%M%S')
        return f"Ord-{day}-{monthasnum}-{time}"

    def getCurrentOrders(self, parameter):
        if parameter == 'all':
            cursor.execute(f"SELECT * FROM purchaseorder ORDER BY id DESC")
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
            date = products['date']
            dateArr = date.split('-')
            dateArr.reverse()
            newdate = ""
            for x in dateArr:
                newdate += f"{x}-"
            date = newdate.rstrip("-")
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
