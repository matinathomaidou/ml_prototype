#!/usr/bin/python3.5
#-*-coding: utf-8 -*-
"""
Created on Wed Apr 12 16:37:19 2017
@author: david
"""

class User:
    def __init__(self, email):
        self.email = email
        
        
    def get_id(self):
        return self.email
        
    def is_active(self):
        return True
        
    def is_anonymous(self):
        return False
        
    def is_authenticated(self):
        return True
        
    def is_admin(self):
        return self.is_admin


