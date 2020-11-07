# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 19:59:42 2020

@author: user
"""
from datetime import datetime
from Development import Development 
import csv

stage = ["播種","萌芽","出土","開花","吐絲"]

# read and write file - weaname, startdate, ouputname
with open('batch.csv',newline='') as batchfile:
    runs = csv.reader(batchfile)
    next(runs) # read the title out
    # read each row of batch file
    for run in runs:
        weaname = run[0]
        startdate = datetime.strptime(run[1],"%m/%d/%Y")
        outputname = run[2]

# initialize parameter
        daycounter = 0
        pltdate =[]
        pltlv =[]
        pltstage = []

    # call Development object
        maize = Development()

        with open(weaname, newline='') as csvfile:

            wea = csv.reader(csvfile)
            next(wea) # skip title
            leaftip = 0
            stg = 0


            for row in wea:
                date = datetime.strptime(row[0],"%Y-%m-%d")
                if date < startdate:
                    continue
                Temp = row[4:28]
     
                maize.update(Temp)
                stg = stage[maize.stg]
                leaftip = round(maize.leafAppeared,2)
                
                datestr = date.strftime("%Y-%m-%d")
     
                pltdate.append(datestr)
                pltlv.append(leaftip)
                pltstage.append(stg)
                
                daycounter += 1
                if daycounter > 80:
                    break


        with open(outputname,'w',newline='') as csvwrite:
            writer = csv.writer(csvwrite, delimiter=',')
            writer.writerow(['Date', 'leaftip', 'Stage'])
            for r in range(len(pltlv)):
                writer.writerow([pltdate[r],pltlv[r],pltstage[r]])
            print(outputname)
            print(daycounter)
            pltdate.clear()
            pltlv.clear()
            pltstage.clear()
