# -*- coding: utf-8 -*-
"""
Created on Sat Oct 31 19:59:42 2020

@author: user
"""
from datetime import datetime
from Development import Development 
import csv

# should be changed 
pheno_output = "TNG1.csv"

stage = ["播種","萌芽","出土","開花","吐絲"]


flowerdate = []
silkingdate = []
name = []

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
            flowerflag = 0
            silkingflag = 0
            VTdate = 0
            R1date = 0


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
                
                # record flowering and silking date
                # this is add for record the growth stage
                if flowerflag == 0 and maize.stg == 3:
                    VTdate = datestr
                    flowerflag = 1
                if silkingflag == 0 and maize.stg == 4:
                    R1date = datestr
                    silkingflag = 1
                
                daycounter += 1
                if daycounter > 80:
                    break
            # append flowering date and silking date
            flowerdate.append(VTdate)
            silkingdate.append(R1date)
            name.append(outputname)


        with open(outputname,'w',newline='') as csvwrite:
            writer = csv.writer(csvwrite, delimiter=',')
            writer.writerow(['Date', 'leaftip', 'Stage'])
            for r in range(len(pltlv)):
                writer.writerow([pltdate[r],pltlv[r],pltstage[r]])
            print(outputname)
            # print(daycounter)
            #print(outputname,"flowering/silking",flowerdate,silkingdate)
            pltdate.clear()
            pltlv.clear()
            pltstage.clear()

# write phenological stage
with open(pheno_output,'w',newline='') as csvwrite:
    writer = csv.writer(csvwrite, delimiter = ',')
    writer.writerow(['Name','tassel emerge date','silking date'])
    print("write phenological stage")

    for r in range(len(flowerdate)):
        writer.writerow([name[r],flowerdate[r],silkingdate[r]])