import os
from os import environ,getenv
import logging
from logging.handlers import RotatingFileHandler

BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
APP_ID = int(os.environ.get("APP_ID", "2468192")) #Your API ID from my.telegram.org
API_HASH = os.environ.get("API_HASH", "4906b3f8f198ec0e24edb2c197677678") #Your API Hash from my.telegram.org
#--------------------------------------------

DB_URI = os.environ.get("DATABASE_URL", "")
DB_NAME = os.environ.get("DATABASE_NAME", "Filter2")
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
PORT = os.environ.get('PORT', '8080')
