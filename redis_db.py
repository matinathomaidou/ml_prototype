# -*- coding: utf-8 -*-
"""
Created on Mon Jun  5 17:31:25 2017

@author: david
"""

import redis
from redis_collections import Dict

#add a new user
profiles = Dict()
users = Dict()
import yaml

class DBHelper:

    def __init__(self):
        self.db = redis.Redis('localhost')

    def get_user(self, email):
        
            entry = self.db.hget('mluserDict', email)            
            user = {}
            user['email'] = email
            val = yaml.load(entry)
            user['admin'] = val['admin']
            user['hashed'] = val['hashed']
            user['salt'] = val['salt']  
            return user
            

    def add_user(self, email, salt, hashed, is_admin):
        user = {}
        user['salt'] = salt
        user['hashed'] = hashed
        user['admin'] = is_admin        
        users[email] = user
        self.db.hmset("mluserDict", users)  

        profile = {}
        profile['name'] = ' '
        profile['city'] = ' '
        profile['news'] = ' '
        profile['currency'] = ' '
        profile['share'] = ' '
        
        profiles[email] = profile        
        
        self.db.hmset('mlprofileDict',profiles)
        
    def list_user(self):
        users = []
        mluserDict =  (self.db.hgetall("mluserDict"))        
        for entry in mluserDict:
            user = {}
            user['email'] = entry
            val = yaml.load(mluserDict[entry])
            user['admin'] = val['admin']
            user['hashed'] = val['hashed']
            user['salt'] = val['salt']
            users.append(user)
        return users
        
    def del_user(self, email):
        self.db.hdel('mluserDict',email)


    def toggle_admin(self, email):
       user = self.get_user(email) 
       val = 'N'
       if user['admin'] == 'N':
           val = 'Y'
       user['admin'] = val
       users[email] = user   
       self.db.hmset("mluserDict", users)  
        

    def pw_user_update(self, email, salt, hashed, is_admin):
        id = self.get_user(email)
        id['salt'] = salt
        id['hashed'] = hashed
        users[email] = id   
        self.db.hmset("mluserDict", users)  
     

    def user_profile_read(self, email):
        profiler = self.db.hget('mlprofileDict', email)          
        profile = {}
        profile['email'] = email
        val = yaml.load(profiler)
        profile['name'] = val['name']
        profile['city'] = val['city']
        profile['news'] = val['news']
        profile['currency'] = val['currency']
        profile['share'] = val['share']
        return profile

    def user_profile_update(self, email, profile):
        profiles[email] = profile 
        self.db.hmset('mlprofileDict',profiles)

        
    def user_delete(self, email):
        self.db.hdel('mluserDict',email)
        self.db.hdel('mlprofileDict',email)

        