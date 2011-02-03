#!/usr/bin/python
#
#  SensorArray.py
# 
#   Created on: 2 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the Sensor Array object.
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

from World import World


class SensorArray :

    def __init__(self,accuracy=0.0,world=None) :
        # constructor (accuracy of measurement, world object)
        self.accuracy=accuracy-float(int(accuracy))  #force to be within constraints

        self.world = world
        if(world) :
            self.N=world.getNumber();
        else :
            self.N = 1

        self.array = zeros(self.N*self.N,dtype=float64) # array of values for dirt levels
        self.array = self.array.reshape(self.N,self.N)

        self.Wet = zeros(self.N*self.N,dtype=float64)   # array of values for dirt levels
        self.Wet = self.array.reshape(self.N,self.N)

        self.setWorking(True)

        self.channel = 0                               # handle to channel to planner


    def setWorking(self,value) :
        self.isWorking = value

    def getWorking(self):
        return(self.isWorking)
        

    def getChannel(self) :
        return(self.channel)

    def setChannel(self,value) :
        self.channel = value

    def getArray(self) :
        return(self.array)

    def getWet(self) :
        return(self.Wet)

    #events %sense
    #    sense; % sensor taking action - triggers action in planner
    #end
    


    
    
    def measure(self) :
        # measure the world and return data

        dirtLevel=[]
        wetted=[]
        if (self.world and self.isWorking):
            actualdata=self.world.getArray()     #get real world values

            #adjust for noise
            #print(actualdata)
            self.array=actualdata*(1.0+2.0*self.accuracy*(random.rand(self.world.getNumber())-0.5))
            #print(self.array)
         
            dirtLevel=self.array;
            self.Wet=(self.world.Moisture>0);
            wetted=self.Wet;

        return([dirtLevel,wetted])



if (__name__ =='__main__') :
    world = World()
    world.randomDust()
    sensor = SensorArray(0.2,world)
    sensor.measure(world)

