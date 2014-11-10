#!/usr/bin/env python
# coding: utf-8

import pyjsonrpc
import sqlite3
# conn = sqlite3.connect('pyjsonrpctest2.db')
# c = conn.cursor()

# #try to insert values into 
# c.execute("INSERT INTO locations VALUES ('longbeach', '90806', 'lgb')")


class RequestHandler(pyjsonrpc.HttpRequestHandler):

  @pyjsonrpc.rpcmethod
  def saveloco(self, loconame, locozip, locoaccr):
      	conn = sqlite3.connect('bedposttest.db')
        c = conn.cursor()
        
        print loconame
      	print locozip
      	print locoaccr
      	#persist new values to sqlite3 database
        dbloconame = str(loconame)
        dblocozip = str(locozip)
        dblocoaccr = str(locoaccr)
        c.execute("DROP TABLE IF EXISTS locations")
        c.execute('''CREATE TABLE locations
        (location_name text, location_zip text, accronym text)''')
      	c.execute("INSERT INTO locations VALUES (?, ?, ?);", (dbloconame, dblocozip, dblocoaccr))
        conn.commit()
        conn.close()

      	return loconame, locozip, locoaccr


# Threading HTTP-Server
http_server = pyjsonrpc.ThreadingHttpServer(
    server_address = ('localhost', 8080),
    RequestHandlerClass = RequestHandler
)
print "Starting HTTP server ..."
print "URL: http://localhost:8080"
http_server.serve_forever()