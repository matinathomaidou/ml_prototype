#!/usr/bin/python3
#-*-coding: utf-8 -*-
"""
Created on Wed Apr 19 15:45:47 2017

@author: david
"""

import datetime
import json
import time
cur_yymm = (time.strftime("%x"))
current = datetime.datetime.strptime(cur_yymm, "%m/%d/%y")

import codecs
items = []
lines = []
prev_command = ''
with codecs.open('/var/log/vsftpd.log','rU','utf-8') as f:
    for line in f:
        log_data = {}
        date = line[:25].strip()
        date = datetime.datetime.strptime(date, "%a %b %d %H:%M:%S %Y")
        log_data['date'] = str(date)   
        log_data['dmy'] = (str(date.year) + '/' + str(date.month) + '/' + str(date.day))
        fields = line.split()
        lines.append(fields)
        if (fields[8] == 'OK'):
            log_data['tran'] = fields[9]
            try:
                log_data['obj'] = fields[12]
            except:
                log_data['obj'] = ''
                    
            if(fields[7] == '[mlexpftp]') :
                log_data['user'] = 'xxxx'
            else:
                log_data['user'] = fields[7]
             
            items.append(log_data)
        
        
log = {'items' : items}
with open('/var/www/ml_prototype/static/ftp_log.txt', 'w') as outfile:
    json.dump(log, outfile)  
       

 
