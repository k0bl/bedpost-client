from datetime import datetime
import ConfigParser
import os
import sys
import logging
import atexit
#import paramiko
from datetime import datetime
from shutil import copytree,rmtree
import json
import sqlite3
import unicodedata

version = 'v0.1'
database = 'bedposttest.db'

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='bedpost.log', level=logging.INFO)
logging.info('Bedpost %s is starting...', version)


def startingTransfer(cpc, name):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    #persist new values to sqlite3 database
    dbcpc = str(cpc)
    dbname = str(name)
    dbstarted_at = str('null')
    dbstatus = str('In Queue')
    dbtimedone = str('null')
    print "Starting Transfer"
    print "Collection PC", dbcpc
    print "Study Name", dbname
    print "Current Status", dbstatus
    c.execute ("INSERT INTO transfers VALUES (null, ?, ?, ?, ?, ?);", (dbcpc, dbtimedone, dbname, dbstarted_at, dbstatus))
    print "Insertion is done...giggity"
    conn.commit()
    conn.close()
    

def transferring(cpc, name, started_at):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    #persist new values to sqlite3 database
    dbcpc = str(cpc)
    dbstarted_at = started_at
    dbname = name
    dbstatus = str('Transferring')
    c.execute("UPDATE transfers SET status=?, started_at=?  WHERE name=?", (dbstatus, dbstarted_at, dbname))
    print "update is done...giggity"
    conn.commit()
    conn.close()


def transferComplete(cpc, name, timedone):
    conn = sqlite3.connect(database)
    c = conn.cursor()
    #persist new values to sqlite3 database
    dbcpc = str(cpc)
    dbtimedone = str(timedone)
    dbname = name
    dbstatus = str('Transfer Complete')
    c.execute("UPDATE transfers SET status=?, time_done=?  WHERE name=?", (dbstatus, dbtimedone, dbname))
    print "update is done...giggity"
    conn.commit()
    conn.close()


#test getting values from database. 
#First need to get the beds and their datapath

# def returncpcs():
#     conn = sqlite3.connect(database)
#     c = conn.cursor()
#     c.execute('SELECT cpc_datadir FROM collection_pcs')
#     results = c.fetchall()
#     r2 = str(results)[1:-1]
#     r3 = r2.encode('ascii', 'ignore')
#     return r3

#Duration timer 
starttime = datetime.now()
def goodbye():
    runtime = datetime.now() - starttime
    logging.info('Bedpost took %s to complete.', runtime)
atexit.register(goodbye)

# Read configuration
config = ConfigParser.SafeConfigParser({'retries': 10, 'purge': False})
if not os.path.exists('bedpost.ini'):
    logging.critical('Configuration not found.')
    sys.exit(1)

config.read('bedpost.ini')

workstations = config.sections()
if len(workstations) < 1:
    logging.critical('Configuration error: No workstations defined in configuration')
    sys.exit(1)
print workstations

retries = 5
purge = False
try:
    sftp_server = config.get('DEFAULT', 'sftp_server')
    sftp_port = config.getint('DEFAULT', 'sftp_port')
    sftp_path = config.get('DEFAULT', 'sftp_path')
    sftp_user = config.get('DEFAULT', 'sftp_user')
    sftp_pass = config.get('DEFAULT', 'sftp_pass')
    data_path = config.get('DEFAULT', 'data_path')
except Exception as e:
    logging.critical('Configuration error: %s', e)
    sys.exit(1)

logging.debug('Retries: %s', retries)
logging.debug('Purge: %s', purge)
logging.debug('Local Data Path: %s', data_path)
logging.debug('SFTP Server: %s', sftp_server)
logging.debug('SFTP Port: %s', sftp_port)
logging.debug('SFTP User: %s', sftp_user)
logging.debug('SFTP Path: %s', sftp_path)
logging.debug('Workstations: %s', workstations)

# Stage 1
# Copy studies from the workstations to data_path
print "Starting Stage 1"
print workstations

logging.info('Starting stage 1')

for current in workstations:
    print current
    logging.info('Processing %s', current)
    logging.debug('Source Path: %s', current)
    #attempt to get a directory listing from source path
    try:
        studies = os.listdir(current)
        print studies
    except:
        errno, error = sys.exc_info()[1]
        logging.warning('Unable to get list of studies from %s. Error %s: %s. Continuing...', current, errno, error)
        continue #with next workstation
    else:
        logging.debug('Studies: %s', studies)

    for entry in studies:
        if entry.lower() == 'sandman.sdb':
            logging.debug('Skipping sandman.sdb')
            continue #with next entry

        srcname = os.path.join(current, entry)
        dstname = os.path.join(data_path, entry)
        logging.debug('Source Name: %s', srcname)
        logging.debug('Dest Name: %s', dstname)
        
        #StartTransfer
        startingTransfer(current, srcname)
        
        if os.path.isdir(dstname):
            logging.info('%s already exists in %s. Skipping...', entry, data_path)
            continue #with next entry

        #TODO: Need to know if there's a way to tell if a test is still in progress via some sort of lock file
    
    for entry in studies:
        if entry.lower() == 'sandman.sdb':
            logging.debug('Skipping sandman.sdb')
            continue #with next entry

        srcname = os.path.join(current, entry)
        dstname = os.path.join(data_path, entry)
        logging.debug('Source Name: %s', srcname)
        logging.debug('Dest Name: %s', dstname)
        
        
        
        if os.path.isdir(dstname):
            logging.info('%s already exists in %s. Skipping...', entry, data_path)
            continue #with next entry
        
        logging.info('Copying %s', srcname)
        tstart1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        transferring(current, srcname, tstart1)
        #attempt to copy the study with retries.
        success = False
        for attempt in range(1, retries+1):
            try:
                copytree(srcname, dstname)
                print srcname, dstname

            except:
                errno, error = sys.exc_info()[1]
                logging.warning('Attempt %s failed. Unable to copy %s. Error %s: %s', attempt, srcname, errno, error)
            else:
                if purge:
                    try:
                        rmtree(srcname)
                    except:
                        logging.warning('Unable to purge %s. Continuing...', srcname)
                logging.info('Done')
                success = True

            if success == True:
                break #out of retry loop early
            tcomplete1 = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            transferComplete(current, srcname, tcomplete1)
        else:
            logging.warning('Copying %s has failed too many times. Continuing...', srcname)
            continue #with next entry

logging.info('Stage 1 has finished')
## Stage 2
## Copy all to sftp server

# logging.info('Starting stage 2')

# studies = os.listdir(data_path)
# logging.debug('Studies: %s', studies)

# try:
#     t = paramiko.Transport((sftp_server, sftp_port))
#     t.connect(username=sftp_user, password=sftp_pass)
#     sftp = paramiko.SFTPClient.from_transport(t)
# except Exception, e:
#     logging.critical('Connection Error: %s', e)
#     sys.exit(1)
# else:
#     logging.info('Connected to %s', sftp_server);

# try:
#     sftp.mkdir(sftp_path)
#     logging.info('Created %s on sftp server', sftp_path)
# except IOError:
#     logging.info('Assuming %s exists on sftp server', sftp_path)

# logging.info('Getting list of uploaded studies')
# try:
#     uploaded_studies = sftp.listdir(sftp_path)
# except Exception, e:
#     logging.critical('Error occurred attempting to get list of studies. %s', e)
#     sys.exit(1)
# else:
#     logging.debug('Uploaded Studies: %s', uploaded_studies)


# for entry in studies:
#     if entry in uploaded_studies:
#         logging.warning('%s already exists on sftp server. Continuing.', entry)
#         continue
#     logging.info('Processing %s', entry);
#     study_src = os.path.join(data_path, entry)
#     study_dst = "/".join((sftp_path, entry))
#     logging.debug('Study Source: %s', study_src)
#     logging.debug('Study Destination: %s', study_dst)
#     try:
#         sftp.mkdir(study_dst)
#         for root, dirs, files in os.walk(study_src):
#             relpath = os.path.relpath(root, study_src)
#             logging.debug("Root: %s", root)
#             logging.debug("Relpath: %s", relpath)
#             logging.debug("Dirs: %s", dirs)
#             logging.debug("File Count: %s", len(files))
#             logging.info('In %s', root)
#             for mydir in dirs:
#                 path = "/".join((study_dst, relpath, mydir))
#                 logging.info('Creating %s', path)
#                 sftp.mkdir(path)
#             for myfile in files:
#                 src = os.path.join(root, myfile)
#                 dst = "/".join((study_dst, relpath, myfile))
#                 logging.debug('src: %s', src)
#                 logging.debug('dst: %s', dst)
#                 logging.info('Copying %s', src)
#                 sftp.put(src, dst)

#     except Exception, e:
#         logging.critical('An error occurred: %s', e)
#         sys.exit(1)
#     else:
#         if purge:
#             path = os.path.join(data_path, entry)
#             try:
#                 rmtree(path)
#             except:
#                 logging.warning('Unable to purge %s. Continuing...', path)

# t.close()
