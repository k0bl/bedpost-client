import subprocess
import requests
import json
from PyQt4.QtGui import *
from PyQt4.QtCore import *
 
class DownloadStudy():
 
    def __init(self):

	def startDownload(self, cid, loc, bed, fol):

		startStatus = "Downloading"
		self.updateTransferStatus(tid, startStatus)
	 	cmd = "winscp.com /command \"open \"\"bedpost\"\"\" \"get \"\"/srv/bedpost/"+loc+"/"+bed+"/"+fol+"\"\"\""
	 	subprocess.Popen(cmd, shell=True,
	       stdout=subprocess.PIPE, 
	       stderr=subprocess.PIPE)
	    
		print "Done Downloading Transfer from Server"
		doneStatus = "Download Complete"
		self.updateTransferStatus(cid, doneStatus)


	def updateTransferStatus(self, cid, status):
	    url = "http://192.168.1.7:5050/"
	    headers = {'content-type': 'application/json'}

	    # Example echo method
	    payload = {
	        "method": "updateDownloadStatus",
	        "params": {"status": status},
	        "jsonrpc": "2.0",
	        "id": tid,
	    }
	    response = requests.post(
	        url, data=json.dumps(payload), headers=headers).json()

	    print response