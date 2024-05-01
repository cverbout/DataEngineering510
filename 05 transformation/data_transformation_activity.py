# -*- coding: utf-8 -*-
"""Data Transformation Activity.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1YJKhscjH7b01LJl-wBgCmw803UD1Bazy
"""

import pandas as pd
url = 'https://drive.google.com/uc?export=download&id=1G4MUbdUFeACgjGcg6dcwykBZn21zg1jO'
df = pd.read_csv(url)
df.head()

df2 = df.drop('EVENT_NO_STOP', axis=1)
df2.head()

df3 = df2.drop(['GPS_SATELLITES', 'GPS_HDOP'], axis=1)
df3.head()

url = 'https://drive.google.com/uc?export=download&id=1G4MUbdUFeACgjGcg6dcwykBZn21zg1jO'
df4 = pd.read_csv(url, usecols=['EVENT_NO_TRIP', 'OPD_DATE', 'VEHICLE_ID', 'METERS', 'ACT_TIME', 'GPS_LONGITUDE', 'GPS_LATITUDE'])
df4.head()

def create_pd_datetime(row):
  return pd.to_datetime(row['OPD_DATE'], format="%d%b%Y:%H:%M:%S") + pd.to_timedelta(row['ACT_TIME'], unit='s')

df4['TIMESTAMP'] = df4.apply(create_pd_datetime, axis=1)
df4.head()

df5 = df4.drop(['OPD_DATE', 'ACT_TIME'], axis=1)
df5.head()

df5['dMETERS'] = df5['METERS'].diff()
df5['dTIMESTAMP'] = df5['TIMESTAMP'].diff()
df5.head()

df5['dMETERS'].fillna(0)
df5['dTIMESTAMP'].fillna(pd.Timedelta(seconds=0))
df5['dTIMESTAMP_seconds'] = df5['dTIMESTAMP'].dt.total_seconds()
df5['SPEED'] = df5.apply(lambda row: row['dMETERS'] / row['dTIMESTAMP_seconds'] if row['dTIMESTAMP_seconds'] != 0 else 0, axis=1)

df5.head()

df5['SPEED'].describe()