# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 20:14:38 2017

@author: david
"""
import re
 
#This regular expression is the heart of the code.
#Python uses Perl regex, so it should be readily portable
#The r'' string form is just a convenience so you don't have to escape backslashes
COMBINED_LOGLINE_PAT = re.compile(
  r'(?P<origin>\d+\.\d+\.\d+\.\d+) '
+ r'(?P<identd>-|\w*) (?P<auth>-|\w*) '
+ r'\[(?P<date>[^\[\]:]+):(?P<time>\d+:\d+:\d+) (?P<tz>[\-\+]?\d\d\d\d)\] '
+ r'"(?P<method>\w+) (?P<path>[\S]+) (?P<protocol>[^"]+)" (?P<status>\d+) (?P<bytes>-|\d+)'
+ r'( (?P<referrer>"[^"]*")( (?P<client>"[^"]*")( (?P<cookie>"[^"]*"))?)?)?\s*\Z'
)
 
logline = input("Paste the Apache log line then press enter: ")
 
match_info = COMBINED_LOGLINE_PAT.match(logline)
print #Add a new line
 
#Print all named groups matched in the regular expression
for key, value in match_info.groupdict().items():
    print (key, ":", value)