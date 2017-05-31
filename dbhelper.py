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
        profile = {}
        profile['name'] = ' '
        profile['city'] = ' '
        profile['news'] = ' '
        profile['currency'] = ' '
        profile['share'] = ' '
        self.db.user_profiles.insert({'email': email, 'profile' : profile})
        
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
      

    def user_profile_read(self, email):
        profiler_r = self.db.user_profiles.find_one({'email': email})
        return profiler_r['profile']

    def user_profile_update(self, email, profile):
        self.db.user_profiles.update({'email': email}, {'$set' : {'profile' : profile}})
        
    def user_delete(self, email):
        self.db.users.delete_many({'email' : email})
        self.db.user_profiles.delete_many({'email' : email})
    
    def read_news(self):
        news = []
        for art in self.db.news.find():
            article = {}
            article['link'] = art['link']
            article['title'] = art['title']
            article['summary'] = art['summary']
            article['date'] = art['date']
            news.append(article)
        return news

