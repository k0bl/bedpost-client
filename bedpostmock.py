import time
import logging

logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p', filename='bedpostmock.log', level=logging.INFO)
print "This is Bedpost 0.1.2"
print "running now"


count = 1
while count <=10:
    print "Now Transferring bed...."
    logging.info('Starting stage 1')
    count = count+count
    time.sleep(5)  # Delay for 5 seconds (5 seconds)