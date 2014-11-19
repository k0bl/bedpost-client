import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import requests
import json
import pyjsonrpc

class TransfersLayout(QtGui.QWidget):
    
    def __init__(self):
        super(TransfersLayout, self).__init__()
        
        self.initUI('bedpost.png')
    
    def initUI(self, image):
    
        hbox = QtGui.QHBoxLayout(self)
        #set the image to lbl
        pixmap = QtGui.QPixmap(image)
        lbl = QtGui.QLabel(self)
        lbl.setPixmap(pixmap)

        self.tranTable = TransfersTable(25, 6)
        bottom = self.tranTable

        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(lbl)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QSplitter')
        self.show()

class TransfersTable(QTableWidget):
    def __init__(self, *args):
        
        QTableWidget.__init__(self, *args)
        table = QTableWidget()
        
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setHorizontalHeaderLabels(('ID','Collection PC','Start Time','Study Name','Complete Time','Status'))
        self.resizeColumnsToContents()
        self.setTransfers()

    def setTransfers(self):
        http_client = pyjsonrpc.HttpClient(
            url = "http://localhost:8080/",
            )
        svr_response = http_client.call("returntransfers")
        
        print svr_response

        
        newstruct = {'transfers_list': svr_response}
        n = 0
        for entry in newstruct:
            x = 0
            for obj in newstruct[entry]:
                sublist = svr_response[x]
                v = 0
                for g in sublist:
                    item = sublist[v]
                    newitem = QTableWidgetItem(item)
                    self.setItem(x, v, newitem)
                    v += 1
                x += 1
            n += 1
