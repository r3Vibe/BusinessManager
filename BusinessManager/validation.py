from BusinessManager.database import cursor, db, dbQuery
from werkzeug.security import check_password_hash
from datetime import datetime
# user validation


class validateUser():
    def __init__(self, username, password):
        self.username = username
        self.password = password

    def validateNow(self):
        cursor.execute(
            f"SELECT * FROM employee WHERE username = '{self.username}'")
        user = cursor.fetchall()
        if len(user) < 1:
            return "error1"
        else:
            password = user[0]['password']
            attempt = user[0]['attempt']
            if check_password_hash(password, self.password):
                if attempt >= 3:
                    lastlogin = user[0]['lastlogin']
                    now = datetime.now()
                    time = now.strftime("%H:%M:%S")
                    FMT = '%H:%M:%S'
                    difference = datetime.strptime(
                        lastlogin, FMT) - datetime.strptime(time, FMT)
                    if (str(difference) >= '0:30:00'):
                        cursor.execute(
                            f"UPDATE employee SET attempt = '0' WHERE username = '{self.username}'")
                        db.commit()
                        now = datetime.now()
                        time = now.strftime("%H:%M:%S")
                        cursor.execute(
                            f"UPDATE employee SET lastlogin = '{time}' WHERE username = '{self.username}'")
                        db.commit()
                        return {"username": user[0]['username'], "role": user[0]['role']}
                    else:
                        return "error3"
                else:
                    now = datetime.now()
                    time = now.strftime("%H:%M:%S")
                    cursor.execute(
                        f"UPDATE employee SET lastlogin = '{time}' WHERE username = '{self.username}'")
                    db.commit()
                    return {"username": user[0]['username'], "role": user[0]['role']}
            else:
                cursor.execute(
                    f"SELECT * FROM employee WHERE username = '{self.username}'")
                query = cursor.fetchall()
                attempt = query[0]['attempt']
                if attempt >= 3:
                    return "error3"
                else:
                    newattempt = int(attempt) + 1
                    cursor.execute(
                        f"UPDATE employee SET attempt = '{newattempt}' WHERE username = '{self.username}'")
                    db.commit()
                    return "error2"


class validateProduct():
    def __init__(self, product, files):
        self.productImage = files['image'].filename
        self.productName = product['name']
        self.productId = product['productid']
        self.barcode = product['barcode']
        self.quantity = product['quantity']
        self.cost = product['cost']
        self.sellprice = product['sellprice']
        self.tax = product['tax']
        self.length = product['length']
        self.bredth = product['bredth']
        self.height = product['height']
        self.weight = product['weight']

    def startValidation(self):
        # image validation
        allowed = ['jpeg', 'jpg', 'png']
        ext = self.productImage.split('.')
        if len(ext) > 2:
            return "error1"
        elif ext[1].lower() not in allowed:
            return "error2"
        # file size validation add later
        # check if product already added to inventory
        elif len(dbQuery().checkPid(self.productId)) >= 1:
            return "error3"
        else:
            return "success"

    def imageValidate(self):
        # image validation
        allowed = ['jpeg', 'jpg', 'png']
        ext = self.productImage.split('.')
        if len(ext) > 2:
            return "error1"
        elif ext[1].lower() not in allowed:
            return "error2"
        else:
            return "success"
