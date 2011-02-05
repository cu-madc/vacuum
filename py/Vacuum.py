#!/usr/bin/python
#
#  Vacuum.py
# 
#   Created on: 2 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the a vacuum object
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

class Vacuum : 
    # robot vaccum object


    def __init__(self,IDnum,currentTime=0.0,channel=None) : #class constructor
            
        self.xPos   = 1
        self.yPos   = 1
        self.status = 3                        # 1 - moving, 2-cleaning, 3-waiting, 4-repairing
        self.timeDone=currentTime+ \
                       random.randint(10);    # time it will be done with current operation

        self.ghan  = []                       # graphics handle
        self.setID(IDnum)
        self.range = 3                        # maximum distance that can be travelled 
        self.queX  = []
        self.queY  = []
        self.setWorking(True)

        self.setChannel(channel)              #channel to commander
        self.timeToClean=8;
        self.timeToRepair=32;
        self.odometer=0;                      # tracks distance travelled
        self.missions=0;                      #number of cells than have been cleaned
        self.moveCost=1;                      #cost to move
        self.repairCost=30;                   # cost to conduct repair
        self.repairs=0;                       # number of repairs - running total
        
        self.time = 0;


    def setWorking(self,value) :
        self.isWorking = value

    def getWorking(self) :
        return(self.isWorking)

    def getChannel(self) :
        return(self.channel)

    def setChannel(self,value) :
        self.channel = value

    def getPosition(self) :
        return([self.xPos,self.yPos])

    def setPosition(self,pos) :
        self.xPos = pos[0]
        self.yPos = pos[1]

    def getID(self) :
        return(self.IDnum)

    def setID(self,value) :
        self.IDnum = value

    def registerWorld(self,W,command) :
        #make vacuum aware of its world and who is its commander
        self.world=W
        self.commander=command
        #timeHear= addlistener(W,'time','PostSet',@(src,evnt)timeStep(a,src,evnt));% listen to world time-tick    


        
        
        
    def move(self,x,y) :
        # allow for movment of vacuum without cleaning
        
        if (not self.isWorking):
            # not functioning
            return

        
        ordered_distance=abs(self.xPos-x)+abs(self.yPos-y)
        if (ordered_distance <= self.range) :
            self.xPos=x;
            self.yPos=y;
            self.world.addExpenditure(self.moveCost);     # update funds expended
            self.timeDone=self.timeDone+1;
            self.status=1;




    def  moveAndClean(self,x,y) :
        # execute an order to move to new location and clean
        # note - this method will only be called if vacuum is working,
        # so no need to check status
        R=abs(self.xPos-x)+abs(self.yPos-y)   # proposed distance to move
        if (R <= self.range) :
            # move is not too far to achieve
            self.xPos=x
            self.yPos=y
            self.odometer += R
            self.missions += 1
            self.world.addExpenditure(self.moveCost)
            
            if (self.world.Moisture[self.xPos,self.yPos] > 0 ) :
                # location is wet
                # repairs required before cleaning
                self.timeDone=self.world.time+self.timeToRepair 
                self.status=4;
                self.world.addExpenditure(self.repairCost);
                self.repairs += 1;
                
            else :
                self.timeDone=self.world.time+self.timeToClean;
                self.status=2;

            
            self.queX=[]; # reset que


           
    def moveord(self,xord,yord) :
        # update que for new location to clean
        self.queX.append(xord)
        self.queY.append(yord)

        
        
    def timeStep(self,src,evnt) :
        #vacuum action on each world time increment
        if (not self.isWorking) :
            # not functioning
            return
            

        t=self.world.time; 
            
        if (t>=self.timeDone) :
            # Vacuum operation is complete
            if (self.status==2) :
                #just finished cleaning
                # update world that location has been cleaned
                self.world.clean(self.xPos,self.yPos) 
                self.status=3                         # waiting new instruction

                # report that cleaning complete, recieve new instruction
                self.channel.sendReportFromVacuum2Commander(self.xPos,self.yPos,2,self.getID());
                
                #getReport(self.commander,a,self.xPos,self.yPos,2)  # report that cleaning complete, recieve new instruction

                
            elif ((self.status==3) and (len(self.queX)==0)) :
                # nothing in que
                self.channel.sendReportFromVacuum2Commander(self.xPos,self.yPos,self.status,self.getID());
                #getReport(self.commander,a,self.xPos,self.yPos,self.status); # report to commander that vac is waiting

                
            elif (self.status==3) :
                # next job is now qued
                self.moveandclean(self.queX,self.queY);

                
            elif (self.status==4) :
                #repairs complete
                #start cleaning sequence
                self.status=2;          
                self.timeDone=t+self.timeToClean;
                    

            else :
                # vacuum is still doing something
                if ((self.status==2) and (self.world.Moisture(self.xPos,self.yPos)>0)) :
                    # region still wet
                    # assume world will dry, then 8 more time units to complete cleaning
                    self.timeDone=t+self.timeToClean 
                    
            
    
    
if (__name__ =='__main__') :
    world = World()
    world.inc()

    vacuum = Vacuum(1,0.0)
    vacuum.registerWorld(world,None)
    vacuum.move(1,1)
    vacuum.moveAndClean(1,1)
    vacuum.moveord(1,1)
    vacuum.timeStep(1,1)
