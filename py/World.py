#!/usr/bin/python
#
#  world.py
# 
#   Created on: 1 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the world object used in the vacuum
#       simulation.
# 
#  This material is based on research sponsored by DARPA under agreement
#  number FA8750-10-2-0165. The U.S. Government is authorized to
#  reproduce and distribute reprints for Governmental purposes
#  notwithstanding any copyright notation thereon.
# 
#  The views and conclusions contained herein are those of the authors
#  and should not be interpreted as necessarily representing the official
#  policies or endorsements, either expressed or implied, of DARPA or the
#  U.S. Government.
# 
#  ==========================================================================
# 
#  For use by entities other than the U.S. Government the following
#  additional limitations apply:
# 
#  Copyright (c) 2011, Clarkson University
#  All rights reserved.
# 
#  Redistribution and use in source and binary forms, with or without
#  modification, are permitted provided that the following conditions are
#  met:
# 
#  * Redistributions of source code must retain the above copyright
#  notice, this list of conditions and the following disclaimer.
# 
#  * Redistributions in binary form must reproduce the above
#  copyright notice, this list of conditions and the following
#  disclaimer in the documentation and/or other materials provided
#  with the distribution.
# 
#  * Neither the name of the Clarkson University nor the names of its
#  contributors may be used to endorse or promote products derived
#  from this software without specific prior written permission.
# 
#  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#  HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
# 
#  (license copied from http://www.opensource.org/licenses/bsd-license)
# 
# 
# 
# 


from numpy import *
from numpy.linalg import *

class  World :  # (handle) :



    def __init__(self,r=1.0,s=1.0,v=1.0,cloudsize=1.0) :

        self.time = 0
    
        self.N=5                   # %size of grid
        self.vacuumArray = []      # array of object handles
        self.sensor = None         # data as recorded on sensor
        self.planner = None        # handle to planning processor
        self.g_handle = None       # handle to worlddraw graph
        self.expenditure = 0.0     # cummulative funds expended since last reset
        self.intializeVariables(r,s,v,cloudsize)

    
    def intializeVariables(self,r,s,v,cloudsize) :
        # initialize the variables this class keeps track of (input rate and size constants)
        self.time=0;
        self.r = r                 # rate constant for - events per unit time(world wide)
        self.s = s                 # size constant for exponential distribution of sizes
        self.v = v                 # rate constant for RAIN events - events per unit
                                   # time (world wide)
        self.cloudsize = cloudsize # average size of rain event

        self.A = zeros(self.N*self.N,dtype=float64)        # array of values for dirt levels
        self.A = self.A.reshape(self.N,self.N)
        self.Moisture = zeros(self.N*self.N,dtype=float64) # array of values for moisture level
        self.Moisture = self.Moisture.reshape(self.N,self.N)




        
    def clean(self,x,y) :
        # reset location x,y dirt level to 0
        self.A[x,y] = 0.0


    def minDust(self) :
        return(min(self.A))


    def maxDust(self) :
        return(max(self.A))

    def getNumber(self) :
        return(self.N)


    def getArray(self) :
        return(self.A)

    def randomDust(self) :
        self.A = random.rand(self.N*self.N)
        self.A = self.A.reshape(self.N,self.N)


    def addExpenditure(self,value) :
        self.expenditure += value

    def addVacuum(self,vacuum) :
        self.vacuumArray.append(vacuum)

    def setSensor(self,sensor) :
        self.sensor = sensor

    def getSensor(self) :
        return(self.sensor)

    def setPlanner(self,planner) :
        self.planner = planner

    def getPlanner(self) :
        return(self.planner)

    def getVaccuums(self) :
        return(self.vacuumArray)


    def inc(self) :
        # single time step of simulated world
            
        # dustfall procedure -----
        t=self.time;               # start time
        T=t+1;                     # final time
        tau=-log(random.rand(1)[0])/self.r ; #time until first event
        t=t+tau;
            
        while(t<T) :
            # accumulate dirt until next event falls past final time
            dustball=-log(random.rand(1.0)[0])*self.s; # dustball size
            Ix=random.randint(self.N);                 # select site
            Iy=random.randint(self.N);                 # select site
            self.A[Ix,Iy] = self.A[Ix,Iy]+dustball;    # update the dustlevel
            tau=-log(random.rand(1.0)[0])/self.r ;     # time until next event
            t=t+tau;
            # end dustfall
            
        # drying
        self.Moisture[self.Moisture>0] -= 1;
            
        # rainfall procedure -----
        t=self.time;                           # start time
        tau=-log(random.rand(1.0)[0])/self.v   #time until first event
        t=t+tau

            
        while (t<T) :
            # accumulate dirt until next event falls past final time
            Ix=random.randint(self.N);                 # select site
            Iy=random.randint(self.N);                 # select site

            #uniform 0# to 200# of average
            self.Moisture[Ix,Iy] += ceil(2*random.rand(1.0)[0]*self.cloudsize);
                               
            tau=-log(random.rand(1.0)[0])/self.v ;   #time until next event
            t=t+tau;
            # end rainfall

        if(self.sensor) :
            self.sensor.measure()

        for vacuum in self.vacuumArray:
            vacuum.timeStep(None,None)
            
        self.time=T;

        
            
            
if (__name__ =='__main__') :
    world = World()
    world.inc()
