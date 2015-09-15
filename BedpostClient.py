import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
from PyQt4.QtCore import *
import requests
import json
import pyjsonrpc
import time
import  subprocess as sp
import threading
import ExtendedQLabel

#this is a test
class Main(QtGui.QMainWindow):
    def __init__(self):
        print "main init"
        super(Main, self).__init__()
        
        self.initUI()
        
    def initUI(self):   
        print "initUI"
        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
       
        
        
        refreshAction = QtGui.QAction(QtGui.QIcon('refresh.png'), '&Refresh', self)
        refreshAction.setShortcut('Ctrl+R')
        refreshAction.triggered.connect(self.refreshClick)

        menubar = self.menuBar()

        self.toolbar = self.addToolBar('Refresh')
        self.toolbar.addAction(refreshAction)

        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        optionsMenu = menubar.addMenu('&Options')
        optionsMenu.addAction(refreshAction)
    
        self.logo = imageLayout()
        self.centapp = TransfersLayout()
        print "centapp set to TransfersLayout"
        self.setMenuWidget(menubar)
        self.setCentralWidget(self.centapp)
        print "central widget set to centapp"
        self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle('Bedpost Client beta 0.0.2')
        self.refreshClick()
        self.show()
        

    
    def configClick(self):
        self.baseconflayout = BaseConfigLayout()
        self.setCentralWidget(self.baseconflayout)
        self.statusBar().showMessage('Entering configuration...')

    def refreshClick(self):

        try:
                    
            self.tranRefresh = TransfersLayout()
            self.statusBar().showMessage('Refreshing...')
            self.setCentralWidget(self.tranRefresh)
            self.statusBar().showMessage('Up To Date')

        finally:
            QTimer.singleShot(5000, self.refreshClick)


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

        self.tranTable = TransfersTable(25, 7)
        self.tranTable.setHorizontalHeaderLabels(('','Bed Number','Clinicore ID','Location',' Study Folder ', ' Status ', 'Download'))
        self.tranTable.resizeColumnsToContents()
        bottom = self.tranTable
        
        splitter = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter.addWidget(lbl)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 1000, 600)
        self.setWindowTitle('QtGui.QSplitter')
        self.show()

class TransfersTable(QTableWidget):
    def __init__(self, *args):
        
        QTableWidget.__init__(self, *args)
        table = QTableWidget()
        
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(True)
        
        
        self.setTransfers()

    def setTransfers(self):
        http_client = pyjsonrpc.HttpClient(
            url = "http://10.0.3.112:5050/",
            #url = "http://192.168.1.7:5050/",
            
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
                    titem = sublist[v]
                    newitem = QTableWidgetItem(titem)
                    self.setItem(x, v, newitem)
                    v += 1
                btn = ExtendedQLabel.ExtendedQLabel(self)
                btn.setText('Download Collection')
                print "Row x = ", x
                self.setCellWidget(x, 6, btn)
                x += 1
                self.connect(btn, SIGNAL('clicked()'), self.downloadTransfer)
            n += 1




    def btnClicked(self):
        self.downloadTransfer()
    
    def downloadTransfer(self):
        row = self.currentRow()
        print "Row Number: ", row
        prow = row        
        row = None
        tiditem = self.item(prow, 2)
        beditem = self.item(prow, 1)
        locitem = self.item(prow, 3)
        folitem = self.item(prow, 4)

        
        tidtext = tiditem.text()
        bedtext = beditem.text()
        loctext = locitem.text()
        foltext = folitem.text()

        tidstr = str(tidtext)
        bedstr = str(bedtext)
        locstr = str(loctext)
        folstr = str(foltext)

        print "bed number: ", bedtext
        print "bed location: ", loctext
        print "bed folder: ", foltext

        download_thread = threading.Thread(target=self.download, args=(tidstr,locstr,bedstr,folstr))
        download_thread.start()
        print "Download Thread Created."
                    

    def download(self, cid, loc, bed, fol):
        self.startDownload(cid, loc, bed, fol)

    def startDownload(self, cid, loc, bed, fol):

        startStatus = "Downloading"
        print "starting download"
        self.updateTransferStatus(cid, startStatus)
        cmd = "start winscp.exe /command \"open \"\"bedpost\"\"\" \"get \"\"/srv/bedpost/"+loc+"/"+bed+"/"+fol+"\"\"\""
        proc = sp.Popen(cmd, shell=True,
               stdout=sp.PIPE, 
               stderr=sp.PIPE)
        streamdata = proc.communicate()[0]

        print "Done Downloading Transfer from Server"
        doneStatus = "Download Complete"
        self.updateTransferStatus(cid, doneStatus)

    def updateTransferStatus(self, cid, status):
        url = "http://10.0.3.112:5050/"
        #url = "http://192.168.1.7:5050/"
        headers = {'content-type': 'application/json'}

        # Example echo method
        payload = {
            "method": "updateDownloadStatus",
            "params": {"status": status, "cid": cid},
            "jsonrpc": "2.0",
            "id": 0
        }
        response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()

        print response

class imageLayout(QtGui.QWidget):
    def __init__(self):
        super(imageLayout, self).__init__()
        self.setImage('bedpost.png')
    
    def setImage(self, image):
        hbox = QtGui.QHBoxLayout(self)
        pixmap = QtGui.QPixmap(image)

        lbl = QtGui.QLabel(self)
        lbl.setPixmap(pixmap)

        hbox.addWidget(lbl)

        self.setLayout(hbox)


def main():
    
    app = QtGui.QApplication(sys.argv)
    app.setStyleSheet(" QTableWidget::item:focus { background-color:transparent; color:blue;  padding: 10px; border: 0px }" )
    ex = Main()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()