import sys
import PyQt4
from PyQt4.QtGui import *
import requests
import json
import pyjsonrpc

#Qtable Widget - display Locations in locations table from server







def setlocationsdata():
    lista = ['aa', 'ab', 'ac']
    listb = ['ba', 'bb', 'bc']
    listc = ['ca', 'cb', 'cc']
    mystruct = {'A':lista, 'B':listb, 'C':listc}
    
    print "####Printing mystruct####"
    print mystruct
    
    n = 0
    for key in mystruct:
        m = 0
        print "####Printing Key####"
        print key
        for item in mystruct[key]:
            print "####Printing Item####"
            print item
            # newitem = QTableWidgetItem(item)
            # self.setItem(m, n, newitem)
            m += 1
        n += 1

setlocationsdata()

# class LocationsTable(QTableWidget):
    
#     def getLocations(self):
#         http_client = pyjsonrpc.HttpClient(
#             url = "http://localhost:8080/",
#         )
#         svr_response = http_client.call("returnloco")
#         print svr_response
#         return svr_response
    
    
    
#     def __init__(self, thestruct, *args):
#         # self.mystruct = {'locations':self.getLocations()}
#         QTableWidget.__init__(self, *args)
#         self.data = thestruct
#         self.setlocationsdata()

#     def setlocationsdata(self):
#         print "printing self.data"
#         print self.data
#         n = 0
#         for key in self.data:
#             m = 0
#             print key
#             for item in self.data[key]:
#                 print item
#                 # newitem = QTableWidgetItem(item)
#                 # self.setItem(m, n, newitem)
#                 m += 1
#             n += 1

# def main(args):
#     app = QApplication(args)
#     table = LocationsTable(mystruct, 3, 3)
#     table.show()
#     sys.exit(app.exec_())

# if __name__=="__main__":
#     main(sys.argv)  