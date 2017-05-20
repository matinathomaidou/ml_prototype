# -*- coding: utf-8 -*-
"""
Created on Sat May 20 09:51:51 2017

@author: david
"""

import feedparser
from bs4 import BeautifulSoup
import urllib.request



def web_scrape(web_index):
    base_path= web_index
    web_path = base_path
    print (web_path)
    #Open and read web page. 
    #Parse returned webpage with BeautifulSoup and extract all the tables in it. 
    request = urllib.request.Request(web_path)
    response = urllib.request.urlopen(request)
    page = response.read().decode('utf-8')        
    soup=BeautifulSoup(page, 'lxml')
    return soup

    #If encoding cannot be determined exit. #
    #Site declares to be utf-8 so UnicodeDecodeError should not happen - we will see#
      

BBC_FEED = 'http://feeds.bbci.co.uk/news/rss.xml'
feed = feedparser.parse(BBC_FEED)
first_article = feed['entries'][0]

obj = web_scrape(first_article['id'])    
paras = obj.find_all('p')
text = ''

for passage in range (12, len(paras)):
    try:
        if len(paras[passage].text) > 3:
            text = text + ' ' + (paras[passage].text)
    except:
        continue
 
   
