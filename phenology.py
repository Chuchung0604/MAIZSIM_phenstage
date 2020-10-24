# -*- coding: utf-8 -*-
"""
Created on Sun Oct 18 22:16:45 2020

@author: user
"""

class Development:
    stg = 0 # 生育期的代碼
    stage = ["種子膨大","萌芽","出土","開花"]
    dt = 1/24
    Tbase = 8
    Topt = 32.1
    Tceil = 43.7
    Rmax_LIR = 0.978
    Rmax_LTAR = 0.53 #葉尖出現速率 leaftip/day
    Rmax_Germination = 0.45 #發芽速率
    Rmax_Emergence = 0.2388 # 出土速率
    leaftip = 0
    LvsInitiated = 5 # directe use from MAIZSIM that 5 leaf initiated as emerged
    T_ind = -99
    juvLeafNo = 20 # Bright Jean
    
    # initiation the parameter
    germinated=0 # 0 as un-germinated, 1 as germinated
    emerged=0
    tassellinitiated = 0
    germinationRate = 0
    emergenceRate = 0
    LvsToInduce = 0
    inductions = 0
    phyllochronesFromTI = 0
    
    
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
        
        if self.germinated == 0:
            for h in range(len(dayTemp)):
                self.__class__.germinationRate += self.beta_fn(float(dayTemp[h]),self.Rmax_Germination,self.Topt,self.Tceil)*self.dt
                if self.germinationRate >= 0.5:
                    self.__class__.germinated = 1
                    self.__class__.stg = 1
                    break
        elif self.emerged == 0:
            for h in range(len(dayTemp)):
                self.__class__.emergenceRate += self.beta_fn(float(dayTemp[h]),self.Rmax_Emergence,self.Topt,self.Tceil)*self.dt
                if self.emergenceRate >= 1:
                    self.__class__.emerged = 1
                    self.__class__.stg = 2
                    break
        elif self.tassellinitiated == 0:
            #daycount = 0
            for h in range(len(dayTemp)):
                # leaf initiation
                self.__class__.LvsInitiated += self.beta_fn(float(dayTemp[h]),self.Rmax_LIR,self.Topt,self.Tceil)*self.dt
                # temperature effect on leaf number
                if self.LvsInitiated >= self.juvLeafNo:
                    
                    if self.T_ind == -99:
                        self.__class__.T_ind = float(dayTemp[h])
                    Tind = self.T_ind
                    addLeafTemperature = max(0.0, (13.6 - 1.89*Tind + 0.081*pow(Tind,2) - 0.001*pow(Tind,3)))
                    
                    self.__class__.LvsToInduce = (self.LvsToInduce*self.inductions + addLeafTemperature) / (self.inductions + 1)
                    Tind = (Tind * self.inductions + float(dayTemp[h])) / (self.inductions + 1)
                    self.__class__.inductions += 1
                    
                    acturalAddedLvs = self.LvsInitiated - self.juvLeafNo
                    if acturalAddedLvs >= self.LvsToInduce:
                        youngestLeaf = totLeafNo = int(self.LvsInitiated)
                        self.__class__.tassellinitiated = 1
                # leaf tip
                self.__class__.leaftip += self.beta_fn(float(dayTemp[h]),self.Rmax_LTAR,self.Topt,self.Tceil)*self.dt

        else:
            # tassel initiated
        
            
    def get_stg(self):
        return self.stg
    def get_stage(self):
        return self.stage

    
if __name__ == "__main__" : 
    maiz = Development()
    print(maiz.Tbase)
    print(maiz.beta_fn(20,1,34,44))
    