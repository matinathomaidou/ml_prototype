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
with codecs.open('/home/david/sii/log/auth.log','rU','utf-8') as f:
    for line in f:
        log_data = {}
        date = line[:15]
        date = datetime.datetime.strptime(date, "%b %d %H:%M:%S")
        date = date.replace(year=current.year)
        log_data['date'] = str(date)   
        log_data['dmy'] = (str(date.year) + '/' + str(date.month) + '/' + str(date.day))
        fields = line.split()
        lines.append(fields)
        log_data['host'] = fields[3].replace('ip-','').replace('-',':')
        comm = fields[4].replace(':','')
        if comm[:4] != 'CRON':
            if comm[:4] == 'sshd':
                if fields[5] == 'Accepted':
                    log_data['tran'] = 'Login -' 
                    if (fields[8] == 'ubuntu'):
                        log_data['user'] = 'xxxx'
                    else:    
                        log_data['user'] = fields[8] 
                    log_data['from'] = fields[10]

                elif fields[6] == 'reset':
                    log_data['tran'] = 'Failed Login'
                    log_data['user'] = fields[10]
                    log_data['from'] = fields[8] 
                    
                elif fields[5] == 'Invalid':
                    log_data['tran'] = 'Invalid user ' 
                    log_data['user'] = fields[7] 
                    log_data['from'] = fields[9]
                        
        try:        
            if(log_data['tran']):
                items.append(log_data)
        except:
            continue
log = {'items' : items}
with open('/home/david/mlexperience/static/auth_log.txt', 'w') as outfile:
    json.dump(log, outfile)  
       

 
