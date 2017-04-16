#!/usr/bin/python3.5
#-*-coding: utf-8 -*-
"""
Created on Wed Apr 12 19:23:42 2017

@author: david
"""

from wtforms import Form
from wtforms import PasswordField
from wtforms import SubmitField
from wtforms.fields.html5 import EmailField
from wtforms import validators
from wtforms import BooleanField

class RegistrationForm(Form):
    email = EmailField('email',validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password',validators=[validators.DataRequired(),validators.Length(min=8, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2',validators=[validators.DataRequired(), validators.EqualTo('password', message='Passwords mustmatch')])
    submit = SubmitField('submit', [validators.DataRequired()])
    
class LoginForm(Form):
    loginemail = EmailField('email', validators=[validators.DataRequired(), validators.Email()])
    loginpassword = PasswordField('password', validators=[validators.DataRequired(message="Password field is required")])
    submit = SubmitField('submit', [validators.DataRequired()])
    
class AdminUserCreateForm(Form):
    email = EmailField('email',validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password',validators=[validators.DataRequired(),validators.Length(min=8, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2',validators=[validators.DataRequired(), validators.EqualTo('password', message='Passwords mustmatch')])
    admin = BooleanField('Is Admin ?')
    submit = SubmitField('submit', [validators.DataRequired()])

class AdminUserUpdateForm(Form):
    email = EmailField('email',validators=[validators.DataRequired(), validators.Email()])
    admin = BooleanField('Is Admin ?')
    submit = SubmitField('submit', [validators.DataRequired()])
    
class AdminUserPW(Form):
    email = EmailField('email',validators=[validators.DataRequired(), validators.Email()])
    password = PasswordField('password',validators=[validators.DataRequired(),validators.Length(min=8, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2',validators=[validators.DataRequired(), validators.EqualTo('password', message='Passwords mustmatch')])
    submit = SubmitField('submit', [validators.DataRequired()])    
    
    
    
    

    
    
    
    
