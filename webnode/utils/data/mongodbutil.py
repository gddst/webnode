#!/usr/bin/env python
'''
Created on Dec 15, 2015

@author: gddst
'''
import pymongo
from pymongo.mongo_client import MongoClient


class MongoDBUtil(object):
    '''
    '''

    def __init__(self, params):
        '''
        Constructor
        '''
    @staticmethod
    def dump(host, port=27017):
        return MongoClient(host, 27017)
        
if __name__=='__main__':
    print dir(pymongo)
    client = MongoClient('localhost', 27017)
    db = client.resbot
    collection = db.user_profile

    cursor= collection.find()
    obj =cursor.next()
    while obj:
        print obj
        obj=cursor.next()
