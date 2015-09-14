import subprocess
from PyQt4.QtGui import *
from PyQt4.QtCore import *
 
class downloadStudy():
 
    def __init(self, parent):
        QLabel.__init__(self, parent)
 
    def startDownload(self, loc, bed, fol):

     	cmd = "winscp.com /command \"open \"\"bedpost\"\"\" \"get \"\"/srv/bedpost/"+str(loc)+"/"+str(bed)+"/"+str(fol)+"\"\"\""
     	subprocess.Popen(cmd, shell=True,
           stdout=subprocess.PIPE, 
           stderr=subprocess.PIPE)
        
        print "Done Downloading Transfer from Server"