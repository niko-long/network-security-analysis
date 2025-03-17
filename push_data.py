import os 
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MOGO_DB_URL = os.getenv("MOGO_DB_URL")
print(MOGO_DB_URL)

import certifi #certifi 是一个 Python 库，提供最新的 SSL 证书，用于安全连接 HTTPS 服务器或 MongoDB Atlas。
               #certifi.where() 返回 SSL 证书文件的路径，ca 存储该路径，用于确保 MongoDB 连接使用最新的可信证书。
ca=certifi.where()

import pandas as pd
import numpy as np
import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            print(data.head())
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records

            self.mongo_client = pymongo.MongoClient(MOGO_DB_URL)

            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return (len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e, sys)


if __name__ == '__main__':
    FILE_PATH = os.path.join(os.getcwd(), "Network_Data", "phisingData.csv")
    DATABASE = "XIAOLONG_MLOPS"
    Collection = "NetworkData"
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    #print(records)
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, Collection)
    #print(no_of_records)