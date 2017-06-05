# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 17:31:25 2017

@author: david
"""

import redis
from redis_collections import Dict

email = 'admin@ml'
email_1 = 'dd'
email_2 = 'bb'
#add a new user
profiles = Dict()

profile = {}
profile['salt'] = 'b'
profile['name'] = ' '
profile['city'] = ' '
profile['news'] = ' '
profile['currency'] = 'gbp'
profile['share'] = ' '
profile['hashed'] = ' '
profile['admin'] = ' '

profiles[email] = profile

conn = redis.Redis('localhost')
conn.hmset("pythonDict", profiles)  
pythonDict =  (conn.hgetall("pythonDict"))

#fetch a single email address
one = conn.hget('pythonDict','admin@mlexperience.org')

#delete a user
two = conn.hdel('pythonDict',email_2)
pythonDict =  (conn.hgetall("pythonDict"))
print(pythonDict)