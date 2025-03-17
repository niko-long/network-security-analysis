import pymongo
import os
from dotenv import load_dotenv

# 载入 .env 文件
load_dotenv()
MONGO_DB_URL = os.getenv("MONGO_DB_URL")

client = pymongo.MongoClient(MONGO_DB_URL)

db = client["XIAOLONG_MLOPS"]  # 确保这个数据库名正确
collection = db["NetworkData"]  # 确保这个集合名正确
print("Databases:", client.list_database_names())
print("Collections in XIAOLONG_MLOPS:", db.list_collection_names())

# 统计数据库里有多少条数据
print("Documents count:", collection.count_documents({}))

# 看看第一条数据长什么样
print("First document:", collection.find_one())
