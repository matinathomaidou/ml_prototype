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
from wtforms import validators, ValidationError
from wtforms import BooleanField
from wtforms import StringField
from wtforms import HiddenField
from wtforms import TextAreaField
from wtforms import TextField

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
    
class UserPW(Form):
    password = PasswordField('password',validators=[validators.DataRequired(),validators.Length(min=8, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2',validators=[validators.DataRequired(), validators.EqualTo('password', message='Passwords mustmatch')])
    submit = SubmitField('submit', [validators.DataRequired()]) 

class UserPref(Form):
    name = StringField(u'Full Name', [validators.optional(), validators.length(max=10)])
    city = StringField(u'City', [validators.DataRequired(), validators.length(max=200)])
    news_pref = StringField(u'News', [validators.DataRequired(), validators.length(max=200)])
    currency = StringField(u'News', [validators.DataRequired(), validators.length(max=200)])
    share = StringField(u'News', [validators.DataRequired(), validators.length(max=200)])
    submit = SubmitField('submit', [validators.DataRequired()])   
    
class UserLeave(Form):
    bye1 = StringField(u'Leaving', [validators.optional(), validators.length(max=3)])
    bye2 = StringField(u'US', [validators.DataRequired(), validators.length(max=3)])
    submit = SubmitField('submit', [validators.DataRequired()]) 
    
class Feedback(Form):
    model_id = HiddenField(u'Model', [validators.DataRequired(), validators.length(max=10)]) 
    element_id =HiddenField(u'Item', [validators.DataRequired(), validators.length(max=10)]) 
    comment = TextAreaField(u'Comment', [validators.optional(), validators.length(max=100)])
    label = HiddenField(u'Label', [validators.optional(), validators.length(max=100)])
    like = HiddenField(u'Like', [validators.optional()])
    date = HiddenField(u'Date', [validators.DataRequired()])
    agree = HiddenField(u'Comment', [validators.optional(), validators.length(max=100)])
    foll_link = HiddenField(u'Date', [validators.DataRequired()])
    no_show = HiddenField(u'Date', [validators.DataRequired()])
    review = HiddenField(u'Date', [validators.DataRequired()])
    submit = SubmitField('submit', [validators.DataRequired()]) 
    
class ContactForm(Form):
    name = TextField("Name",  [validators.DataRequired(),validators.length(max=10)])
    email = TextField("Email",  [validators.DataRequired(),validators.Email()])
    subject = TextField("Subject",  [validators.DataRequired(),validators.length(max=50)])
    message = TextAreaField("Message",  [validators.DataRequired(),validators.length(max=1000)])
    submit = SubmitField("Send", [validators.DataRequired()])
    
class Email(Form):
    email = EmailField('email',validators=[validators.DataRequired(), validators.Email()])   
    submit = SubmitField("Send", [validators.DataRequired()])
    
class UserPW_Ext(Form):
    password = PasswordField('password',validators=[validators.DataRequired(),validators.Length(min=8, message="Please choose a password of at least 8 characters")])
    password2 = PasswordField('password2',validators=[validators.DataRequired(), validators.EqualTo('password', message='Passwords mustmatch')])
    submit = SubmitField('submit', [validators.DataRequired()])    
    
    
