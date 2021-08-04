#!/usr/bin/env python3
import re
import os
import os.path

userlist=[]

def main():
    username = input('Enter your username: ')
    passwd = input('Enter your password: ')
    reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,12}$"
                  
    # compiling regex
    pat = re.compile(reg)
        
    # searching regex                 
    mat = re.search(pat, passwd)
    
    file1 = open('/root/iot_vol/SmartFarm/scripts/cacert/password.txt', 'r')
    Lines = file1.readlines()

    for line in Lines:
        line2=line.rsplit(':',1)[0]
        userlist.append(line2)
    #print(userlist)

    for u in userlist:
        if u == username:
            print("Username is taken")
            exit()
            

    # validating conditions
    if mat:
        if os.path.isfile('/root/iot_vol/SmartFarm/scripts/cacert/password.txt'):
            print("Password is valid and added into password.txt file.")
            os.system("mosquitto_passwd -b /root/iot_vol/SmartFarm/scripts/cacert/password.txt " + username + " " + passwd)
        else:
            print("Password is valid and added into password.txt file.")
            os.system("echo " + username + ":" + passwd + " > /root/iot_vol/SmartFarm/scripts/cacert/password.txt")
            os.system("mosquitto_passwd -U /root/iot_vol/SmartFarm/scripts/cacert/password.txt")
    else:
        print("Password invalid")

# Driver Code   
if __name__ == '__main__':
    main()

