# -*- coding: utf-8 -*-
"""
This is used to combine the observed and predicted weather data for runing simulation model.

This is a temporary script file.
"""


from datetime import datetime,timedelta
from statistics import mean
import csv

# future = "future/2020031100_tch.csv"
# hist = "Weather/histwea.csv"
# out = "test2.csv"


def writeWeather(endRealDate,histwea,futurewea,stdwea,writewea):
    # make end date of future 
    endDate = datetime.strptime(endRealDate,"%m/%d/%Y")
    tofile = []
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
            lastPredictday = date
    # read standard weather
    with open(stdwea, newline='') as stdweather:
        wea = csv.reader(stdweather)
        next(wea)
        for row in wea:
            date = datetime.strptime(row[0],"%m/%d/%Y")
            if date <= lastPredictday:
                continue
     
            datestr = date.strftime("%Y-%m-%d")
            dayrow = [datestr]
            dayT = []
            for h in range(27):
                dayT.append(float(row[h+1]))
            dayrow.extend(dayT)
            dayrow.append(row[28])
            tofile.append(dayrow)
            
        
        
 # write file       
    with open(writewea, 'w',newline='') as csvwrite:
        writer = csv.writer(csvwrite, delimiter=',')
        writer.writerow(header)
        for r in range(len(tofile)):
            writer.writerow(tofile[r])
    

with open("makeweather.csv",newline="") as csvbatch:
    batch = csv.reader(csvbatch)
    next(batch)
    for row in batch:
        # endRealDate = row[0]
        # histwea = row[1]
        # futurewea = row[2]
        # writewea = row[4]
        writeWeather(row[0],row[1],row[2],row[3],row[4] )
        print(row[0])



