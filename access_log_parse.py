#!/usr/bin/python3
#-*-coding: utf-8 -*-
"""
Created on Wed Apr 19 15:45:47 2017

@author: david
"""
apache_codes = {'200':	'OK',
'201':	'Created',
'202':	'Accepted',
'203':	'Non-Authorative Information',
'204':	'No Content',
'205':	'Reset Content',
'206':	'Partial Content',
'300':	'Multiple Choices',
'301':	'Moved Permanently',
'302':	'Redirected',
'303':	'See Other',
'304':	'Not Modified',
'305':	'Use Proxy',
'400':	'Bad Request',
'401':	'Authorization Required',
'402':	'Payment Required (not used yet)',
'403':	'Forbidden',
'404':	'Not Found',
'405':	'Method Not Allowed',
'406':	'Not Acceptable (encoding)',
'407':	'Proxy Authentication Required',	
'408':	'Request Timed Out',
'409':	'Conflicting Request',
'410':	'Gone',
'411':	'Content Length Required',
'412':	'Precondition Failed',
'413':	'Request Entity Too Long',
'414':	'Request URI Too Long',
'415':	'Unsupported Media Type',
'500':	'Internal Server Error',
'501':	'Not Implemented',
'502':	'Bad Gateway	',
'503':	'Service Unavailable',
'504':	'Gateway Timeout',
'505':'HTTP Version Not Supported'
}
import datetime
import json
import unicodedata

import codecs
import re


data = []
with codecs.open('/var/log/apache2/access.log','rU','utf-8') as f:
    for line in f:
       try:
           # handle escaped characters
           jline = unicodedata.normalize('NFKC',line)
           # regular expression to take care of it
           re.sub(r'\\x??', '', jline)
           data.append(json.loads(jline))
       except:
           print(line)
           error=line
           continue
   
log = {"items" : data}    
for entry in log['items']:
    time = entry['time'].split()[0].strip().replace('[','')
    time = datetime.datetime.strptime(time, "%d/%b/%Y:%H:%M:%S")
    entry['time'] = str(time)
    entry['status'] = entry['status'] + '-' + apache_codes[entry['status']]

with open('/var/www/ml_prototype/static/log.txt', 'w') as outfile:
    json.dump(log, outfile)    


