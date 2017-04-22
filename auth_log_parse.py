#!/usr/bin/python3
#-*-coding: utf-8 -*-
"""
Created on Wed Apr 19 15:45:47 2017

@author: david
"""

import datetime
import json

import codecs
items = []
lines = []
prev_command = ''
with codecs.open('/home/david/sii/log/auth.log','rU','utf-8') as f:
    for line in f:
        log_data = {}
        fields = line.split()
        lines.append(fields)
        log_data['month'] = fields[0]
        log_data['day'] = fields[1]
        log_data['time'] = fields[2]
        log_data['host'] = fields[3].replace('ip-','').replace('-',':')
        comm = fields[4].replace(':','')
        if comm[:4] != 'CRON':
            if comm[:4] == 'sshd':
                if fields[5] == 'Accepted':
                    log_data['tran'] = 'Login -' 
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
       

 
