import mysql.connector
import requests
import json
from app import *

class Database:
    @staticmethod
    def getItems():
        response = requests.post(url=url + '/api/get-items')
        return response.json()