import sys
import PyQt4
from PyQt4.QtGui import *
import requests
import json
import pyjsonrpc

#Qtable Widget - display Locations in locations table from server




# lista = getLocations()
# mystruct = {'locations_list': lista}

# print "Printing mystruct"
# print mystruct

class LocationsTable(QTableWidget):
    

    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setLocations()
    
    def setLocations(self):
        http_client = pyjsonrpc.HttpClient(
            url = "http://localhost:8080/",
        )
        svr_response = http_client.call("returnloco")
        print "######PRINTING SERVER JSON DUMPS RESPONSE########"
        print json.dumps(svr_response, ensure_ascii=True, separators=None)
        print "######DONE PRINTING SERVER RESPONSE########"
        newstruct = {'locations_list': svr_response}
        print "######PRINTING STRUCT########"
        print newstruct
        print "######DONE PRINTING STRUCT########"
        print "######PRINTING LIST AS STRING######"
        n = 0
        for entry in newstruct:
            x = 0
            print "Printing Entry"
            print entry
            print "Done printing entry"
            for obj in newstruct[entry]:
                sublist = svr_response[x]
                print "#####PRINTING SUBLIST#####"
                print sublist
                v = 0
                for g in sublist:
                    item = sublist[v]
                    print "####Printing Item######"
                    print item
                    newitem = QTableWidgetItem(item)
                    self.setItem(x, v, newitem)
                    v +=1
                print sublist
                x += 1
            n += 1

def main(args):
    app = QApplication(args)
    table = LocationsTable(5, 4)
    table.show()
    sys.exit(app.exec_())

if __name__=="__main__":
    main(sys.argv)  