# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:56:21 2020

@author: user
"""
2020
from datetime import datetime
from phenology import Development 
import datetime as dtime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates



date0str = input("請輸入播種日期(yyyy-mm-dd):")
startDate = datetime.strptime(date0str,"%Y-%m-%d")
filename = 'out.csv'

daycounter = 0
ptdate =[]
ptlv =[]

#呼叫Development 物件
maize = Development()


# print("播種日期 = ", date0)
with open(filename, newline='') as csvfile:

  wea = csv.reader(csvfile)
  next(wea) # skip title

  for row in wea:

      date = datetime.strptime(row[0],"%Y-%m-%d")
      if date < startDate:
          continue
 
      Temp = row[4:28]
     
      maize.update(Temp)
      stg = maize.stg
      leaftip = int(maize.leafAppeared)
     
      print(date, maize.stage[stg],"葉尖數=",leaftip)
      
      # making plot
      ptdate.append(date)
      ptlv.append(float(maize.leafAppeared))
      daycounter += 1

plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%m/%d'))
plt.scatter(ptdate,ptlv, marker='o')

      