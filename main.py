### MODULE IMPORTS ###
from flask import Flask, redirect ,url_for, render_template, request, session, flash
import psycopg2, psycopg2.extras, datetime, re
from datetime import timedelta, date, datetime, time
from classes import * # import all classes from classes.py


### POSTGRESQL CONFIG ###
db_host = 'ec2-34-193-232-231.compute-1.amazonaws.com'
db_name = 'dcdffat62o43dd'
db_user = 'gahhsnxxsieddf'
db_pw = '5d380f55b8021f5b7a104ef1bd9597c53b921be378f0404dc2104ed883b15576'


### SESSION CONFIG (password & period) ###
app = Flask(__name__)
app.secret_key = "duck_rice"
app.permanent_session_lifetime = timedelta(minutes=60)


### LOGIN PAGE ###
@app.route("/", methods=["GET", "POST"])
def index():
    boundary = LoginPage()
    if request.method == "GET":
        return boundary.loginTemplate() # A-B

    elif request.method == "POST":
        if boundary.controller.getCredentials(request.form): # B-C, C-E

            # login success - add username & account_type in session
            session["username"] = request.form["username"]
            session["account_type"] = request.form["type"]

            # redirect page to manager, staff, owner or admin
            return LoginPage.redirectPage(session["account_type"]) # C-B

        else:
            flash(request.form["username"] + " login failed!")
            return boundary.loginTemplate() # redirect to login page


### LOGOUT (TO APPLY BCE) ###
@app.route("/logOut")
def logOut():
    boundary = Logout(session)
    return boundary.logUserOut()


### OTHER CREATED PROFILE PAGE ###
@app.route("/<type>")
def otherProfiles(type):
    username = session["username"]
    return render_template("otherProfiles.html", username=username, type=type)

### MANAGER PAGE ###
@app.route("/manager", methods=["GET", "POST"])
def manager():
    if request.method == "GET":
        return render_template("manager.html")

    elif request.method == "POST":
        if request.form["button_type"] == "a1":
            return redirect(url_for("managerviewItem"))
        elif request.form["button_type"] == "a3":
            return redirect(url_for("managerupdateItem"))
        elif request.form["button_type"] == "a4":
            return redirect(url_for("managercreateItem"))
        elif request.form["button_type"] == "a5":
            return redirect(url_for("managerdeleteItem"))
        elif request.form["button_type"] == "a6":
            return redirect(url_for("managerviewCoupon"))
        elif request.form["button_type"] == "a7":
            return redirect(url_for("managersearchCoupon"))
        elif request.form["button_type"] == "a8":
            return redirect(url_for("managerupdateCoupon"))
        elif request.form["button_type"] == "a9":
            return redirect(url_for("managercreateCoupon"))
        elif request.form["button_type"] == "a10":
            return redirect(url_for("managerdeleteCoupon"))
        return render_template("manager.html")

@app.route("/manager/managerviewItem", methods=["GET", "POST"])
def managerviewItem():
    if request.method == "GET":
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM menuitems ORDER BY item_id ASC")
                query = cursor.fetchall()
                ##print(query)
        return render_template("managerviewitem.html", query=query)

    elif request.method == "POST":
        item_name = request.form["itemname"].upper()

        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM menuitems WHERE upper(name) like '{}%'".format(item_name))
                query = cursor.fetchall()
                print(query)

        return render_template("managerviewitem.html", query=query)

@app.route("/manager/managerupdateItem", methods=["GET", "POST"])
def managerupdateItem():
    if request.method == "GET":
         with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM menuitems ORDER BY item_id ASC")
                query = cursor.fetchall()
         return render_template("managerupdateitem.html" , query=query)
    elif request.method == "POST":
        item_name = request.form["itemname2"]
        item_price = request.form["itemprice2"]
        item_id = request.form["item2"]
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
             with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor2:
                 cursor2.execute("UPDATE menuitems SET name = '{}', price = {} WHERE item_id = {}".format(item_name, item_price, item_id))
             with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor3:
                cursor3.execute("SELECT * FROM menuitems ORDER BY item_id ASC")
                query = cursor3.fetchall()
        db.commit()
        return render_template("managerupdateitem.html" , query=query)



@app.route("/manager/managercreateItem", methods=["GET", "POST"])
def managercreateItem():
    if request.method == "GET":
         with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM menuitems ORDER BY item_id ASC")
                query = cursor.fetchall()
         return render_template("managercreateitem.html" , query=query)
    elif request.method == "POST":
        item_name = request.form["itemname3"]
        item_price = request.form["itemprice3"]
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
             with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor2:
                 cursor2.execute("INSERT INTO menuitems (name, price, ordered_count) VALUES (%s, %s, 0)", (item_name, item_price))
             with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor3:
                cursor3.execute("SELECT * FROM menuitems ORDER BY item_id ASC")
                query = cursor3.fetchall()
        db.commit()
        return render_template("managerviewitem.html" , query=query)




@app.route("/manager/managerdeleteItem", methods=["GET", "POST"])
def managerdeleteItem():
    if request.method == "GET":
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM menuitems ORDER BY item_id ASC")
                query = cursor.fetchall()
        return render_template("managerdeleteitem.html" , query=query)
    elif request.method == "POST":
        item_id = request.form["item4"]
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor2:
                cursor2.execute("DELETE FROM menuitems WHERE item_id = {}".format(item_id))
                db.commit()
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor3:
                cursor3.execute("SELECT * FROM menuitems ORDER BY item_id ASC")
                query = cursor3.fetchall()

        return render_template("managerdeleteitem.html",  query=query)



@app.route("/manager/managerviewCoupon", methods=["GET", "POST"])
def managerviewCoupon():
    if request.method == "GET":
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM coupon ORDER BY coupon_id ASC")
                query = cursor.fetchall()
                ##print(query)
        return render_template("managerviewcoupon.html", query=query)

    elif request.method == "POST":
        coupon_name = request.form["couponname"].upper()

        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM coupon WHERE upper(name) like '{}%'".format(coupon_name))
                query = cursor.fetchall()
                print(query)

        return render_template("managerviewcoupon.html", query=query)


@app.route("/manager/managerupdateCoupon", methods=["GET", "POST"])
def managerupdateCoupon():
    if request.method == "GET":
         with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM coupon ORDER BY coupon_id ASC")
                query = cursor.fetchall()
         return render_template("managerupdatecoupon.html" , query=query)
    elif request.method == "POST":
        coupon_id = request.form["couponid4"]
        coupon_name = request.form["couponname4"]
        valid_from = request.form["validfrom4"]
        valid_till = request.form["validtill4"]
        discount_percent = request.form["coupondiscount4"]
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
             with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor2:
                 cursor2.execute("UPDATE coupon SET name = '{}', valid_from = '{}', valid_till = '{}', discount_percent = {} WHERE coupon_id = {}".format(coupon_name, valid_from, valid_till, discount_percent, coupon_id))
             with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor3:
                cursor3.execute("SELECT * FROM coupon ORDER BY coupon_id ASC")
                query = cursor3.fetchall()
        db.commit()
        return render_template("managerupdatecoupon.html" , query=query)



@app.route("/manager/managercreateCoupon", methods=["GET", "POST"])
def managercreateCoupon():
    if request.method == "GET":
         with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM coupon ORDER BY coupon_id ASC")
                query = cursor.fetchall()
         return render_template("managercreatecoupon.html" , query=query)
    elif request.method == "POST":
        coupon_name = request.form["couponname3"]
        valid_from = request.form["validfrom3"]
        valid_till = request.form["validtill3"]
        discount_percent = request.form["coupondiscount3"]
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
             with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor2:
                 cursor2.execute("INSERT INTO coupon (name, valid_from, valid_till, discount_percent) VALUES (%s, %s, %s, %s)", (coupon_name, valid_from, valid_till, discount_percent))
             with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor3:
                cursor3.execute("SELECT * FROM coupon ORDER BY coupon_id ASC")
                query = cursor3.fetchall()
        db.commit()
        return render_template("managercreatecoupon.html" , query=query)

@app.route("/manager/managerdeleteCoupon", methods=["GET", "POST"])
def managerdeleteCoupon():
    if request.method == "GET":
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                cursor.execute("SELECT * FROM coupon ORDER BY coupon_id ASC")
                query = cursor.fetchall()
        return render_template("managerdeletecoupon.html" , query=query)
    elif request.method == "POST":
        coupon_id = request.form["couponID4"]
        with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor2:
                cursor2.execute("DELETE FROM coupon WHERE coupon_id = {}".format(coupon_id))
                db.commit()
            with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor3:
                cursor3.execute("SELECT * FROM coupon ORDER BY coupon_id ASC")
                query = cursor3.fetchall()

        return render_template("managerdeletecoupon.html",  query=query)


### STAFF PAGE (TO DO) ###
@app.route("/staff", methods=["GET", "POST"])
def staff():
    #if request.method == "GET":
    #    return render_template("staff.html")
    boundary = StaffPage()
    if request.method == "GET":
        print("In GET")
        return boundary.staffTemplate() # A-B
    if request.method == "POST":
        if request.form["button_type"] == "b1":
            return redirect(url_for('viewCart'))
        if request.form["button_type"] == "b2":
            return redirect(url_for('fufillOrders'))

#-----View Cart----#
@app.route("/staff/ViewCart", methods=["GET", "POST"])
def viewCart():
    boundary = StaffPage()
    if request.method == "GET":
        print("IN GET FOR viewCart()")
        return render_template("staffViewCart.html", data=boundary.controller.getCart())
    if request.method == "POST":
        print("IN POST for viewCart()")
        get_cart_id = request.form["cart_id"]
        session['cartId'] = get_cart_id
        return redirect(url_for('viewOrders',data=boundary.controller.getOrders(get_cart_id)))

#-----View Orders----#
@app.route("/staff/ViewCart/ViewOrders", methods=["GET", "POST"])
def viewOrders():
    boundary = StaffPage()
    if request.method == "GET":
        all_data = request.args.getlist('data')
        print(all_data)
        new_data = []
        for i in all_data:
            all_data_array = i[1:-1].split(', ')
            all_data_array[0] = int(all_data_array[0])
            all_data_array[1] = all_data_array[1][1:-1]
            new_data.append(all_data_array)
        print(new_data)
        #get_cart_id= request.args.get('current_cart_id')
        print("Now in GET for viewOrders")
        print("In session cart_id = " + str(session['cartId']))

        return render_template("staffViewOrders.html",data=new_data)
    if request.method == "POST":
        #get_cart_id = request.form["cart_id"]
        if request.form["button_type"] == "button_confirm_edit":
            order_id = request.form["order_id"]
            item_name = request.form["item_name"]
            item_quantity = request.form["item_quantity"]
            print("Now in POST for ViewOrders")
            print("current cart: " + str(session['cartId']))
            #boundary.controller.editOrders(get_cart_id,order_id,item_name,item_quantity)
            #all_data = request.args.getlist('data')
            return redirect(url_for('viewOrders',data=boundary.controller.updateOrder(session['cartId'],order_id,item_name,item_quantity)))
        if request.form["button_type"] == "button_delete":
            order_id = request.form["order_id"]
            print("In delete main.py")
            return redirect(url_for('viewOrders',data=boundary.controller.deleteOrder(session['cartId'],order_id)))
            ##Do insert over the weekend and fulfillorder
        if request.form["button_type"] == "button_insert":
            print("in insert main.py")
            insert_item_id = request.form["insert_item_id"]
            insert_item_name = request.form["insert_item_name"]
            insert_item_quantity = request.form["insert_item_quantity"]
            insert_item_price = request.form["insert_item_price"]
            print("Before is_it_fulfilled")
            insert_is_it_fulfilled = request.form.get("insert_is_it_fulfilled")
            print("After requestform...")
            return redirect(url_for('viewOrders',data=boundary.controller.insertOrder(session['cartId'],insert_item_id,insert_item_name,insert_item_quantity,insert_item_price,insert_is_it_fulfilled)))

#-----fulfill Orders----# NOT DONE!!
@app.route("/staff/fulfillOrders", methods=["GET", "POST"])
def fufillOrders():
    boundary = StaffPage()
    if request.method == "GET":
        return render_template("staffFulfillOrders.html", data=boundary.controller.getCart())






### OWNER PAGE (TO DO) ###
@app.route("/owner", methods=["GET", "POST"])
def owner():
    boundary = OwnerPage()
    if request.method == "GET":
        return boundary.ownerHomePage()

    elif request.method == "POST":
        return boundary.buttonClicked(request.form)


#-----Owner functions----#
@app.route("/owner/HourlyAvgSpending", methods=["GET", "POST"])
def display_H_avg_spend():
    boundary = OwnerPage()
    if request.method == "GET":
        return boundary.getDatePage()

    else:
        date_request = request.form["calendar"]
        data = boundary.controller.getHourlySpending(date_request)
        return boundary.displayHourlySpendingReport(date_request, data)




@app.route("/owner/DailyAvgSpending", methods=["GET", "POST"])
def display_D_avg_spend():
    boundary = OwnerPage()
    if request.method == "GET":
        return boundary.getDatePage()

    else:
        date_request = request.form["calendar"]
        date_split = date_request.split('-')
        year = int(date_split[0])
        month = int(date_split[1])
        day = int(date_split[2])


        start = datetime(year, month, day, 12, 0, 0)
        end = start + timedelta(hours=6)
        data = boundary.controller.getDailySpending(start, end)
        #print(data)
        dates = []
        for i in range(7):
            temp = str(start).split(" ")[0]
            dates.append(temp)
            start = start - timedelta(days =1)

        #print(dates)
        to_read = zip(dates,data)
        return boundary.displayDailySpendingReport(date_request, to_read)



@app.route("/owner/WeeklyAvgSpending", methods=["GET", "POST"])
def display_W_avg_spend():
    boundary = OwnerPage()
    if request.method == "GET":
        return boundary.getWeeklyDatePage()

    else:
        week_requested = request.form["calendar"] # "2022-W18"
        year = int(week_requested.split("-")[0])
        week = int(week_requested.split("W")[1])

        start_of_week = datetime(year,1,3,12,0,0) + timedelta(weeks=week-1)
        end_of_week = start_of_week + timedelta(days= 6)

        start_date = str(start_of_week).split(" ")[0] #2022-05-06
        end_date =  str(end_of_week).split(" ")[0]

        end = start_of_week + timedelta(hours=6)
        data = boundary.controller.getWeeklySpending(start_of_week, end)
        #print(data)
        dates = []
        for i in range(7):
            temp = str(start_of_week).split(" ")[0]
            dates.append(temp)
            start_of_week = start_of_week + timedelta(days =1)
        #print(dates)

        totalRev = 0
        totalCust = 0
        for row in range(len(data)):
            totalRev += data[row][0]
            totalCust += data[row][1]

        to_read = zip(dates, data)
        return boundary.displayWeeklySpendingReport(week_requested, start_date, end_date, to_read, totalRev, totalCust)

@app.route("/owner/HourlyFrequency", methods=["GET", "POST"])
def display_H_frequency():
    boundary = OwnerPage()
    if request.method == "GET":
        return boundary.getDatePage()

    elif request.method == "POST":
        date_request = request.form["calendar"]
        date_split = date_request.split('-')
        year = int(date_split[0])
        month = int(date_split[1])
        day = int(date_split[2])

        data = boundary.controller.getHourlyFrequency(year,month,day)
        return boundary.displayHourlyFrequencyReport(date_request, data)

@app.route("/owner/DailyFrequency", methods=["GET", "POST"])
def display_D_frequency():
    boundary = OwnerPage()
    if request.method == "GET":
        return boundary.getDatePage()

    elif request.method == "POST":
        date_request = request.form["calendar"]
        date_split = date_request.split('-')
        year = int(date_split[0])
        month = int(date_split[1])
        day = int(date_split[2])

        #print(month)
        start = datetime(year, month, day, 12, 0, 0)
        end = start + timedelta(hours=6)
        data = boundary.controller.getDailyFrequency(start, end)

        dates = []
        for i in range(7):
            temp = str(start).split(" ")[0]
            dates.append(temp)
            start = start - timedelta(days =1)

        to_read = zip(dates, data)
        return boundary.displayDailyFrequencyReport(date_request, to_read)

@app.route("/owner/WeeklyFrequency", methods=["GET", "POST"])
def display_W_frequency():
    boundary = OwnerPage()
    if request.method == "GET":
        return boundary.getWeeklyDatePage()

    else:
        week_requested = request.form["calendar"] # "2022-W18"
        year = int(week_requested.split("-")[0])
        week = int(week_requested.split("W")[1])

        start_of_week = datetime(year,1,3,0,0,0) + timedelta(weeks=week-1) #2022-05-06 00:00:00
        end_of_week = start_of_week + timedelta(days= 6, hours= 23, minutes=59, seconds=59)

        #print(start_of_week)
        #print(end_of_week)

        start_date = str(start_of_week).split(" ")[0] #2022-05-06
        end_date =  str(end_of_week).split(" ")[0]
        #print(start_date)

        date_split = start_date.split('-')
        year = int(date_split[0])
        month = int(date_split[1])
        day = int(date_split[2])
        start = datetime(year, month, day, 12, 0, 0)
        end = start + timedelta(hours=7)


        data = boundary.controller.getWeeklyFrequency(start,end)
        total = 0
        for row in range(len(data)):
            total += data[row][0]
        print(data)
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        to_read = zip(days, data)

        return boundary.displayWeeklyFrequencyReport(week_requested,start_date,end_date,to_read,total)

@app.route("/owner/HourlyPreference", methods=["GET", "POST"])
def display_H_preference():
    boundary = OwnerPage()
    if request.method == "GET":
        return boundary.hourlyPreferencePage()

    elif request.method == "POST":
        ddmmyy = request.form["birthday"] # "2022-05-30"

        # convert "2022-05-30" to datetime object
        ddmmyy = ddmmyy.split("-") # ['2022', '05', '30']
        year = int(ddmmyy[0]) # 2022
        month = int(ddmmyy[1]) # 05
        day = int(ddmmyy[2]) # 30

        list = boundary.controller.getHourlyPreferenceData(year, month, day)
        return boundary.preferenceResultPage(year, month, day, list)


@app.route("/owner/DailyPreference", methods=["GET", "POST"])
def display_D_preference():
    boundary = OwnerPage()
    if request.method == "GET":
        return boundary.dailyPreferencePage()

    elif request.method == "POST":
        ddmmyy = request.form["birthday"] # "2022-05-30"
        ddmmyy = ddmmyy.split("-") # ['2022', '05', '30']
        year = int(ddmmyy[0]) # 2022
        month = int(ddmmyy[1]) # 05
        day = int(ddmmyy[2]) # 30

        result = dailyFoodPreference(year, month, day)
        return render_template("DailyPreferenceResult.html", year=year, month=month, day=day, result=result)



@app.route("/owner/WeeklyPreference", methods=["GET", "POST"])
def display_W_preference():
    boundary = OwnerPage()
    if request.method == "GET":
        return boundary.weeklyPreferencePage()

    elif request.method == "POST":
        ddmmyy = request.form["birthday"] # "2022-W18"
        year = int(ddmmyy.split("-")[0])
        week = int(ddmmyy.split("W")[1])

        start_of_week = datetime(year,1,3,0,0,0) + timedelta(weeks=week)
        end_of_week = start_of_week + timedelta(weeks=1)

        string_start = str(start_of_week).split(" ")[0]
        string_end = str(end_of_week).split(" ")[0]

        result = weeklyFoodPreference(year, week)

        return render_template("WeeklyPreferenceResult.html", week=week, year=year, start=string_start, end=string_end, result=result)



def dailyFoodPreference(year:int, month:int, day:int) -> list:
    with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
        with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            start = datetime(year, month, day, 0, 0, 0)
            end = datetime(year, month, day, 23, 59, 59)

            cursor.execute("SELECT name, quantity from public.\"order\" WHERE ordered_time between '{}' and '{}'".format(start, end))
            name_quantity = cursor.fetchall()

            name_quantity_dictionary = {}
            for pair in name_quantity:
                item_name = pair[0]
                item_quantity = pair[1]
                if item_name in name_quantity_dictionary:
                    name_quantity_dictionary[item_name] += item_quantity
                else:
                    name_quantity_dictionary[item_name] = item_quantity

            name_quantity_descending = sorted(name_quantity_dictionary.items(), key=lambda x:x[1], reverse=True)
            return name_quantity_descending


def weeklyFoodPreference(year:int, week:int) -> list:
    with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
        with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
            start_of_week = datetime(year,1,3,0,0,0) + timedelta(weeks=week)
            end_of_week = start_of_week + timedelta(weeks=1)

            cursor.execute("SELECT name, quantity from public.\"order\" WHERE ordered_time between '{}' and '{}'".format(start_of_week, end_of_week))
            name_quantity = cursor.fetchall()

            name_quantity_dictionary = {}
            for pair in name_quantity:
                item_name = pair[0]
                item_quantity = pair[1]
                if item_name in name_quantity_dictionary:
                    name_quantity_dictionary[item_name] += item_quantity
                else:
                    name_quantity_dictionary[item_name] = item_quantity

            name_quantity_descending = sorted(name_quantity_dictionary.items(), key=lambda x:x[1], reverse=True)
    return name_quantity_descending

#----End of Owner----#

### ADMIN PAGE (TO DO) ###
@app.route("/admin", methods=["GET", "POST"])
def admin():
    boundary = AdminPage()
    if request.method == "GET":
        return boundary.adminTemplate()
    elif request.method == "POST":
        ##create edit view search suspend
        if request.form["button_type"] == "create_Account":
            return redirect(url_for('CreateAccount'))
        elif request.form["button_type"] == "edit_Account":
            return redirect(url_for('EditAccount'))
        elif request.form["button_type"] == "view_Account":
            return redirect(url_for('ViewAccount'))
        elif request.form["button_type"] == "search_Account":
            return redirect(url_for('SearchAccount'))
        elif request.form["button_type"] == "suspend_Account":
            return redirect(url_for('SuspendAccount'))

@app.route("/admin/CreateAccount", methods=["GET", "POST"])
def CreateAccount():
    boundary = AdminPage()
    if request.method == "GET":
        return boundary.adminTemplateCreateAccount()
    elif request.method == "POST":
        boundary.controller.createAccountInfo(request.form) # B-C, C-E
        flash(request.form["username"] + " successfully created!")
        return redirect(url_for('admin')) # redirect to admin page

@app.route("/admin/UpdateAccount", methods=["GET", "POST"])
def EditAccount():
    boundary = AdminPage()
    if request.method == "GET":
        return boundary.adminTemplateUpdateAccount()
    elif request.method == "POST":
        if boundary.controller.getSearchInfo(request.form): #B-C, C-E #check account exist
            boundary.controller.editAccountInfo(request.form) # B-C, C-E
            flash(request.form["username"] + " successfully updated!")
            return redirect(url_for('admin')) # redirect to admin page
        else:
            flash(request.form["username"] + " update failed or does not exist!")
            return redirect(url_for('admin')) # redirect to admin page

#search return all based on username
#while view retun based on username and role
#view display password, search does not
@app.route("/admin/ViewAccount", methods=["GET", "POST"])
def ViewAccount():
    boundary = AdminPage()
    if request.method == "GET":
        return boundary.adminTemplateViewSearchAccount()
    elif request.method == "POST":
        if boundary.controller.getSearchInfo(request.form): # B-C, C-E #return true if account exist
            with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
                with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                    cursor.execute("SELECT username FROM users WHERE username=%s AND profile=%s", (request.form["username"], request.form["type"]))
                    username = cursor.fetchall()

            with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
                with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                    cursor.execute("SELECT password FROM users WHERE username=%s AND profile=%s", (request.form["username"], request.form["type"]))
                    password = cursor.fetchall()

            with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
                with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                    cursor.execute("SELECT profile FROM users WHERE username=%s AND profile=%s", (request.form["username"], request.form["type"]))
                    account_type = cursor.fetchall()
            return boundary.adminTemplateViewAccount(username, password, account_type)
        else:
            flash(request.form["username"] + " account does not exist!")
            return redirect(url_for('admin')) # redirect to admin page

#search return all based on username
#while view retun based on username and role
#view display password, search does not
@app.route("/admin/SearchAccount", methods=["GET", "POST"])
def SearchAccount():
    boundary = AdminPage()
    if request.method == "GET":
        return boundary.adminTemplateSearchAccount()
    elif request.method == "POST":
        if boundary.controller.searchAccountInfo(request.form): # B-C, C-E #return true if account exist
            with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
                with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                    cursor.execute("SELECT username FROM users WHERE username='{}'".format(request.form["username"]))
                    username = cursor.fetchall()

            with psycopg2.connect(dbname=db_name, user=db_user, password=db_pw, host=db_host) as db:
                with db.cursor(cursor_factory=psycopg2.extras.DictCursor) as cursor:
                    cursor.execute("SELECT profile FROM users WHERE username='{}'".format(request.form["username"]))
                    account_type = cursor.fetchall()
            return boundary.adminTemplateSearchResult(username, account_type)
        else:
            flash(request.form["username"] + " account does not exist!")
            return redirect(url_for('admin')) # redirect to admin page

@app.route("/admin/SuspendAccount", methods=["GET", "POST"])
def SuspendAccount():
    boundary = AdminPage()
    if request.method == "GET":
        return boundary.adminTemplateSuspendAccount()
    elif request.method == "POST":
        if boundary.controller.getSearchInfo(request.form): #B-C, C-E #check account exist
            boundary.controller.suspendAccountInfo(request.form) # B-C, C-E
            flash(request.form["username"] + " successfully suspended!")
            return redirect(url_for('admin')) # redirect to admin page
        else:
            flash(request.form["username"] + " suspend fail or does not exist!")
            return redirect(url_for('admin')) # redirect to admin page

#----End of Admin----#





@app.errorhandler(500)
def page_not_found(e):
    flash("Unauthorized!")
    return redirect(url_for("index"))


### INITIALIZATION ###
if __name__ == "__main__":
    app.run(debug=False)
