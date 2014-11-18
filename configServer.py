#!/usr/bin/env python
# coding: utf-8

"""
This is a dynamic http server for saving configutations. At the 
moment, I will keep the configuration (admin) backend portion 
separate from the main view application.
"""
import json
import requests
import pyjsonrpc
import sqlite3
#Globals
database = 'bedposttest.db'
# conn = sqlite3.connect('pyjsonrpctest2.db')
# c = conn.cursor()


# #try to insert values into 
# c.execute("INSERT INTO locations VALUES ('longbeach', '90806', 'lgb')")

def resetDatabase():
        conn = sqlite3.connect(database)
        c = conn.cursor()
        #Drop the tables if they already exist
        c.execute("DROP TABLE IF EXISTS collection_pcs")
        c.execute("DROP TABLE IF EXISTS remote_servers")
        c.execute("DROP TABLE IF EXISTS locations")
        c.execute("DROP TABLE IF EXISTS transfers")
        #Create new tables for each entity
        c.execute('''CREATE TABLE collection_pcs
        
        (cpc_id  INTEGER PRIMARY KEY ASC, cpc_name text, cpc_hostname text, cpc_domain text, cpc_username text, cpc_password text, cpc_datadir text, cpc_fqdn text,  cpc_location text)''')
        
        c.execute('''CREATE TABLE remote_servers
        (rm_id  INTEGER PRIMARY KEY ASC, rm_name text, rm_ip text, rm_port text, rm_datapath text, rm_user text, rm_pass text)''')
        
        c.execute('''CREATE TABLE locations
        (location_id  INTEGER PRIMARY KEY ASC, location_name text, location_zip text, accronym text)''')                        
        c.execute('''CREATE TABLE transfers
            (transfer_id INTEGER PRIMARY KEY ASC, cpc text, time_done text, name text, started_at text, status text)''')


class RequestHandler(pyjsonrpc.HttpRequestHandler):
    
    #rpc method for adding a new collection pc to the database.

    @pyjsonrpc.rpcmethod
    def savecpc(self, cpcname, cpchostname, cpcdomain, cpcusername, cpcpassword, cpcdatadir, cpcfqdn, cpclocation):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        print cpcname
        print cpchostname
        print cpcdomain
        print cpcusername
        print cpcpassword
        print cpcdatadir
        print cpcfqdn
        print cpclocation
        dbcpcname = str(cpcname)
        dbcpchostname = str(cpchostname)
        dbcpcdomain = str(cpcdomain)
        dbcpcusername = str(cpcusername)
        dbcpcpassword = str(cpcpassword)
        dbcpcdatadir = str (cpcdatadir)
        dbcpcfqdn = str(cpcfqdn)
        dbcpclocation = str (cpclocation)

        c.execute ("INSERT INTO collection_pcs VALUES (null, ?, ?, ?, ?, ?, ?, ?, ?);", (dbcpcname, dbcpchostname, dbcpcdomain, dbcpcusername, dbcpcpassword, dbcpcdatadir, dbcpcfqdn, dbcpclocation))        
        
        print "CPC Insertion is done"
        conn.commit()

        last_id = c.lastrowid
        
        print "Last ID is set to last inserted row"
        print last_id

        print "Printing selection"
        print c.execute("SELECT * FROM cpcs WHERE cpc_id = ?", (last_id,))
        row = c.fetchone()
        
        # print "Selection is done"
        # print "Printing dbout"
        # print dbout
        conn.close()
        return row
    
    @pyjsonrpc.rpcmethod
    def saveremote(self, rmname, rmipaddress, rmport, rmdatapath, rmuser, rmpass):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        print rmname
        print rmipaddress
        print rmport
        print rmdatapath
        print rmuser
        print rmpass
    
        dbrmname = str(rmname)
        dbrmipaddress = str(rmipaddress)
        dbrmport = str(rmport)
        dbrmdatpath = str(rmdatapath)
        dbrmuser = str(rmuser)
        dbrmpass = str (rmpass)

        c.execute ("INSERT INTO remote_servers VALUES (null, ?, ?, ?, ?, ?, ?);", (dbrmname, dbrmip, dbrmport, dbrmdatapath, dbrmuser, dbrmpass))        
        
        print "CPC Insertion is done"
        conn.commit()

        last_id = c.lastrowid
        
        print "Last ID is set to last inserted row"
        print last_id

        print "Printing selection"
        print c.execute("SELECT * FROM remote_servers WHERE rm_id = ?", (last_id,))
        row = c.fetchone()
        
        # print "Selection is done"
        # print "Printing dbout"
        # print dbout
        conn.close()
        return row

    @pyjsonrpc.rpcmethod
    def saveloco(self, loconame, locozip, locoaccr):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        
        #persist new values to sqlite3 database
        dbloconame = str(loconame)
        dblocozip = str(locozip)
        dblocoaccr = str(locoaccr)
        print "loconame is:", dbloconame 
        print "locozip is:", dblocozip
        print "locoaccr is:", dblocoaccr
        
        c.execute("INSERT INTO locations VALUES (null, ?, ?, ?);", (dbloconame, dblocozip, dblocoaccr))
        print "Insertion is done...giggity"
        conn.commit()

        last_id = c.lastrowid
        
        print "Last ID is set to last inserted row"
        print last_id

        print "Printing selection"
        print c.execute("SELECT * FROM locations WHERE location_id = ?", (last_id,))
        row = c.fetchone()
        

        conn.close()
        return row

    #write a return method that just sends the locations objects back to the client
    @pyjsonrpc.rpcmethod
    def returnloco(self):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('SELECT * FROM locations')
        results = c.fetchall()
        print "printing locations"
        print '\nindividual records'
        for result in results:
            print result
        return results

    #write a return method that just sends the collection pcs back to the client
    @pyjsonrpc.rpcmethod

    
    #write a return methos that sends the remote servers back to the client
    @pyjsonrpc.rpcmethod
    def returnremote(self):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('SELECT * FROM remote_servers')
        results = c.fetchall()
        print "printing remote servers"
        print '\nindividual records'
        
        for result in results:
            print result
        return results

#write a return methos that sends the remote servers back to the client
    @pyjsonrpc.rpcmethod
    def returncpcs(self):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('SELECT * FROM collection_pcs')
        results = c.fetchall()
        
        print "printing collection pcs"
        print '\nindividual records'
        
        for result in results:
            print result
        return results
    
    @pyjsonrpc.rpcmethod
    def returntransfers(self):
        conn = sqlite3.connect(database)
        c = conn.cursor()
        c.execute('SELECT * FROM transfers')
        results = c.fetchall()
        
        print "printing transfers"
        print '\nindividual records'
        
        for result in results:
            print result
        return results
# print "resetting database"
# resetDatabase()
# print "done resetting database"

    
# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 8080),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:8080"

try:
    http_server.serve_forever()
except KeyboardInterrupt:
        http_server.shutdown()
print "Stopping HTTP Server"

