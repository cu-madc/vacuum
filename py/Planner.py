#!/usr/bin/python
#
#  Planner.py
# 
#   Created on: 1 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the planner object used in the vacuum
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
from World import World
from SensorArray import SensorArray

class Planner :


    def __init__(self,errGrowth,dirtRate,sensor,world) :
        
        # define the
        #     variance growth parameter,
        #     average dirt fall,
        #     handle to sensor,
        #     handle to array of vacuums)
        N = world.getNumber()
        self.setNumber(N)
        self.vacuumRange = 3

        # Initialize the matrices.
        self.worldview = zeros((N,N),dtype=float64);
        self.dirtLevels = []
        self.wetview = zeros((N,N),dtype=float64);
        self.viewPrecision = zeros((N,N),dtype=float64);
        
        self.errGrowth=errGrowth      # estimated growth in variance
        self.dirtRate=dirtRate        #

        # Define the other objects that need to be tracked.
        self.setWorld(world)
        self.setSensor(sensor)
        self.setChannel(None)

        self.setWorking(True)
        self.vacuumlocation = []
        
        #create distance matrix
        self.defineDistanceArray()
        self.wDist=0;               # default
        
        

    def setNumber(self,value) :
        self.N = value

    def getNumber(self) :
        return(self.N)
    
    def setWorking(self,value) :
        self.isWorking = value

    def getWorking(self) :
        return(self.isWorking)

    def setSensor(self,value) :
        self.sensor = value

    def getSensor(self) :
        return(self.sensor)

    def setWorld(self,value) :
        self.world = value

    def getWorld(self) :
        return(self.world)

    def getWorldView(self) :
        return(self.worldview)

    def getDirtLevels(self):
        return(self.dirtLevels)

    def setDirtLevels(self,value):
        self.dirtLevels = value
        
    def getArray(self) :
        return(self.worldview)

    def setChannel(self,value) :
        self.channel = value

    def getChannel(self) :
        return(self.channel)

    def getWet(self):
        return(self.wetview)

    def setWet(self,value) :
        self.wetview = value

    def setVacuumLocation(self,id,x,y) :
        while(id>=len(self.vacuumlocation)) :
            self.vacuumlocation.append(None)
        self.vacuumlocation[id] = [x,y]


    def defineDistanceArray(self) :
        # Define the array that keeps track of the distances between
        # places in the world. This is used by the vacuums to
        # determine how far two cells are from one another.

        # This is a list of lists. The list is of the form
        #   self.Z[i][j]
        # This entry in the list contains an array which has the
        # distance away each coresponding cell in the array is from
        # cell (i,j).

        N = self.getNumber()
        self.Z = range(N)
        for i in range(N) :
            self.Z[i] = range(N)
            for j in range(self.getNumber()) :

                # Figure out the distance each cell is from the cell
                # given at row i and column j.
                distance = zeros((N,N),dtype=int16);

                for m in range(N) :
                    for n in range(N) :
                        # Use a Manhatten distance away from cell i,j.
                        distance[m,n] = abs(m-i) + abs(n-j)

                # Set the entry in the list to be the array just
                # calculated.
                self.Z[i][j] = distance


    def updateView(self) :
        # triggered by world time tick - update planner's view of world
        if not self.getWorking() :
            return

        # update for error growth due to dynamics
        self.viewPrecision=self.viewPrecision/(1+self.errGrowth*self.viewPrecision);  # entry by entry - ok
        mu_0=self.worldview+self.dirtRate; # matrix + scalar
        tau_0=self.viewPrecision;          # matrix
            
        # get data from sensor, if available
        self.channel.sendMeasuredFromPlanner2Sensor()
            
        # update levels based on sensor information
        # (Bayesian update - see wikipedia page for now)
        if len(self.dirtLevels) == 0 :
            # no data available  
            self.worldview=mu_0; # adjust dirt ONLY FOR DYNAMICS
        else :
            # data available 
            # bayes update on dirt  
            tau=3./((self.sensor.accuracy**2)*self.sensor.array+1.0);  # Uniform error/assumes exact information from sensor (??)
            mu=self.dirtLevels;
            self.worldview=(tau_0*mu_0+tau*mu)/(tau_0+tau);            # update assuming normal
            self.viewPrecision=tau+tau_0;
            # see http://en.wikipedia.org/wiki/Conjugate_prior for details.

            
    def receiveReport(self,x,y) :
        # update worldview based on report that location was cleaned
        if not self.getWorking() :
            return
            
        self.worldview[x,y]=0;                     # update level
        self.viewPrecision[x,y]=1/self.errGrowth;  # updated modelled error



    def receiveOrder(self,IDnum,x,y) :
        # report of order to a vacuum to clean a location
        # keep updated status on expected vacuum locations
        if not self.getWorking() :
            return

        while(IDnum >= len(self.vacuumlocation)) :
            self.vacuumlocation.append([])
           
        self.vacuumlocation[IDnum] = [x,y];



    def recommendOrder(self,id,xPos,yPos) :
        # decide on recommended order for a vacuum
        if not self.getWorking() :
            return([])

        #print("recommend order: {0} {1} {2}".format(id,xPos,yPos))
        if(len(self.vacuumlocation)>id) :
            self.setVacuumLocation(id,xPos,yPos)
        else :
            return

        A=self.worldview
        distance = self.Z[xPos][yPos]
        
        A[distance>self.vacuumRange] = -1;  # out of range
        A[self.wetview>0] = -1              # exclude wetted locations
        for loc in self.vacuumlocation :
            A[loc[0],loc[1]] = -1           # exclude where robot already assigned.
            
        # distance weighting
        for i in range(self.vacuumRange) :
            A[distance==i]=A[distance==i]*(1+self.wDist*i);

        I = argmax(A)
        xord = I/self.getNumber()
        yord = I%self.getNumber()
        #print("view: {0}\n {1}: {2} {3} from {4} {5}".format(A,I,xord,yord,xPos,yPos))
        #raw_input("Press Enter to continue...")
        self.channel.sendRecommendOrderFromPlanner2Commander(xord,yord,id)
    


if (__name__ =='__main__') :
    from Channel import Channel
    from Commander import Commander

    world = World()
    sensor = SensorArray(0.1,world)
    planner = Planner(0.2,0.1,sensor,world)

    #N = world.getNumber()
    #for i in range(N) :
    #    for j in range(N) :
    #        print("\n\nRow: {0} Col: {1}\n{2}".format(i,j,planner.Z[i][j]))

    #print("Val: {0}".format(planner.Z[1][2][3,4]))
    planner.receiveOrder(0,2,3)
    planner.setChannel(Channel(world,[],sensor,planner,Commander()))
    planner.recommendOrder(0)
