# -*- coding: utf-8 -*-
"""
Created on Tue Nov  3 18:03:30 2020

@author: ccchen
"""
import Debelopment
import math

class Leaf:
    maxElongRate = 12 # 12 cm per day at Topt
    LM_min = 97
    
    def __ini__(self,rank):
        self.rank = rank
        self.elongAge = 0
        self.length = 0
        self.growthDuration = 0
        
       
    
    def cal_dimensions(self):
        k = 24
        totalLeaves = Debelopment.totLeafNo
        L_max = math.sqrt(self.LM_min*self.LM_min + k*(totalLeaves- totalLeaves))
        n_m = 5.93 + 0.33*totalLeaves
        a = -10.61 + 0.25*totalLeaves
        b = -5.99 + 0.27*totalLeaves
        ptnLength = L_max*math.exp(a/2*pow(self.rank/n_m-1,2)+b/2+pow(self.rank/n_m-1,3))
        self.growthDuration = ptnLength/self.maxElongRate
    


    def expand(self, dayTemp):
        growthDuration_half = self.growthDuration/2
        
    