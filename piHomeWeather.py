#!/usr/bin/python

import sys
import Adafruit_DHT
import sqlite3
import time

# configuration area
# databasename
dbname='/home/pi/piHomeWeather/weatherdb'

# store the temperature in the database
def log_data_in_db(temperature, humidity):
    conn=sqlite3.connect(dbname)
    curs=conn.cursor()
    curs.execute("INSERT INTO weatherdata values(datetime('now'), (?), (?))", (temperature, humidity))
    conn.commit()
    conn.close()

# also log the data in google spreadsheet
def log_data_in_spreadsheet(temperature, humidity):
    print "Coming soon...."

humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, 23)
if humidity is not None and temperature is not None:
        print 'Temp={0:0.1f}*C  Humidity={1:0.1f}%  Date {2}'.format(temperature, humidity, time.strftime("%H:%M:%S"))
	log_data_in_db(temperature, humidity)
else:
        print 'Failed to get reading. Try again!' 
