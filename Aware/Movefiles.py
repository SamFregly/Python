import time
import datetime
import sys 
import stat
import os
from time import gmtime, strftime
import subprocess


def movefiles(filename):
       
        ts = time.time()
        now = datetime.datetime.fromtimestamp(ts)
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y%m%d %H:%M:%S')
	#date1 = strftime(a% %d %b %Y, date)
        datemonth= "January" #strftime("%m", gmtime()) # format of strftime is (format code, time object
        datename = strftime(date[0:8])
	source_files = '/home/hofstra/Desktop/Oracle/rawjsondata.txt' # default name to be changed later
        final_files = '/home/hadoop/twitter/d2016/' + datemonth + '/raw/'
	commandmovefile= "sudo hadoop fs -put " + source_files +' ' + final_files
	commandrenamefile = 'sudo hadoop fs -mv '+ final_files + '/Twitter.txt /home/hadoop/twitter/d2016/January/raw'+ datename + '.txt'
        #os.system(commandmovefile)
	#Popen.communicate('its doing the thing')
	os.system(commandrenamefile)
        #return check_output("hadoop fs -ls", shell=True, stderr=subprocess.STDOUT)
	#hopefully sends proper command to command line to be used. stder... is supposed to reat the output
        #when moving creating the raw data files all will be named Twitter.txt and then when exported to the hdfs framework it will be named
        # as set in "final_files"
        #files are named based on their ending time and not starting time. as this prompt will run after stream.py
        #stream.py will send to to the "source_files" location. That will be done completely in crontab.
        # 1. crontab stream.py 2. crontab hadoop (move files) movefiles.py
        #return final_files

print movefiles()
