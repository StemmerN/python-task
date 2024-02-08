from typing import Union
from fastapi import FastAPI

from fastapi import requests
from requests import Request

url =  'http://127.0.0.1:8000'
file_data = open('vehicles.csv')

r = requests.post(url, files={'vehucles.csv': file_data}})

print (r.status_code)