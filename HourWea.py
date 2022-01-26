# -*- coding: utf-8 -*-
"""
Created on Wed Jan 19 17:09:33 2022

@author: ccchen
"""
import math
import csv
import matplotlib.pyplot as plt
# This submodel was written to simulate hourly temperature from daily value. It was designed to
# connect with process based crop model. The following scripts were rewritten from 2DSOIL model,
# simulators for elements of energy movement within soil profile, I had it from Dr. Timlin. 
# For the concepts of the model, please chek: Timlin, D.J. et al.(2002) Error analysis of soil 
# temperature simulations using measured and estimated hourly weather data with 2DSOIL. 
# Agricultural system 72:215-139.
# Also check Reicosky, D.C. et al. (1989) Accuracy of hourly air temperatures calculated from 
# daily minima and maxima. Agricultural and Forest Meterology, 46: 193-209. That paper describes
# the GLYCIM method on hourly temperature calculation.


# universal variable
DEGRAD = 0.017453293 # 1/180 * pi 

# --------- (read weather submodel)-------
# Read weather file download from TCCIP, two year of data (Tmin and Tmax) were read in the same time 
# and convert list as output for other sub model. The DOY values were used in this model. 
class ReadWea:
    location = ["北部","中部","南部","東部"]
    def __init__(self,yr1):
        self.year1 = yr1 # the fist year value
        self.Tmax = []
        self.Tmin = []
        self.SolRad = []
    
    def histWea(self,lon,lat):
        self.Tmax = self.readValue(lon,lat,self.year1,"最高溫")
        self.Tmin = self.readValue(lon,lat,self.year1,"最低溫")
        self.SolRad = self.readValue(lon,lat,self.year1,"日射量") # (w/m2)
    
    def dayNumbers(self,year):
        if year%4 == 0:
            return 366
        else:
            return 365  

    def readValue(self,lon,lat,year,weatype):
        # read the daily temperature in specsific grid, combine two years
        # to make a long list 

        Value = []
        for i in range(2):
            isFind = False # refresh in each year loop
            for loc in self.location:     
                if isFind == True:
                    break
                filename = "WeaHist/TReAD_日資料_%s_%s/TReAD_日資料_%s_%s_%d.csv" %(
                    loc,weatype,loc,weatype,year+i)
                
                with open(filename, newline='') as readfile:
                    wea = csv.reader(readfile, delimiter = ',')
                    next(wea) # skip header
                    for row in wea:
                        if float(row[0]) == lon:
                            if float(row[1]) == lat:
                                isFind = True
                                for d in range(self.dayNumbers(year+i) + 2):
                                    if d < 2:
                                        continue
                                    Value.append(float(row[d]))
            if year == 2020:
                return Value # return only 2020
        return Value # end of function readTemp
    
    @staticmethod
    def makeTempList(tmin_lst, tmax_lst, DO2Y):
        posit = DO2Y - 1 # the list value started at position 0
        Tmin_yest = tmin_lst[posit-1]      
        Tmax_yest = tmax_lst[posit-1]
        Tmin = tmin_lst[posit]
        Tmax = tmax_lst[posit]
        Tmin_tom = tmin_lst[posit+1]
        Tmax_tom = tmax_lst[posit+1]
        
        tempList = [[Tmin_yest,Tmax_yest], [Tmin,Tmax], [Tmin_tom,Tmax_tom]]
        
        return tempList # end of the function
    
    
#--------- (inciden radiation submodel) ----------

class Radiation:    
    SDERP = [0.3964, 3.631, 0.03838, 0.07659, 0.0, -22.97,-0.3885, -0.1587, -0.01021]
    def __init__(self,lat):
        self.DAYLNG = 0  # day length
        self.DEC = 0.3964 # solar declination
        self.lat = lat
        self.XLAT = lat * DEGRAD # latitude in grade
    
    def theory(self, JDAY):
        DOY = JDAY
        self.solarDeclination(DOY)
        self.dayLength()
        self.WATPOT = self.potentialRad(DOY)

    def solarDeclination(self,JDAY):
        # Roberson and Ruselo (1968)
        self.DEC = self.SDERP[0]
        for i in range(1,5):
            j = i + 4
            D11 = i*0.01721*JDAY            
            self.DEC += self.SDERP[i]*math.sin(D11) + self.SDERP[j]*math.cos(D11)
        self.DEC = self.DEC * DEGRAD
                        
    def dayLength(self):
        # Smithonian Meterological Table, 1966 p. 495
        D12 = math.sin(self.XLAT) * math.sin(self.DEC)
        D13 = math.cos(self.XLAT) * math.cos(self.DEC)
        self.DAYLNG = math.acos((-0.014544 - D12)/D13) * 7.6394
        # 7.6394 = 180/3.1416/360*24*2
        
    def potentialRad(self,JDAY):
        # solar radiation indicent
        D12 = math.sin(self.XLAT) * math.sin(self.DEC)
        D13 = math.cos(self.XLAT) * math.cos(self.DEC) 
        D14 = D12 + D13
        RADVEC = 1 + (0.01674*math.sin(JDAY-93.5)*0.9863*DEGRAD)
        WATATM = 1325.4 * D14/(RADVEC*DEGRAD) # radiation incident at the top of the 
        # atmosphere at noon (W/m2)
        
        # atmospheric transmission 
        if JDAY < 145:
            ATRANS = 0.68 + (145-JDAY)*(1.57*self.lat/30 - 0.1)/1000
        elif JDAY <= 237:
            ATRANS = 0.68
        else:
            if self.lat <= 30:
                D15 = (self.lat * 5.25E-5) - 0.1E-3
            else:
                D15 = 0.65E-3 + self.lat * 3.0E-5
            ATRANS = 0.68 + D15 * (JDAY - 237)
        
        # calculate potential direct + diffuce radiation incident on crop at noon
        potRad = WATATM*0.5*(0.93 - 0.02/D14 + pow(ATRANS,1/D14))
        
        return potRad


class TemperatureHr:
    # generate
    def __init__(self):
        self.Tmax_yest = 24
        self.Tmin_yest = 20
        self.Tmax = 24
        self.Tmin = 20
        self.Tmax_tom = 24
        self.Tmin_tom = 20
        self.WATACT = 200 # W/m2
        self.TempH = {1:10, 2:10, 3:10, 4:10, 5:10, 6:10, 7:10, 8:10, 9:10, 10:10,
                      11:10, 12:10, 13:10, 14:10, 15:10, 16:10, 17:10, 18:10, 19:10,
                      20:10, 21:10, 22:10, 23:10, 24:10} # list content hourly value
    
    def Hourly(self,day_leng,tempList,solRad):

        daylength = day_leng
        self.Tmin_yest = tempList[0][0]
        self.Tmax_yest = tempList[0][1]
        self.Tmin = tempList[1][0]
        self.Tmax = tempList[1][1]
        self.Tmin_tom = tempList[2][0]
        self.Tmax_tom = tempList[1][1]
        self.WATACT = solRad
        self.convertHourly(daylength) # end of the method
        
    def convertHourly(self,daylength):
        DAYLNG = daylength
        DAWN = 12 - (DAYLNG/2)
        DUSK = 12 + DAYLNG/2
        TDUSKY = (self.Tmax_yest + self.Tmin_yest)/2
        # calculate time after doawn in hours when maximum temp is reached
        D20 = 0.0945 - (self.WATACT- 8.06E-5 ) + (self.Tmax * 6.77E-4)
        D21 = self.Tmax/D20/self.WATACT
        D21 = min(D21,1)
        TMAXHR = DAYLNG/math.pi * (math.pi - math.asin(D21))
        # calculate air temp at dusk TDUSK
        D22 = (self.Tmax - self.Tmin) / 2
        D23 = math.pi/TMAXHR
        D24 = 1.5*math.pi
        TDUSK = (D22 * 1.0 + math.sin(D23*DAYLNG + D24)) + self.Tmin
        # some parts of temperature equation
        XTEMP = 5.0
        if self.Tmin < TDUSKY:
            D25 = TDUSKY - self.Tmin + XTEMP
            D26 = math.log(D25/XTEMP) / (2 * DAWN)
        else:
            D27 = (self.Tmin - TDUSKY)/ (2 * DAWN)
            
        if self.Tmin_tom < TDUSK:
            D28 = TDUSK - self.Tmin_tom + XTEMP
            D29 = math.log(D28/XTEMP) / (2 * DAWN)
        else:
            D30 = (self.Tmin_tom - TDUSK) / (2 * DAWN)
        # calculate air temperature at each time
        for h in range(1,25):
            TIMH = h - 0.5
            if TIMH >= DAWN and TIMH <= DUSK: # 白天
                T01 = self.Tmin + D22 * (1 + math.sin(D23*(TIMH-DAWN)+D24))
                self.TempH[h] = T01
            elif TIMH < DAWN: # 清晨
                if self.Tmin < TDUSKY:
                    T01 = self.Tmin - XTEMP + (D25/math.exp(D26*(DAWN + TIMH)))
                    self.TempH[h] = T01
                else:
                    T01 = TDUSKY + D27*(DAWN+TIMH)
                    self.TempH[h] = T01
            elif TIMH > DUSK: # 晚上
                if self.Tmin_tom < TDUSK:
                    T01 = self.Tmin_tom - XTEMP + (D28/math.exp(D29*(TIMH-DUSK)))
                    self.TempH[h] = T01
                else:
                    T01 = TDUSK + D30*(TIMH - DUSK)
                    self.TempH[h] = T01
        # end of the method

    
            
# DEC - solar declination (太陽赤緯)
# DAYLNG - day length (h)
# WATATM - radiation incident at the top of the atmosphere at noon (W/m2)
# WATPOT - potential radiation incident at earth's surface at noon (W/m2)
# WATACT - actual radiation incident at eath's surface at noon (W/m2)
# JDAY - day of year
# h - hour value (0-24)
# TDUSKY - temperature at dusk in yesterday
# TDUSK - temperature at dusk
        

if __name__ == "__main__" : 
    # --------- read the temperature from TCCIP ---------
    # read weather from TCCIP file with specific location by "ReadWea"
    # Wea = ReadWea(2010)
    # Wea.histWea(120.75, 24.3)
    # tmax_lst = Wea.Tmax
    # tmin_lst = Wea.Tmin
    # wat_lst = Wea.SolRad
    # # calculating day length by the "Radiation class"
    # Rad = Radiation(21.3) # activate class with latitude
    # Rad.theory(180) # calculate theory value i.e. daylength, potential solRad(W/m2)
    # dayLength = Rad.DAYLNG
    
    # # make temperature list by the ReadWea.makeTempList method
    # # [[tminY,tmaxY], [tmin,tmax], [tminT,tmaxT]]
    # templst = ReadWea.makeTempList(tmin_lst, tmax_lst, 180)

    # # calculate hourly temperature
    # HourCalculator = TemperatureHr() # create HourTemp object
    # HourCalculator.Hourly(dayLength,templst,wat_lst[180-1])
    # test = HourCalculator.TempH
    # print(test)
    
    #------- have temperature and radiation as input
    JDAY = 3
    latitude = 24.01
    # input
    solRad = 6.15 #(MJ/m2)
    templst = [[16.5,24.9], [18.6,23.4], [16.6,29.8]]
    WAT = 24 * 1000000/(60*60*24) # W/m2
    
    # calculating day length by the "Radiation class"
    Rad = Radiation(latitude) # activate class with latitude
    Rad.theory(JDAY) # calculate theory value i.e. daylength, potential solRad(W/m2)
    dayLength = Rad.DAYLNG
    # calculate hourly temperature
    HourCalculator = TemperatureHr() # create HourTemp object
    HourCalculator.Hourly(dayLength,templst,WAT)
    test = HourCalculator.TempH
    
    tempH_obs = [18.6,18.5,18.5,18.6,18.6,18.5,
                 18.4,18.7,19.4,19.9,20.2,20.7,
                 22.1,22.6,22.6,23.4,23.1,22.3,
                 20.7,20.0,20.1,19.9,19.6,19.0]
    
    
    # --------- make plot
    Hour = []
    tempH_lst = []
    for h in range(1,25):
        Hour.append(h)
        tempH_lst.append(test[h])    
    
    plt.plot(Hour,tempH_lst,label='simulated')
    plt.plot(Hour,tempH_obs,label='observed',color ="#C0C0C0" )
    plt.show()