# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from datetime import datetime,timedelta
from statistics import mean
import csv

future = "future/2020031100_tch.csv"
hist = "Weather/histwea.csv"
out = "test2.csv"

endDate = datetime.strptime("8/8/2020","%m/%d/%Y")

tofile = []

def writeWeather(futurewea,histwea,writewea):
    # read history weather
    with open(histwea, newline='') as histweather:

        wea = csv.reader(histweather)
        header = next(wea)
#        next(wea) # skip title
        
        for row in wea:
          date = datetime.strptime(row[0],"%m/%d/%Y")
          datestr = date.strftime("%Y-%m-%d")
          dayrow = [datestr]
          dayT = []
          for h in range(27):
                dayT.append(float(row[h+1]))
          dayrow.extend(dayT)
          dayrow.append(row[28])
          tofile.append(dayrow)

          if date >= endDate:
              break
    # read predicted weather
    with open(futurewea, newline='') as futureweather:
        wea = csv.reader(futureweather)
        next(wea)
        for row in wea:
            date = date + timedelta(days=1)
            datestr = date.strftime("%Y-%m-%d")
            dayrow = [datestr]
            dayT = []
            for h in range(24):
                dayT.append(float(row[h+1]))
            dayrow.append(round(mean(dayT),1))
            dayrow.append(max(dayT))
            dayrow.append(min(dayT))
            dayrow.extend(dayT)
            dayrow.append(0)
            tofile.append(dayrow)
        
 # write file       
    with open(writewea, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        writer.writerow(header)
        for r in range(len(tofile)):
            writer.writerow(tofile[r])
    


writeWeather(future,hist,out)    



