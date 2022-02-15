import os
from dotenv import load_dotenv
key = os.environ.get("APP_SETTINGS")
print(key)
print(load_dotenv)
load_dotenv()
key = os.environ.get("APP_SETTINGS")
print(key)
