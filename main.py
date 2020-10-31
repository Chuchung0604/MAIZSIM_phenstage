# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:56:21 2020

@author: user
"""
from datetime import datetime
from Development import Development 
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import observed as obs


date0str = input("請輸入播種日期(yyyy-mm-dd):")

startDate = datetime.strptime(date0str,"%Y-%m-%d")
filename = 'wea2.csv'


daycounter = 0
pltdate =[]
pltlv =[]
pltstage = []

#呼叫Development 物件
maize = Development()
print(type(maize))


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
      pltdate.append(date)
      pltlv.append(float(maize.leafAppeared))
      pltstage.append(stg)
      daycounter += 1
      if daycounter > 80:
          break




lable_corn =  ["Sowing","Germination","Sowing","Flowering","Silking"]
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b%d'))
plt.xlabel('Date')
plt.ylabel('Leaf tip')



plt.scatter(pltdate,pltlv, c=pltstage)
plt.scatter(obs.dateleaf,obs.leaftip,marker='x')
plt.scatter(obs.dateflowering,obs.flowering, marker='2')
plt.scatter(obs.datesilking,obs.silking, marker='1')

plt.show()

