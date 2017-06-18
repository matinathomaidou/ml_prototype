# -*- coding: utf-8 -*-
"""
Created on Sun Jun 18 15:48:54 2017

@author: david
"""
import config
if config.test:
    from mockdbhelper import MockDBHelper as DBHelper
else:
    if config.db == 'redis':    
        from redis_db import DBHelper
    else:
        from dbhelper import DBHelper
    

from passwordhelper import PasswordHelper
from newsdbhelper import newsDBHelper

DB = DBHelper()
PH = PasswordHelper()
model_db = newsDBHelper()

#function to migrate from non email validation to email_validation
#first thing is to create the object from the class DBHelper()
#this only works for the Mongo backend at the moment
#first step is to pull a list of all users

users = DB.list_user()
print(users)

#second step
#is to iterate over each user and call the     def email_val(self, email, val):
#method of DBHelper() to manage the set-up of validated emails
#all existing accounts will be considered validated

for user in users:
    email = user['email']
    DB.email_val(email, True)
    print(user)

#third step
#reload the user list
#check for successful migration of email_validation feature
users = DB.list_user()
print(users)
    