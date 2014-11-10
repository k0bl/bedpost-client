import sys
import requests
import json
from PyQt4 import QtGui, QtCore

class Example(QtGui.QWidget):
    
    def __init__(self):
        super(Example, self).__init__()
        
        self.initUI()
        
    def initUI(self):      

        hbox = QtGui.QHBoxLayout(self)

        startb = QtGui.QPushButton('Start Transfers', self)
        startb.clicked[bool].connect(self.startTransfer)        

        self.setLayout(hbox)
        QtGui.QApplication.setStyle(QtGui.QStyleFactory.create('Cleanlooks'))
        
        self.setGeometry(300, 300, 300, 200)
        self.setWindowTitle('QtGui.QSplitter')
        self.show()

    def startTransfer(self):
        url = "http://localhost:4000/"
        headers = {'content-type': 'application/json'}

        # Example echo method
        payload = {
            "method": "xfer",
            "params": {"username": "csherer"},
            "jsonrpc": "2.0",
            "id": 0,
        }
        response = requests.post(
            url, data=json.dumps(payload), headers=headers).json()

        print response

def main():
    
    app = QtGui.QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()   