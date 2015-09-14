from datetime import datetime
import time
import logging
#!/usr/bin/env python
# coding: utf-8

"""
This is a mock script that does what bedpost does but without actually copying data.
"""
import json
import requests
import pyjsonrpc
import sqlite3
#Globals
rightnow = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
database = 'bedposttest.db'

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='bedpostmock.log', level=logging.INFO)
print "This is Bedpost 0.1.2"
print "running now"
def startingTransfer(cpc, name):
	conn = sqlite3.connect(database)
	c = conn.cursor()
	#persist new values to sqlite3 database
	dbcpc = str(cpc)
	dbname = str(name)
	dbstarted_at = str('null')
	dbstatus = str('In Queue')
	dbtimedone = str('null')
	print "Starting Transfer"
	print "Collection PC", dbcpc
	print "Study Name", dbname
	print "Current Status", dbstatus
	c.execute ("INSERT INTO transfers VALUES (null, ?, ?, ?, ?, ?);", (dbcpc, dbtimedone, dbname, dbstarted_at, dbstatus))
	print "Insertion is done...giggity"
	conn.commit()
	conn.close()
	

def transferring(cpc, name, started_at):
	conn = sqlite3.connect(database)
	c = conn.cursor()
	#persist new values to sqlite3 database
	dbcpc = str(cpc)
	dbstarted_at = started_at
	dbname = name
	dbstatus = str('Transferring')
	c.execute("UPDATE transfers SET status=?, started_at=?  WHERE name=?", (dbstatus, dbstarted_at, dbname))
	print "update is done...giggity"
	conn.commit()
	conn.close()


def transferComplete(cpc, name, timedone):
	conn = sqlite3.connect(database)
	c = conn.cursor()
	#persist new values to sqlite3 database
	dbcpc = str(cpc)
	dbtimedone = str(timedone)
	dbname = name
	dbstatus = str('Transfer Complete')
	c.execute("UPDATE transfers SET status=?, time_done=?  WHERE name=?", (dbstatus, dbtimedone, dbname))
	print "update is done...giggity"
	conn.commit()
	conn.close()



count = 1
while count <=10:
	#Starting Transfer, In Queu
	tname1 = "Jennifer Smith"
	tname2 = "Bob Jenkins"
	tname3 = "Fred Ximeno"
	bed1 ="bed1.unitedsleep.local"
	bed2 = "bed2.unitedsleep.local"
	bed3 = "bed3.unitedsleep.local"
	startingTransfer(bed1, tname1)
	startingTransfer(bed2, tname2)
	startingTransfer(bed3, tname3)				


	#Transferring
	tstart1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	transferring(bed1, tname1, tstart1)
	time.sleep(15)  # Delay for 5 seconds (5 seconds)
	#Transfer Complete
	tcomplete1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	transferComplete(bed1, tname1, tcomplete1)

	#Transferring
	
	tStart2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	transferring(bed2, tname2, tStart2)
	time.sleep(20)  # Delay for 5 seconds (5 seconds)
	#Transfer Complete
	tcomplete2 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	transferComplete(bed2, tname2, tcomplete2)
	
	#Transferring
	tStart3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	transferring(bed3, tname3, tStart3)
	time.sleep(25)  # Delay for 5 seconds (5 seconds)
	#Transfer Complete
	tcomplete3 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
	transferComplete(bed3, tname3, tcomplete3)

	count = count+count
    