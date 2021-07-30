#!/usr/bin/env python3

import os
from flask import Flask, request, redirect, render_template
import datetime
import random
import MySQLdb
import os
import re
# from os import urandom
# from Crypto.Cipher import AES

app = Flask(__name__)
db_user = "sfuser"
db_password = "sfp@ssw0rD$su$"
db_address = "localhost"
db_database = "SmartFarm"

@app.route('/init')
def init():
    """
        Delete all information
    """
    try:
        db = MySQLdb.connect(db_address, db_user, db_password, db_database)
    except:
        return "MYSQL not running"
    connection = db.cursor()
    try:
        connection.execute("delete from sensors")
        db.commit()
    except:
        db.rollback()
    db.close()
    return redirect("/")
    
@app.route("/update/", methods=["GET","PUT"] )
@app.route("/update/<Id>", methods=["GET","PUT"] )
def update(Id=None):
    device_nameStr = request.args.get('Device')
    device_timeStr = request.args.get('DeviceTime') 
    device_statusStr = request.args.get('DeviceStatus')
    device_informationStr = request.args.get('DeviceInformation')
    if device_nameStr == None and Id == None and device_timeStr == None and device_statusStr == None and device_informationStr == None:
        #return "usage: update/ID?'DeviceTime=VALUE&DeviceStatus=VALUE&DeviceInformation=VALUE'"
        return "INCORRECT SYNTAX\n"
    
    #Validate all fields before updating to the database
    check = 0
    #Check the value of Id is 1-4
    regex_id = "^[1-4]"
    match_id = re.findall(regex_id, Id)
    if not match_id:
        check = check + 1
        print("Failed to update. Incorrect Id Format: ",Id, "\n")

    #Check that value of device status is either ON or OFF
    if (device_statusStr == "ON") and (device_statusStr != "OFF"):
        pass
    elif (device_statusStr != "ON") and (device_statusStr == "OFF"):
        pass
    else:
        check = check + 1
        print("Failed to update. Incorrect Status Format: "+device_statusStr, "\n")

    #Validate device time string
    regex_time = "^([0-9][0-9][0-9][0-9])[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])[ ](2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$"
    match_time = re.findall(regex_time, device_timeStr)
    if not match_time:
        check = check + 1
        print("Failed to update. Incorrect Time Format: "+device_timeStr, "\n")    

    #Validate device information string
    regex_info = r"^[a-zA-Z_]+[ ]+[A-Za-z]+[: ]+[0-9]{1,3}$"
    match_info = re.findall(regex_info, device_informationStr)
    if not match_info:
        check = check + 1
        print("Failed to update. Incorrect Device Information Format: "+device_informationStr, "\n")
    
    if check == 0:
        try:
            db = MySQLdb.connect(db_address, db_user, db_password, db_database)
        except:
            return "MYSQL not running"
        
        cursor = db.cursor()
        #Update All
        try:
            #query="update sensorsUp set DeviceTime = '" + db.escape_string(device_timeStr).decode("UTF-8") + "', DeviceStatus = '" + db.escape_string(device_statusStr).decode("UTF-8") + "', DeviceInformation = '" + db.escape_string(device_informationStr).decode("UTF-8") + "' where Id = '" + db.escape_string(Id).decode("UTF-8") + "';"
            #Prepared Statement
            query="update sensorsUp set DeviceTime = %s, DeviceStatus = %s, DeviceInformation = %s where Id = %s;"
            q1 = (device_timeStr, device_statusStr, device_informationStr, Id)
            cursor.execute(query, q1)
            print("UPDATE", q1)
            # print(query)
            # cursor.execute(query)
            db.commit()
        except:
            db.rollback()
            return "FAIL\n"
        db.close()
        return "UPDATED\n"
    return "NOT UPDATED\n"

@app.route("/add/", methods=["GET","PUT"] )
@app.route("/add/<device_name>", methods=["GET","PUT"] )
def add(device_name=None):
    device_timeStr = request.args.get('DeviceTime') 
    device_statusStr = request.args.get('DeviceStatus')
    device_informationStr = request.args.get('DeviceInformation')
    if device_timeStr == None or device_name == None or device_statusStr == None or device_informationStr == None:
        #return "usage: add/device_name?'DeviceTime=VALUE&DeviceStatus=VALUE&DeviceInformation=VALUE'"
        return "INCORRECT SYNTAX\n"
    
    #Validate all fields before adding to the database
    check = 0
    #Check that format of device name is only letters
    check_name = device_name.isalpha()
    if check_name != True:
        check = check + 1
        print("Failed to add. Incorrect Name Format: "+device_name, "\n")

    #Check that value of device status is either ON or OFF
    if (device_statusStr == "ON") and (device_statusStr != "OFF"):
        pass
    elif (device_statusStr != "ON") and (device_statusStr == "OFF"):
        pass
    else:
        check = check + 1
        print("Failed to add. Incorrect Status Format: "+device_statusStr, "\n")

    #Validate device time string
    regex_time = "^([0-9][0-9][0-9][0-9])[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])[ ](2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$"
    match_time = re.findall(regex_time, device_timeStr)
    if not match_time:
        check = check + 1
        print("Failed to add. Incorrect Time Format: "+device_timeStr, "\n")    

    #Validate device information string
    regex_info = r"^[a-zA-Z_]+[ ]+[A-Za-z]+[: ]+[0-9]{1,3}$"
    match_info = re.findall(regex_info, device_informationStr)
    if not match_info:
        check = check + 1
        print("Failed to add. Incorrect Device Information Format: "+device_informationStr, "\n")

    # #secret_key = urandom(16).encode("UTF8")
    # key = "abcdefghijklmnop"
    # secret_key = str.encode(key)
    # #iv = urandom(16).encode("UTF8")
    # iv = str.encode(key)
    # aes_en = AES.new(secret_key, AES.MODE_CBC, iv)
    # encrypt_name = aes_en.encrypt(str.encode(device_name))
    # encrypt_status = aes_en.encrypt(str.encode(device_statusStr))
    # encrypt_time = aes_en.encrypt(str.encode(device_timeStr))
    # encrypt_info = aes_en.encrypt(str.encode(device_informationStr))

    if check == 0:
        try:
            db = MySQLdb.connect(db_address, db_user, db_password, db_database)
        except:
            return "MYSQL not running"
        cursor = db.cursor()
        try:
            #query="insert into sensors(Device,DeviceTime,DeviceStatus,DeviceInformation) values ('" + db.escape_string(device_name).decode("UTF-8") + "','" + db.escape_string(device_timeStr).decode("UTF-8") + "','" + db.escape_string(device_statusStr).decode("UTF-8") + "','" + db.escape_string(device_informationStr).decode("UTF-8") + "');"
            #Prepared Statement
            query="insert into sensors(Device,DeviceTime,DeviceStatus,DeviceInformation) values (%s,%s,%s,%s);"
            q1 = (device_name, device_timeStr, device_statusStr, device_informationStr)
            #q1 = (encrypt_name, encrypt_time, encrypt_status, encrypt_info)
            cursor.execute(query, q1)
            print("INSERT", q1)
            db.commit()
        except Exception as e:
            db.rollback()
            print(str(e))
            return "FAIL\n"
        db.close()
        return "ADDED\n"
    return "NOT ADDED\n"
    
# @app.route("/")
# def root():
#     return render_template("base.html")
@app.route("/db", methods=["GET", "PUT"])
def default():
    """
        Show list of comments with form to submit comments
    """
    try:
        db = MySQLdb.connect(db_address, db_user, db_password, db_database)
    except:
        return "MYSQL not running"
    cursor = db.cursor()
    cursor.execute('''select * from sensors''')
    comments = cursor.fetchall()
    db.close()
    return render_template("db.html", comments=comments)

@app.route("/")
def dashboard():
    try:
        db = MySQLdb.connect(db_address, db_user, db_password, db_database)
    except:
        return "MYSQL not running"
    cursor = db.cursor()
    cursor.execute('''select Device, DeviceStatus from sensorsUp''')
    comments = cursor.fetchall()
    db.close()
    return render_template("dashboard.html", comments=comments)

if __name__ == "__main__":
    host = os.getenv("IP", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    app.run(host=host, port=port, debug=False, use_reloader=True, use_evalex=False)
