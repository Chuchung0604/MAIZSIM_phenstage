# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 22:16:45 2020

@author: user
"""

class Development:
    #stg = 0 # 生育期的代碼
    stage = ["播種","萌芽","出土","開花","吐絲"]
    dt = 1/24
    Tbase = 8
    Topt = 32.1
    Tceil = 43.7
    Rmax_LIR = 0.978
    Rmax_LTAR = 0.53 #葉尖出現速率 leaftip/day
    Rmax_Germination = 0.45 #發芽速率
    Rmax_Emergence = 0.2388 # 出土速率
    PhyllochronsToTassel = 3
    PhyllochronsToSilk = 3
    juvLeafNo = 16 # Bright Jean
   
    def __init__(self):
        self.stg = 0
        self.germinated = False
        self.emerged = False
        self.tassellinitiated = False
        self.silking = False
        self.tasselFull = False
        self.LvsInitiated = 5
        self.leafAppeared = 0
        self.germinationRate = 0
        self.emergenceRate = 0
        self.LvsToInduce = 0
        self.inductions = 0
        self.phyllochronesFromTI = 0    
        self.T_ind = -99
        self.progressToTasselEmerg = 0
        self.progressToAnthesis = 0
           
    def beta_fn(self,t, Rmax, t_o, t_c):
        t_b = 0
        beta = 1
        if (t <= t_b or t > t_c):
            return 0
        f = (t - t_b) / (t_o - t_b)
        g = (t_c - t) / (t_c - t_o)
        alpha = beta*(t_o - t_b) / (t_c - t_o)
    
        return Rmax*pow(f, alpha)*pow(g, beta)
        

    def update(self,dayTemp):
        
        if self.germinated == False:
            for h in range(len(dayTemp)):
                self.germinationRate += self.beta_fn(float(dayTemp[h]),self.Rmax_Germination,self.Topt,self.Tceil)*self.dt
                if self.germinationRate >= 0.5:
                    self.germinated = True
                    self.stg = 1
                    break
        elif self.emerged == False:
            for h in range(len(dayTemp)):
                self.emergenceRate += self.beta_fn(float(dayTemp[h]),self.Rmax_Emergence,self.Topt,self.Tceil)*self.dt
                if self.emergenceRate >= 1:
                    self.stg = 2
                    self.leafAppeared = 1
                    self.emerged = True
                    break
        elif self.tassellinitiated == False:

            for h in range(len(dayTemp)):
                # leaf initiation
                self.LvsInitiated += self.beta_fn(float(dayTemp[h]),self.Rmax_LIR,self.Topt,self.Tceil)*self.dt
                # temperature effect on leaf number
                if self.LvsInitiated >= self.juvLeafNo:
                    
                    if self.T_ind == -99:
                        self.T_ind = float(dayTemp[h])
                    Tind = self.T_ind
                    addLeafTemperature = max(0.0, (13.6 - 1.89*Tind + 0.081*pow(Tind,2) - 0.001*pow(Tind,3)))
                    
                    self.LvsToInduce = (self.LvsToInduce*self.inductions + addLeafTemperature) / (self.inductions + 1)
                    Tind = (Tind * self.inductions + float(dayTemp[h])) / (self.inductions + 1)
                    self.inductions += 1*self.dt
                    
                    acturalAddedLvs = self.LvsInitiated - self.juvLeafNo
                    if acturalAddedLvs >= self.LvsToInduce:
                        youngestLeaf = totLeafNo = int(self.LvsInitiated)
                        self.tassellinitiated = True
                

        elif self.tassellinitiated == True:
            # tassel initiated
            for h in range(len(dayTemp)):
                self.phyllochronesFromTI +=  self.beta_fn(float(dayTemp[h]),self.Rmax_LTAR,self.Topt,self.Tceil)*self.dt
        
        if self.emerged == True and self.leafAppeared < int(self.LvsInitiated):
            # leaf tip appearance rate
            for h in range(len(dayTemp)):
                self.leafAppeared += self.beta_fn(float(dayTemp[h]),self.Rmax_LTAR,self.Topt,self.Tceil)*self.dt
         
        if self.tassellinitiated == True and (self.leafAppeared > int(self.LvsInitiated)):
            
            if self.tasselFull == False:
                for h in range(len(dayTemp)):
                    self.progressToTasselEmerg += self.beta_fn(float(dayTemp[h]),self.Rmax_LTAR,self.Topt,self.Tceil)*self.dt
            if self.progressToTasselEmerg >= self.PhyllochronsToTassel and self.tasselFull==False:
                self.tasselFull = True
                self.stg = 3

            if self.silking == False and self.tasselFull == True:
                for h in range(len(dayTemp)):
                    self.progressToAnthesis += self.beta_fn(float(dayTemp[h]),self.Rmax_LTAR,self.Topt,self.Tceil)*self.dt
            if self.progressToAnthesis >= self.PhyllochronsToSilk and self.silking == False:
                self.silking = True
                self.stg = 4
       
         
    def get_stg(self):
        return self.stg
    def get_stage(self):
        return self.stage

    
if __name__ == "__main__" : 
    maiz = Development()
    print(maiz.Tbase)
    print(maiz.beta_fn(20,1,34,44))
    