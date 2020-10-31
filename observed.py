# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 15:37:08 2020

@author: user
"""

from datetime import datetime
import csv
import matplotlib.pyplot as plt
import matplotlib.dates as mdates


filename = 'obs.csv'

dateleaf =[]
leaftip = []
dateflowering = []
flowering = []
datesilking = []
silking = []

with open(filename, newline='') as csvfile:

  wea = csv.reader(csvfile)
  next(wea) # skip title
  next(wea)

  for row in wea:
      # read date
      date = datetime.strptime(row[0],"%Y-%m-%d")
      
      # leaf tip number
      if row[1] == '':
          pass    
      else:
          obs = float(row[1])
          leaftip.append(obs)
          dateleaf.append(date) 
          
     # flowering
      if row[2] == '':
          pass     
      else:
          flowering.append(float(row[2]))
          dateflowering.append(date)
          
      # silking
      if row[3] == '':
          pass  
      else:
          silking.append(float(row[3]))
          datesilking.append(date)


  
if __name__ == "__main__" : 
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%b/%d'))
    plt.xlabel('Date')
    plt.ylabel('Leaf tip')

    plt.scatter(dateleaf,leaftip, marker='x')
    plt.scatter(dateflowering,flowering, marker='2')
    plt.scatter(datesilking,silking, marker='1')
    plt.show()


    
