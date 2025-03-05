import os 
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MOGO_DB_URL = os.getenv("MOGO_DB_URL")
print(MOGO_DB_URL)