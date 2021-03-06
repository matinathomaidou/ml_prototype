# -*- coding: utf-8 -*-
"""
Created on Sat May 20 09:51:51 2017

@author: david

A small program to work with an RSS feeder
Retrieve news articles
Process the article into a bag of words
Perform classification using a trained model
Find similar articles using TFIDF and GENSIM
Store the RSS portion of the article, the similar documents and class label in MongoDB
for later use in a micro service with Flask
Private research project

Here you will find the HTTP header fields which evenutally get written
to the target server logs and records who we are 
https://en.wikipedia.org/wiki/List_of_HTTP_header_fields

Here you will find the urllib request documentation - used for building the http request logic
https://docs.python.org/3/library/urllib.request.html

Python strip time reference
http://strftime.org/

string to dates courtsey of
https://stackoverflow.com/questions/466345/converting-string-into-datetime

Python datetime library
https://docs.python.org/2/library/datetime.html


"""

from datetime import datetime
import pymongo
import feedparser
from bs4 import BeautifulSoup
import urllib.request
import requests
from nltk import word_tokenize
from nltk.tokenize import RegexpTokenizer
from nltk.tokenize import StanfordTokenizer
from nltk.stem.porter import PorterStemmer
import re
from nltk.corpus import stopwords
from nltk.corpus import reuters
import os
from nltk.parse import stanford
from nltk.tokenize import wordpunct_tokenize
from nltk.tokenize import WordPunctTokenizer
from nltk.tokenize import WhitespaceTokenizer
from nltk.stem.lancaster import LancasterStemmer
from nltk.stem import RegexpStemmer
st = RegexpStemmer('ing$|s$|e$|able$', min=4)
from nltk.stem.snowball import EnglishStemmer
snow = EnglishStemmer()
from nltk.stem import WordNetLemmatizer
wnl = WordNetLemmatizer()
from collections import Counter
import numpy as np
import pandas as pd
import config
#os.environ['STANFORD_PARSER'] = '/Users/David/postagger/stanford-parser-full-2014-08-27/stanford-parser.jar'
#os.environ['STANFORD_MODELS'] = '/Users/David/postagger/stanford-parser-full-2014-08-27/stanford-parser-3.4.1-models.jar'
#parser = stanford.StanfordParser(model_path="/Users/David/postagger/stanford-parser-full-2014-08-27/stanford-parser-3.4.1-models/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz")
cachedStopWords = stopwords.words("english")
#cachedStopWords.append('said')

headers = config.headers
DATABASE = config.DATABASE
uri = config.uri

client = pymongo.MongoClient(uri)
db = client[DATABASE]

current_time = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
def web_scrape(web_index):
    base_path= web_index
    web_path = base_path
    print (web_path)
    #Open and read web page. 
    #Parse returned webpage with BeautifulSoup and extract all the tables in it. 
    request = urllib.request.Request(web_path, headers=headers)
    response = urllib.request.urlopen(request)
    page = response.read().decode('utf-8')        
    soup=BeautifulSoup(page, 'lxml')
    return soup

def web_scrape_alt(web_index):
    base_path= web_index
    web_path = base_path
    print (web_path)
    #Open and read web page. 
    #Parse returned webpage with BeautifulSoup and extract all the tables in it. 
    response = requests.get(web_path, verify=True)
    page = response.content      
    soup=BeautifulSoup(page, 'lxml')
    return soup




    #If encoding cannot be determined exit. #
    #Site declares to be utf-8 so UnicodeDecodeError should not happen - we will see#
      
def tokenize(text):
    min_length = 3
    #tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|\S+')
    words =  map(lambda word: word.lower(), WordPunctTokenizer().tokenize(text))
    #words = list(WhitespaceTokenizer().span_tokenize(text))
    #words = map(lambda word: word.lower(), word_tokenize(text));    
    #words = wordpunct_tokenize(text)
    #word_tokenize = Penn Treebank#
    #words = map(lambda word: word.lower(), tokenizer.tokenize(text));
    #words = list(parser.raw_parse(text,verbose=False))
    #words = map(lambda word: word.lower(), text.split())
    words = [word for word in words
             if word not in cachedStopWords]
    #tokens =(list(map(lambda token: PorterStemmer().stem(token),words)));
    #tokens =(list(map(lambda token: LancasterStemmer().stem(token),words)));
    #tokens =(list(map(lambda token: snow.stem(token),words)));
    #tokens =(list(map(lambda token: st.stem(token),words)));
    tokens =(list(map(lambda token: wnl.lemmatize(token),words)));
    #tokens=words
    p = re.compile('[a-zA-Z]+');
    filter_words = list(filter(lambda token: p.match(token) and len(token)>=min_length, tokens));
    return filter_words      

 

BBC_FEED = 'http://feeds.bbci.co.uk/news/rss.xml'
feed = feedparser.parse(BBC_FEED)
for f in range(0,len(feed)):
    rec = {}   
    simslist = []   
    first_article = feed['entries'][f]
    date_pub = datetime.strptime(first_article['published'], '%a, %d %b %Y %H:%M:%S %Z').replace(hour=0, minute=0, second=0)
    vintage = current_time - date_pub
    if (vintage.days == 1):

        obj = web_scrape_alt(first_article['link'])    
        paras = obj.find_all('p')
        text = ''

        for passage in range (12, len(paras)):
            try:
                if len(paras[passage].text) > 3:
                    text = text + ' ' + (paras[passage].text)
            except:
                continue
 

        words = tokenize(text)  

        rec['ml_id'] = 'todo'  #this needs to be a unique incremental number - perhaps MongoDb will help
        rec['link'] = first_article['link']
        rec['title'] = first_article['title']
        rec['summary'] = first_article['summary']
        rec['bagofwords'] = words 
        rec['date'] = first_article['published']
        rec['topic'] = 'todo' #this needs to be the class label from the machine learning model
        rec['simlist'] = simslist #this needs to be a list of similar documents based on tfidf vector and similarity (GENSIM)

        db.news.insert_one(rec)

    else:
        print(first_article['title'], ' ', first_article['published'], ' not right vintage')
        







#this function just removes these prototyped scrapes for the short while
def others():

    FOX_FEED = 'http://feeds.foxnews.com/foxnews/latest'
    feed1 = feedparser.parse(FOX_FEED)
    first_article = feed1['entries'][0]
    obj = web_scrape_alt(first_article['link'])    
    paras = obj.find_all('p')
    text = ''

    for passage in range (0, len(paras)):
        try:
            if len(paras[passage].text) > 3:
                text = text + ' ' + (paras[passage].text)
        except:
            continue

    words = tokenize(text)   

    REUTERS = 'http://feeds.reuters.com/'
    REUTERS_SUB = ['/news/artsculture',
              '/reuters/businessNews']

    reuters_feed = REUTERS + REUTERS_SUB[0]
    feed2 = feedparser.parse(reuters_feed)
    first_article = feed2['entries'][0]
    obj = web_scrape_alt(first_article['link'])  
    paras = obj.find_all('p')
    text = ''

    for passage in range (0, len(paras)):
        try:
            if len(paras[passage].text) > 3:
                text = text + ' ' + (paras[passage].text)
        except:
            continue

    words = tokenize(text)    

    wired = 'https://www.wired.com/feed'
    feed3 = feedparser.parse(wired)
    first_article = feed3['entries'][1]
    obj = web_scrape_alt(first_article['link'])  
    paras = obj.find_all('p')
    text = ''

    for passage in range (0, len(paras)):
        try:
            if len(paras[passage].text) > 3:
                text = text + ' ' + (paras[passage].text)
        except:
            continue

    words = tokenize(text)  
    return words




