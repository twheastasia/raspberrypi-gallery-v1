#!/bin/python

import requests
import json
import time

key = "xxxx"
location_id = "101020100" # 上海
# location_id = "101161301" # 白银

url = "https://devapi.qweather.com/v7/weather/now?key={0}&location={1}".format(key, location_id)

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

if response.status_code == 200:
    ffw = open('/home/pi/Desktop/city_weather.json', 'w', errors='ignore')
    ffw.write(response.text)
    ffw.close()
    print('Updated!')
else:
    print('Nothing Change.')
