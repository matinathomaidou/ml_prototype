#!/usr/bin/python3.5
#-*-coding: utf-8 -*-

import pymongo
import config


uri = config.uri

DATABASE = config.DATABASE


class DBHelper:

    def __init__(self):
        client = pymongo.MongoClient(uri)
        self.db = client[DATABASE]

    def get_user(self, email):
        return self.db.users.find_one({"email": email})  

    def add_user(self, email, salt, hashed, is_admin):
        self.db.users.insert({"email": email, "salt": salt, "hashed": hashed, "admin": is_admin})
        
    def list_user(self):
        users = []
        for user in self.db.users.find():
            users.append(user)
        return users
        
    def del_user(self, email):
        self.db.users.remove({"email": email})

    def toggle_admin(self, email):
       val = 'N'
       if self.db.users.find_one({"email": email})['admin'] == 'N':
           val = 'Y'
       self.db.users.update({"email": email}, {"$set": {"admin": val}})
        

    def pw_user_update(self, email, salt, hashed, is_admin):
        self.db.users.update({"email": email}, {"$set": {"salt": salt, "hashed":hashed}})
      

        

