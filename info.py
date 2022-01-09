#!/bin/python

import json
import time

tempeature = '-'
weather = '未知'
response = {}
wind_dir = '东风'
wind_scale = '0'

with open('/home/pi/Desktop/city_weather.json', 'r', encoding='UTF-8') as f:
    response = json.loads(f.read())


if response["code"] == "200":
    tempeature = response["now"]["temp"]
    weather = response["now"]["text"]
    wind_dir = response["now"]["windDir"]
    wind_scale = response["now"]["windScale"]

date = time.strftime("%Y-%m-%d %H:%M", time.localtime())

print("{0}\n上海: {1}, {2}℃\n{3}{4}级".format(date, weather, tempeature, wind_dir, wind_scale))

