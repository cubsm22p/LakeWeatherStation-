#!/usr/bin/env python
import os
import time
import datetime
import glob
import MySQLdb
from time import strftime
 
os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')
temp_sensor = '/sys/bus/w1/devices/28-0317714266ff/w1_slave'
 

db = MySQLdb.connect(host="localhost", user="root",passwd="Trine11271991", db="temp_database")
cur = db.cursor()

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines
 
def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        temp_f = temp_c * 9.0 / 5.0 + 32.0
        return round(temp_f,1)
while True:
	temp = read_temp()
        print temp	
        dateTimeWrite = (time.strftime("%Y-%m-%d ") + time.strftime("%H:%M:%S"))
        print dateTimeWrite    
	sql = ("""INSERT INTO tempLog (datetime,temperature) VALUES (%s,%s)""",(dateTimeWrite,temp))
	time.sleep(1)
        try:
       		 print "Writing to database..."
       		 # Execute the SQL command
       		 cur.execute(*sql)
       		 # Commit your changes in the database
       		 db.commit()
       		 print "Write Complete"
 
        except:
       		 # Rollback in case there is any error
       		 db.rollback()
       		 print "Failed writing to database"
 
        cur.close()
        db.close()
        break
