#!/usr/bin/env python3

import os
from flask import Flask, request, redirect, render_template
import datetime
import random
import MySQLdb
import os
import re
from cryptography.fernet import Fernet
import base64

app = Flask(__name__)
db_user = "sfuser"
db_password = "sfp@ssw0rD$su$"
db_address = "localhost"
db_database = "SmartFarm"

#Retrieve key for encryption/decryption from file
file = open('key.txt')
key = file.readline()
#Initialise Fernet with key
fernet = Fernet(key)

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
    # device_nameStr = request.args.get('Device')
    # device_timeStr = request.args.get('DeviceTime') 
    device_statusStr = request.args.get('DeviceStatus')
    # device_informationStr = request.args.get('DeviceInformation')
    #if device_nameStr == None and Id == None and device_timeStr == None and device_statusStr == None and device_informationStr == None:
    if Id == None and device_statusStr == None:
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

    # #Validate device time string
    # regex_time = "^([0-9][0-9][0-9][0-9])[-](0[1-9]|1[012])[-](0[1-9]|[12][0-9]|3[01])[ ](2[0-3]|[01]?[0-9]):([0-5]?[0-9]):([0-5]?[0-9])$"
    # match_time = re.findall(regex_time, device_timeStr)
    # if not match_time:
    #     check = check + 1
    #     print("Failed to update. Incorrect Time Format: "+device_timeStr, "\n")    

    # #Validate device information string
    # regex_info = r"^[a-zA-Z_]+[ ]+[A-Za-z]+[: ]+[0-9]{1,3}$"
    # match_info = re.findall(regex_info, device_informationStr)
    # if not match_info:
    #     check = check + 1
    #     print("Failed to update. Incorrect Device Information Format: "+device_informationStr, "\n")
    
    #Encrypt encoded data before updating db
    # encrypt_time = fernet.encrypt(device_timeStr.encode())
    encrypt_status = fernet.encrypt(device_statusStr.encode())
    # encrypt_info = fernet.encrypt(device_informationStr.encode())

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
            #query="update sensorsUp set DeviceTime = %s, DeviceStatus = %s, DeviceInformation = %s where Id = %s;"
            query="update sensorsUp set DeviceStatus = %s, where Id = %s;"
            q1 = (encrypt_status, Id)
            cursor.execute(query, q1)
            # print(query)
            # cursor.execute(query)
            db.commit()
        except:
            db.rollback()
            return "FAIL\n"
        db.close()
        return "UPDATED SUCCESSFULLY\n"
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

    #Encrypt encoded data before adding to db
    encrypt_name = fernet.encrypt(device_name.encode())
    encrypt_time = fernet.encrypt(device_timeStr.encode())
    encrypt_status = fernet.encrypt(device_statusStr.encode())
    encrypt_info = fernet.encrypt(device_informationStr.encode())

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
            #q1 = (device_name, device_timeStr, device_statusStr, device_informationStr)
            q1 = (encrypt_name, encrypt_time, encrypt_status, encrypt_info)
            cursor.execute(query, q1)
            db.commit()
        except Exception as e:
            db.rollback()
            print(str(e))
            return "FAIL\n"
        db.close()
        return "ADDED SUCCESSFULLY\n"
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
    comments1 = cursor.fetchall()
    comments2 = []

    #Loop through each database entry
    for row in comments1:
        id, name, time, status, info = row[0], row[1], row[2], row[3], row[4]
        
        #Convert string to bytes
        name2 = bytes(name, 'utf-8')
        time2 = bytes(time, 'utf-8')
        status2 = bytes(status, 'utf-8')
        info2 = bytes(info, 'utf-8')

        #Decrypt and decode data
        decrypt_name = fernet.decrypt(name2).decode()
        decrypt_time = fernet.decrypt(time2).decode()
        decrypt_status = fernet.decrypt(status2).decode()
        decrypt_info = fernet.decrypt(info2).decode()

        #Store decrypted data in new array
        comments2.append((id, decrypt_name, decrypt_time, decrypt_status, decrypt_info))

    db.close()
    return render_template("db.html", comments2=comments2)

@app.route("/")
def dashboard():
    try:
        db = MySQLdb.connect(db_address, db_user, db_password, db_database)
    except:
        return "MYSQL not running"
    cursor = db.cursor()
    cursor.execute('''select Device, DeviceStatus from sensorsUp''')
    comments1 = cursor.fetchall()
    comments2 = []
    for row in comments1:
        name, status = row[0], row[1]

        if status == "OFF":
            comments2.append((name, status))
        else:
            status2 = bytes(status, 'utf-8')
            decrypt_status = fernet.decrypt(status2).decode()
            comments2.append((name, decrypt_status))

    db.close()
    return render_template("dashboard.html", comments2=comments2)

if __name__ == "__main__":
    host = os.getenv("IP", "0.0.0.0")
    port = int(os.getenv("PORT", 8080))
    app.run(host=host, port=port, debug=False, use_reloader=True, use_evalex=False)
