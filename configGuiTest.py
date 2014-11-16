import sys
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import *
import requests
import json
import pyjsonrpc

#this is a test
class Main(QtGui.QMainWindow):
    def __init__(self):
        
        super(Main, self).__init__()
        self.initUI()

    def initUI(self):   

        exitAction = QtGui.QAction(QtGui.QIcon('exit.png'), '&Exit', self)        
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Exit application')
        exitAction.triggered.connect(QtGui.qApp.quit)
       
        configAction = QtGui.QAction('&Configure', self)
        configAction.setShortcut('Ctrl+O')
        configAction.setStatusTip('Client Options')
        configAction.triggered.connect(self.configClick)
        
        self.statusBar()

        menubar = self.menuBar()
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(exitAction)
        optionsMenu = menubar.addMenu('&Options')
        optionsMenu.addAction(configAction)

        self.logo = imageLayout()
        self.centapp = TransfersLayout()
        self.setMenuWidget(menubar)
        self.setCentralWidget(self.centapp)
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('Bedpost Client beta 0.0.2')
        self.show()
    
    def configClick(self):
        self.baseconflayout = BaseConfigLayout()
        self.setCentralWidget(self.baseconflayout)

class CentralAppLayout(QtGui.QWidget):
    def __init__(self):
        super (CentralAppLayout, self).__init__()
        self.initUI('bedpost.png')
        

    def initUI(self, image):

        vbox = TransfersLayout()
        
        self.setLayout(vbox)
        
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QSplitter')
        # self.show()

class TransfersLayout(QtGui.QWidget):
    
    def __init__(self):
        super(TransfersLayout, self).__init__()
        
        self.initUI()
    
    def initUI(self):
    
        hbox = QtGui.QHBoxLayout(self)
    
        self.tranTable = TransfersTable(25, 4)
        bottom = self.tranTable

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QSplitter')
        # self.show()

class TransfersTable(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setTransfers()

    def setTransfers(self):
        http_client = pyjsonrpc.HttpClient(
            url = "http://localhost:8080/",
            )
        svr_response = http_client.call("returntransfers")
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


class BaseConfigLayout(QtGui.QWidget):
    def __init__(self):
        super (BaseConfigLayout, self).__init__()
        self.initUI()


    def initUI(self):
        
        self.tabs = QtGui.QTabWidget()
        self.configlayout = LocationsConfigLayout()
        self.cpclayout = ComputersConfigLayout()
        self.rmlayout = RemoteServersConfigLayout()
        self.tab1 = self.configlayout
        self.tab2 = self.cpclayout
        self.tab3 = self.rmlayout
        self.tab4 = QtGui.QWidget()

        self.tabs.resize(250, 150)
        self.tabs.move(300, 300)
                
        self.tabs.addTab(self.tab1,"Locations")
        self.tabs.addTab(self.tab2,"Computers")
        self.tabs.addTab(self.tab3, "Backup and Retention")
        self.tabs.addTab(self.tab4, "Schedule")
        self.tabs.setGeometry(500, 500, 500, 300)
        self.tabs.setWindowTitle('Bedpost Configuration')

        self.tabs.show()
    


class LocationsConfigLayout(QtGui.QWidget):
    
    def __init__(self):
        super(LocationsConfigLayout, self).__init__()
        
        self.initUI()
    
    def initUI(self):
    
        hbox = QtGui.QHBoxLayout(self)
    
        self.locTable = LocationsTable(25, 4)
        bottom = self.locTable
        
        self.newbtn = QtGui.QPushButton('New Location', self)
        self.newbtn.move(20, 40)
        self.newbtn.clicked.connect(self.newLocation)
        
        self.applybtn = QtGui.QPushButton('Apply Changes', self)
        self.applybtn.move(30, 40)
        self.applybtn.clicked.connect(self.applyChanges)

        self.loconame = QtGui.QLineEdit(self)
        self.loconame.move(40, 40)

        self.locozip = QtGui.QLineEdit(self)
        self.locozip.move(50, 40)

        self.locoaccr = QtGui.QLineEdit(self)
        self.locoaccr.move(60, 40)

        splitter = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter.addWidget(self.loconame)
        splitter.addWidget(self.locozip)
        splitter.addWidget(self.locoaccr)
        splitter.addWidget(self.newbtn)
        splitter.addWidget(self.applybtn)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter)
        splitter2.addWidget(bottom)

        hbox.addWidget(splitter2)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QSplitter')
        # self.show()
    
    def newLocation(self):
        
        self.textLoco, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter location name:')
        
        self.textZip, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter location zip:')
        
        self.textAccr, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter location accronym:')
        
        if ok:
            self.loconame.setText(str(self.textLoco))
            self.locozip.setText(str(self.textZip))
            self.locoaccr.setText(str(self.textAccr))
    

    def applyChanges(self):
        self.jsonLoco = str(self.textLoco)
        print self.jsonLoco
        self.jsonZip = str(self.textZip)
        print self.jsonZip
        self.jsonAccr = str(self.textAccr)
        print self.jsonAccr

        http_client = pyjsonrpc.HttpClient(
            url = "http://localhost:8080/",
        )
        print http_client.call("saveloco", self.jsonLoco, self.jsonZip, self.jsonAccr)
    

class LocationsTable(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setAlternatingRowColors(True)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setLocations()

    def setLocations(self):
        http_client = pyjsonrpc.HttpClient(
            url = "http://localhost:8080/",
            )
        svr_response = http_client.call("returnloco")
        newstruct = {'locations_list': svr_response}
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

#Display configuration panel for computers on the bedpost network. Create new Computers, manage computers table.
class ComputersConfigLayout(QtGui.QWidget):
    
    def __init__(self):
        super(ComputersConfigLayout, self).__init__()
        
        self.initUI()
    
    def initUI(self):
    
        hbox = QtGui.QHBoxLayout(self)
    
        self.cpcTable = ComputersTable(25, 8)
        bottom = self.cpcTable
        
        self.newbtn = QtGui.QPushButton('New Computer', self)
        self.newbtn.move(20, 40)
        self.newbtn.clicked.connect(self.newComputer)
        
        self.applybtn = QtGui.QPushButton('Apply Changes', self)
        self.applybtn.move(30, 40)
        self.applybtn.clicked.connect(self.applyChanges)

        self.cpcname = QtGui.QLineEdit(self)
        self.cpcname.move(40, 40)

        self.cpchostname = QtGui.QLineEdit(self)
        self.cpchostname.move(50, 40)

        self.cpcdomain = QtGui.QLineEdit(self)
        self.cpcdomain.move(60, 40)
        
        self.cpcusername = QtGui.QLineEdit(self)
        self.cpcusername.move(40, 40)

        self.cpcpassword = QtGui.QLineEdit(self)
        self.cpcpassword.move(50, 40)

        self.cpcdatadir = QtGui.QLineEdit(self)
        self.cpcdatadir.move(60, 40)
        
        self.cpcfqdn = QtGui.QLineEdit(self)
        self.cpcfqdn.move(60, 40)

        self.cpclocation = QtGui.QLineEdit(self)
        self.cpclocation.move(60, 40)


        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.cpcname)
        splitter1.addWidget(self.cpchostname)
        splitter1.addWidget(self.cpcdomain)
        splitter1.addWidget(self.newbtn)
        splitter1.addWidget(self.applybtn)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.cpcusername)
        splitter2.addWidget(self.cpcpassword)
        splitter2.addWidget(self.cpcdatadir)
        splitter2.addWidget(self.cpcfqdn)
        splitter2.addWidget(self.cpclocation)

        splitter3 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter3.addWidget(splitter2)
        splitter3.addWidget(bottom)

        hbox.addWidget(splitter3)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QSplitter')
        # self.show()
    
    def newComputer(self):
        
        self.cpcName, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter Computer Name:')
        
        self.cpcHost, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter Computer Hostname:')
        
        self.cpcDomain, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter Computer Domain Name:')

        self.cpcUser, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter Computer Username:')

        self.cpcPass, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter Computer Password:')
        
        self.cpcData, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter Collection Data Directory :')
        
        self.cpcFqdn, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter FQDN:')
        
        #Need to figure out how to do a dropdown, select location from list of locations.
        self.cpcLocation, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter location:')
        
        if ok:
            self.cpcname.setText(str(self.cpcName))
            self.cpchostname.setText(str(self.cpcHost))
            self.cpcdomain.setText(str(self.cpcDomain))
            self.cpcusername.setText(str(self.cpcUser))
            self.cpcpassword.setText(str(self.cpcPass))
            self.cpcdatadir.setText(str(self.cpcData))
            self.cpcfqdn.setText(str(self.cpcFqdn))
            self.cpclocation.setText(str(self.cpcLocation))
    

    def applyChanges(self):
        self.jsonCpcName = str(self.cpcName)
        print self.jsonCpcName
        self.jsonCpcHost = str(self.cpcHost)
        print self.jsonCpcHost
        self.jsonCpcDomain = str(self.cpcDomain)
        print self.jsonCpcDomain
        self.jsonCpcUser = str(self.cpcUser)
        print self.jsonCpcUser
        self.jsonCpcPass = str(self.cpcPass)
        print self.jsonCpcPass
        self.jsonCpcData = str(self.cpcData)
        print self.jsonCpcData
        self.jsonCpcFqdn = str(self.cpcFqdn)
        print self.jsonCpcFqdn
        self.jsonCpcLocation = str(self.cpcLocation)
        print self.jsonCpcLocation

        http_client = pyjsonrpc.HttpClient(
            url = "http://localhost:8080/",
        )
        print http_client.call("savecpc", self.jsonCpcName, self.jsonCpcHost, self.jsonCpcDomain, self.jsonCpcUser, self.jsonCpcPass, self.jsonCpcData, self.jsonCpcFqdn, self.jsonCpcLocation)
    

class ComputersTable(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setComputers()


    def setComputers(self):
        http_client = pyjsonrpc.HttpClient(
            url = "http://localhost:8080/",
            )
        svr_response = http_client.call("returncpcs")
        newstruct = {'cpc_list': svr_response}
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

#Display Creation, and Management Table for Remote SFTP Servers configured for backup of bedpost data.
class RemoteServersConfigLayout(QtGui.QWidget):
    
    def __init__(self):
        super(RemoteServersConfigLayout, self).__init__()
        
        self.initUI()
    
    def initUI(self):
    
        hbox = QtGui.QHBoxLayout(self)
    
        self.rmservertable = RemoteServersTable(25, 7)
        bottom = self.rmservertable

        self.newbtn = QtGui.QPushButton('New Remote Server', self)
        self.newbtn.move(20, 40)
        self.newbtn.clicked.connect(self.newRemoteServer)
        
        self.applybtn = QtGui.QPushButton('Apply Changes', self)
        self.applybtn.move(30, 40)
        self.applybtn.clicked.connect(self.applyChanges)

        self.rmservername = QtGui.QLineEdit(self)
        self.rmservername.move(40, 40)

        self.rmserverip = QtGui.QLineEdit(self)
        self.rmserverip.move(50, 40)

        self.rmserverport = QtGui.QLineEdit(self)
        self.rmserverport.move(60, 40)
        
        self.rmserverdatapath = QtGui.QLineEdit(self)
        self.rmserverdatapath.move(40, 40)

        self.rmserveruser = QtGui.QLineEdit(self)
        self.rmserveruser.move(50, 40)

        self.rmserverpass = QtGui.QLineEdit(self)
        self.rmserverpass.move(60, 40)


        splitter1 = QtGui.QSplitter(QtCore.Qt.Horizontal)
        splitter1.addWidget(self.rmservername)
        splitter1.addWidget(self.rmserverip)
        splitter1.addWidget(self.rmserverport)
        splitter1.addWidget(self.applybtn)
        splitter1.addWidget(self.newbtn)

        splitter2 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter2.addWidget(splitter1)
        splitter2.addWidget(self.rmserverdatapath)
        splitter2.addWidget(self.rmservername)
        splitter2.addWidget(self.rmserverpass)

        splitter3 = QtGui.QSplitter(QtCore.Qt.Vertical)
        splitter3.addWidget(splitter2)
        splitter3.addWidget(bottom)

        hbox.addWidget(splitter3)

        self.setLayout(hbox)

        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QSplitter')
    
    def newRemoteServer(self):
        
        self.rmServerName, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter Remote Server Name:')
        
        self.rmServerIP, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter Remote Server IP:')
        
        self.rmServerPort, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter SFTP Port:')

        self.rmServerDataPath, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter SFTP Data Path:')

        self.rmServerUser, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter SFTP Username:')
        
        self.rmServerPass, ok = QtGui.QInputDialog.getText(self, 'Input Dialog', 
            'Enter SFTP Password :')
        
        if ok:
            self.rmservername.setText(str(self.rmServerName))
            self.rmserverip.setText(str(self.rmServerIP))
            self.rmserverport.setText(str(self.rmServerPort))
            self.rmserverdatapath.setText(str(self.rmServerDataPath))
            self.rmserveruser.setText(str(self.rmServerUser))
            self.rmserverpass.setText(str(self.rmServerPass))


    def applyChanges(self):
        self.jsonRmServerName = str(self.rmServerName)
        print self.jsonRmServerName
        self.jsonRmServerIP = str(self.rmServerIP)
        print self.jsonRmServerIP
        self.jsonRmServerPort = str(self.rmServerPort)
        print self.jsonRmServerPort
        self.jsonRmServerDataPath = str(self.rmServerDataPath)
        print self.jsonRmServerDataPath
        self.jsonRmServerUser = str(self.rmServerUser)
        print self.jsonRmServerUser
        self.jsonRmServerPass = str(self.rmServerPass)
        print self.jsonRmServerPass

        http_client = pyjsonrpc.HttpClient(
            url = "http://localhost:8080/",
        )
        print http_client.call("saveremote", self.jsonRmServerName, self.jsonRmServerIP, self.jsonRmServerPort, self.jsonRmServerDataPath, self.jsonRmServerUser, self.jsonRmServerPass)
    

class RemoteServersTable(QTableWidget):
    def __init__(self, *args):
        QTableWidget.__init__(self, *args)
        self.setShowGrid(False)
        self.verticalHeader().setVisible(False)
        self.horizontalHeader().setVisible(False)
        self.setAlternatingRowColors(True)
        self.setRemoteServers()


    def setRemoteServers(self):
        http_client = pyjsonrpc.HttpClient(
            url = "http://localhost:8080/",
            )
        svr_response = http_client.call("returnremote")
        newstruct = {'remote_list': svr_response}
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
    app.setStyleSheet(" QTableWidget::item:focus { background-color:transparent; color:blue;  border: 0px }" )
    ex = Main()
    sys.exit(app.exec_())



if __name__ == '__main__':
    main()