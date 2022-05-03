### IMPORTS ###
from inspect import _void
from flask import Flask, redirect ,url_for, render_template, request, session, flash
import psycopg2, psycopg2.extras, datetime, re
from datetime import timedelta, date, datetime


### POSTGRESQL CONFIG ###
db_host = 'ec2-34-193-232-231.compute-1.amazonaws.com'
db_name = 'dcdffat62o43dd'
db_user = 'gahhsnxxsieddf'
db_pw = '5d380f55b8021f5b7a104ef1bd9597c53b921be378f0404dc2104ed883b15576'


### Use Case 1 (LOGIN) ###
class LoginPage:
    def __init__(self) -> None:
        self.controller = LoginPageController()
        self.user_exist = False

    def loginTemplate(self):
        return render_template("login.html")

    def redirectPage(account_type):
        return redirect(url_for(account_type))


class LoginPageController:
    def __init__(self) -> None:
        self.entity = UserAccount()

    def getCredentials(self, request_form) -> bool:
        self.entity.username = request_form["username"]
        self.entity.password = request_form["password"]
        self.entity.account_type = request_form["type"]
        return self.entity.doesUserExist()

    def userExist(self) -> None:
        self.user_exist = True

    def userNotExist(self) -> None:
        self.user_exist = False


class UserAccount:
    def doesUserExist(self) -> bool:
        # connect to db
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                return self.checkDatabase(cursor, db)

    def checkDatabase(self, cursor, db) -> bool:
        # check db - does user exist
        cursor.execute(f"SELECT * FROM users WHERE username = %s AND password = %s AND profile = %s", (self.username, self.password, self.account_type))
        result = cursor.fetchone()
        db.commit()

        if result != None: return True
        else: return False




### Use Case 2 (LOGOUT) ###
class Logout:
    def __init__(self, session) -> None:
        self.session = session
        self.username = session["username"]
        self.controller = LogoutController(self.session, self.username)

    def logUserOut(self):
        self.session = self.controller.editSession(self.session, self.username)
        flash(f"{self.username} logged out!")
        return redirect(url_for("index"))


class LogoutController:
    def __init__(self, session, username) -> None:
        self.session = session
        self.username = session["username"]
        self.entity = UserSession()

    def editSession(self, session, username):
        return self.entity.checkUserInSession(session, username)


class UserSession:
    def checkUserInSession(self, session, username):
        self.session = session
        if "username" in session and session["username"] == username:
            return self.removeUserSession(username)

    def removeUserSession(self, username):
        self.session.pop("username")
        return self.session


### STAFF Use case ###
class StaffPage:
    def __init__(self) -> None:
        self.controller = StaffPageController()
        self.doesCartExist = False

    def staffTemplate(self):
        return render_template("staff.html")
    

class StaffPageController:
    def __init__(self) -> None:
        self.entity = CartDetails()

    def getCart(self,request_form) -> bool:
        self.entity.table_id=request_form["table_id"]
        return self.entity.doesCartExist()

    def cartExist(self) -> None:
        self.entity.doesCartExist = True

    def cartNotExist(self) -> None:
        self.entity.doesCartExist = False

class CartDetails:

    def doesCartExist(self,table_id) -> bool:
        # connect to db
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                return self.checkDatabase(cursor, db,table_id)

    def checkDatabase(self, cursor, db,table_id) -> bool:
        # check db - does cart exist
        print("In database area")
        cursor.execute(f"SELECT o.order_id, o.item_id, o.cart_id, o.name, o.quantity FROM public.""order"" o, cart c WHERE c.cart_id = o.cart_id and c.table_id = %s; ", (table_id, ))
        result = cursor.fetchall()
        
        db.commit()

        if result != None:  
            print ("cart exists")
            #procees to retrieve by calling retrieveCartDetails
            return self.retrieveCartDetails(cursor,db,table_id)
        else: return False

    def retrieveCartDetails(self, cursor, db,table_id):
        print("Inside checkCartDetails1st")
        cursor.execute(f"SELECT o.order_id, o.item_id, o.cart_id, o.name, o.quantity FROM public.""order"" o, cart c WHERE c.cart_id = o.cart_id and c.table_id = %s; ",(table_id, ))
        result = cursor.fetchall()
        db.commit()
        print("Inside checkCartDetails")
        return result

    def getCartDetails(self,table_id) -> _void:
        print("Inside getCartDetails")
        return self.doesCartExist(table_id)
        