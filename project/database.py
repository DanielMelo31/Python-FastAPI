from peewee import *
import os
from dotenv import load_dotenv

load_dotenv()

database_connection = MySQLDatabase(
    os.environ.get('DB_NAME'),
    user= os.environ.get('DB_USER'),
    password = os.environ.get('DB_PASWORD'),
    host='localhost',
    port=3306 )

