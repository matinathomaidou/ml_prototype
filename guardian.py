#!/usr/bin/python3
#-*-coding: utf-8 -*-
"""
Created on Wed Apr 26 17:17:57 2017
https://github.com/prabhath6/theguardian-api-python
@author: david
The majority of this code is from https://gist.github.com/dannguyen/c9cb220093ee4c12b840
modifications by mlexperience.org for machine learning experiments

Use of content is subject to the T&C's here
https://www.theguardian.com/open-platform/terms-and-conditions

Specifically - we must not keep content more than 24hours
5. Lifecycle of OP Content
You must either replace (by re-requesting) or delete all OP Content you hold (whether or not published on Your Website) 
at least every 24 hours. For legal reasons, you must not keep any OP Content for longer than 24 hours.

Wiping various collections:
ensures that this program will remove all content before being granted
the right to new content for 24hours 

db.guardian.remove()
db.news.remove()


"""

import config
import requests

import redis
from redis_collections import Dict


from datetime import date, timedelta
import pymongo
from datetime import datetime
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

API_KEY = config.guardian['API_KEY']
API_URL = config.guardian['API_URL']
DATABASE = config.DATABASE

uri = config.uri
client = pymongo.MongoClient(uri)
db = client[DATABASE]

# Sample URL
#
# http://content.guardianapis.com/search?from-date=2016-01-02&
# to-date=2016-01-02&order-by=newest&show-fields=all&page-size=200
# &api-key=your-api-key-goes-here

MY_API_KEY = API_KEY
API_ENDPOINT = API_URL

my_params = {
    'from-date': "",
    'to-date': "",
    'order-by': "newest",
    'show-fields': 'all',
    'page-size': 200,
    'show-tags': 'all',
    'api-key': MY_API_KEY
}


# day iteration from here:
# http://stackoverflow.com/questions/7274267/print-all-day-dates-between-two-dates

start_date = date.today() - timedelta(10)
end_date = date.today() - timedelta(1)
dayrange = range((end_date - start_date).days + 1)
db.guardian.drop()
db.news.drop()
for daycount in dayrange:
    dt = start_date + timedelta(days=daycount)
    datestr = dt.strftime('%Y-%m-%d')
    # then let's download it
    print("Downloading", datestr)
    all_results = []
    my_params['from-date'] = datestr
    my_params['to-date'] = datestr
    current_page = 1
    total_pages = 1
    while current_page <= total_pages:
       print("...page", current_page)
       my_params['page'] = current_page
       resp = requests.get(API_ENDPOINT, my_params)
       data = resp.json()
       all_results.extend(data['response']['results'])
       # if there is more than one page
       current_page += 1
       total_pages = data['response']['pages']

    db.guardian.insert_many(all_results)   
    
for first_article in all_results:
        #words = tokenize(first_article['fields']['bodyText'])  
        rec = {}
        rec['ml_id'] = first_article['id']  #this needs to be a unique incremental number - perhaps MongoDb will help
        rec['link'] = first_article['fields']['shortUrl']
        rec['title'] = first_article['fields']['headline']
        rec['summary'] = first_article['fields']['trailText']
        rec['date'] = first_article['webPublicationDate']
        rec['topic'] = '/' + first_article['sectionName']
        rec['content_type'] = first_article['type']
        rec['publication'] = first_article['fields']['publication']
        rec['published_by'] = first_article['fields']['productionOffice']
        rec['text'] = (first_article['fields']['bodyText']) 
        tags_list = []
        for tag in first_article['tags']:
            tagss = {}          
            tagss['id'] = tag['id']
            tagss['Url'] = tag['webUrl']
            tagss['type'] = tag['type']
            if tagss['type'] in ['keyword','contributor']:
                tags_list.append(tagss)            
            
        rec['tags'] = tags_list
        rec['simlist'] = '' #this needs to be a list of similar documents based on tfidf vector and similarity (GENSIM)
        if(rec['content_type'] == 'article'):
            db.news.insert_one(rec)





