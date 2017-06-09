#!/usr/bin/python3.5
#-*-coding: utf-8 -*-

import pymongo
import config


uri = config.uri

DATABASE = config.DATABASE


class newsDBHelper:

    def __init__(self):
        client = pymongo.MongoClient(uri)
        self.db = client[DATABASE]

     
    def read_news(self):
        news = []
        for art in self.db.news.find():
            article = {}
            article['link'] = art['link']
            article['title'] = art['title']
            article['summary'] = art['summary']
            article['date'] = art['date']
            article['topic'] = art['topic']
            article['id'] = art['ml_id']
            news.append(article)
        return news

        

