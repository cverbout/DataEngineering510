# -*- coding: utf-8 -*-
"""RestAPI.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1I3OKFLg2hPcfRtYVgHAUBP1ZhzfwWxHV
"""

import requests
import json
import datetime
from datetime import datetime, timedelta

api_key = 'd5bef28b992f5cae3668c6d11562142d'
base_url = 'http://api.openweathermap.org/data/2.5/weather?'
city_name = 'Portland'

complete_url = base_url + 'appid=' + api_key + '&q=' + city_name
print(complete_url)
response = requests.get(complete_url)

x = response.json()
print(x)

def isItRainingNow(city_name):
    base_url = 'http://api.openweathermap.org/data/2.5/weather?'
    x = requests.get(base_url + 'appid=' + api_key + '&q=' + city_name).json()
    weather = x['weather'][0]['main']
    if weather == 'Rain':
        print('It is raining')
        return True
    else:
        print('It is not raining')
        return False

city_name = 'Portland'
isItRainingNow(city_name)

def isItRainingThen(city_name, days_from_now):
  base_url = 'http://api.openweathermap.org/data/2.5/forecast?'
  x = requests.get(base_url + '&q=' + city_name + '&appid=' + api_key).json()
  forecast = []
  future = datetime.now() + timedelta(days=days_from_now)
  for entry in x['list']:
     date_obj = datetime.strptime(entry['dt_txt'], '%Y-%m-%d %H:%M:%S')
     if date_obj.day == future.day:
        forecast.append(entry)
  for interval in forecast:
    if interval['weather'][0]['main'] == 'Rain':
      print('It will rain at some point')
      return True

  print('It will not rain')
  return False

days_from_now = 3
city_name = 'Portland'
isItRainingThen(city_name, days_from_now)