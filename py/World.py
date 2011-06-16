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

from Channel import Channel
from Router import Router
from Agent import Agent

class  World (Agent):



    def __init__(self,r=1.0,s=1.0,v=1.0,cloudsize=1.0) :
	Agent.__init__(self,Router.WORLD)
        self.time = 0
    
        self.N=5                   # %size of grid
        self.sensor = None         # data as recorded on sensor
        self.expenditure = 0.0     # cummulative funds expended since last reset
        self.numberVacuums = 0     # No vacuums assigned yet.
        self.intializeVariables(r,s,v,cloudsize)

    
    def intializeVariables(self,r,s,v,cloudsize) :
        # initialize the variables this class keeps track of (input rate and size constants)
        self.time=0;
	self.setDirtRate(r)          # rate constant for - events per unit time(world wide)
	self.setDirtSize(s)          # size constant for exponential distribution of sizes
	self.setRainRate(v)          # rate constant for RAIN events - events per unit
	                             # time (world wide)
	self.setRainSize(cloudsize)  # average size of rain event
	

        self.A = zeros((self.N,self.N),dtype=float64)        # array of values for dirt levels
        self.Moisture = zeros((self.N,self.N),dtype=float64) # array of values for moisture level


    def setNumberVacuums(self,number) :
	# Routine to set the value that tracks the number of vacuums.
	self.numberVacuums = number


    def setGridSize(self,N):
	# Routine to set the grid size.
	if(N > self.N) :
	    # Need to add more grids.
	    while(self.N < N) :
		# Add a row and then a column to A and Moisture
		self.A = append(self.A,zeros((1,self.N),dtype=float64),axis=0)
		self.A = append(self.A,zeros((self.N+1,1),dtype=float64),axis=1)

		self.Moisture = append(self.Moisture,zeros((1,self.N),dtype=float64),axis=0)
		self.Moisture = append(self.Moisture,zeros((self.N+1,1),dtype=float64),axis=1)
		self.N += 1

	
	elif (N < self.N) :
	    # Need to delete grids
	    while(self.N > N) :
		# Delete a row and then delete a column from A and Moisture
		self.A = delete(self.A,self.N-1,axis=0)
		self.A = delete(self.A,self.N-1,axis=1)

		self.Moisture = delete(self.Moisture,self.N-1,axis=0)
		self.Moisture = delete(self.Moisture,self.N-1,axis=1)

		self.N -= 1

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
        self.A = random.rand(self.N*self.N).reshape(self.N,self.N)

    def randomMoisture(self) :
        self.Moisture = random.rand(self.N*self.N).reshape(self.N,self.N)


    def addExpenditure(self,value) :
        self.expenditure += value

    def incrementVacuumCount(self):
        self.numberVacuums += 1;
        

    def setDirtRate(self,r) :
        self.r = r                 # rate constant for - events per unit time(world wide)

    def setDirtSize(self,s) :
        self.s = s                 # size constant for exponential distribution of sizes

    def setRainRate(self,v) :
        self.v = v                 # rate constant for RAIN events - events per unit
                                   # time (world wide)

    def setRainSize(self,cloudsize) :
        self.cloudsize = cloudsize # average size of rain event

    def addVacuum(self,vacuum) :
	# This is a dummy method. It is assumed to be overridden by a
	# child class.
	pass

    def deleteVacuum(self,vacuum) :
    	# This is a dummy method. It is assumed to be overridden by a
	# child class.
	pass


    def inc(self) :
        # Take a single time step of the simulated world
            
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


        # Notify the Channel of the current status
        self.channel.sendWorldStatusToSensor(self.A)
        
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


        self.channel.sendWorldWetnessToSensor(self.Moisture)
        self.channel.sendPlannerUpdateRequest()

        for vacuum in range(self.numberVacuums):
	    #print("Sending to vacuum {0}".format(vacuum))
            self.channel.sendVacuumWorldTime(T,vacuum,self.Moisture)
            
        self.time=T;



    @staticmethod
    def spawnWorld(r=1.0,s=1.0,v=1.0,cloudsize=1.0) :
	world = World(r,s,v,cloudsize)
	channel = world.initializeChannel()
	return(world)

            
            
if (__name__ =='__main__') :
    world = World.spawnWorld()
    #world.inc()
    world.randomDust()
    world.randomMoisture()

    print(world.A)
    print(world.Moisture)

    world.setGridSize(8)
    
    print(world.A)
    print(world.Moisture)

    world.setGridSize(3)

    print(world.A)
    print(world.Moisture)
    
