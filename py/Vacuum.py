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

from Channel import Channel
from Router import Router
from Agent import Agent
from XML.XMLMessageForAgent import XMLMessageForAgent


class Vacuum (Agent): 
    # robot vaccum object


    def __init__(self,IDnum,currentTime=0.0,channel=None) : #class constructor
	Agent.__init__(self,Router.VACUUM)
	
        self.xPos   = 0
        self.yPos   = 0
        self.setStatus(3)                     # 1 - moving, 2-cleaning, 3-waiting, 4-repairing
        self.initializeTime(currentTime)      # time it will be done with current operation
        self.setID(IDnum)
        self.range = 3                        # maximum distance that can be travelled 
        self.moveQueue  = []

        self.setChannel(channel)              #channel to commander
        self.timeToClean=8;
        self.timeToRepair=32;
        self.odometer=0;                      # tracks distance travelled
        self.missions=0;                      #number of cells than have been cleaned
        self.moveCost=1;                      #cost to move
        self.repairCost=30;                   # cost to conduct repair
        self.repairs=0;                       # number of repairs - running total
        
        self.time = 0;

        self.Moisture = None
	#print("Creating vacuum {0}/{1}".format(IDnum,id(self.moveQueue)))



    def setChannel(self,value) :
        Agent.setChannel(self,value)
        if(self.channel) :
            pos = self.getPosition()
            self.sendPlannerVacuumMovedPosition(self.IDnum,pos[0],pos[1])

    def setWetness(self,wet) :
        self.Moisture = wet

    def getWetness(self) :
        return(self.Moisture)

    def getPosition(self) :
	# routine to determine the current position of the vacuum.
	
	if(self.queue.empty()):
	    # the queue is empty. Just return the current position.
	    return([self.xPos,self.yPos])

	else:
	    # There are requests in the queue. Empty it out and use
	    # the latest valid request.
	    while(not self.queue.empty()):
		pos = self.queue.get()
		self.move(pos[0],pos[1])


	return([self.xPos,self.yPos])

    def setPosition(self,pos) :
        self.xPos = pos[0]
        self.yPos = pos[1]

    def getID(self) :
        return(self.IDnum)

    def setID(self,value) :
        self.IDnum = value
	#print("Setting id: {0}-{1}".format(self.IDnum,value))

    def setStatus(self,value) :
        self.status = value




    def initializeTime(self,currentTime) :
        self.timeDone=currentTime+random.randint(10);
        
        
    def move(self,x,y) :
        # allow for movment of vacuum without cleaning

        if (self.isWorking):
            # this vacuum is functioning
	    ordered_distance=abs(self.xPos-x)+abs(self.yPos-y)
	    if (ordered_distance <= self.range) :
		self.setPosition([x,y]);
		self.sendVacuumWorldExpenditure(self.moveCost,self.IDnum)
		#self.timeDone += 1;
		#self.status=1;




    def  moveAndClean(self,x,y) :
        # execute an order to move to new location and clean
        # note - this method will only be called if vacuum is working,
        # so no need to check status
        R=abs(self.xPos-x)+abs(self.yPos-y)   # proposed distance to move

        if (R <= self.range) :
            # move is not too far to achieve
            self.setPosition([x,y])
            self.odometer += R
            self.missions += 1
            self.sendVacuumWorldExpenditure(self.moveCost,self.IDnum)

            # Let the planner know that I have moved.
            #print("Moving vacuum {0}".format(self.IDnum))
            self.sendPlannerVacuumMovedPosition(self.IDnum,x,y)
            
            
            if ((type(self.Moisture) is ndarray) and (self.Moisture[x,y] > 0 )) :

                # location is wet
                # repairs required before cleaning
                self.timeDone=self.time+self.timeToRepair 
                self.status=4;
                self.sendVacuumWorldExpenditure(self.repairCost,self.IDnum)
                self.repairs += 1;
                
            else :
                self.timeDone=self.time+self.timeToClean;
                self.status=2;

            
            ##?? self.moveQueue=[]; # reset queue


           
    def moveord(self,xord,yord) :
        # update que for new location to clean
        self.moveQueue.append([xord,yord])
	#import random
	#print("moveord {0} : {1} - {2}".format(self.IDnum,self.moveQueue,id(self.moveQueue)))
	#print("Me: {0}".format(id(self)))
        
        
    def timeStep(self,time,wetness) :
        #vacuum action on each world time increment
        #print("Vacuum.timeStep ID: {0} Time: {1} working: {2} pos: {3},{4} wetness:\n{5}".format\
        #     (self.getID(),time,self.isWorking,self.xPos,self.yPos,wetness))

	self.checkIncomingQueue()
        self.setWetness(wetness)

        if (not self.isWorking) :
            # not functioning
            return
            

        self.time=time;
        #print("timeStep: {0} ID: {1} [{4},{5}] status: {2} queue: {3} ".format(
	#    time,self.IDnum,self.status,self.moveQueue,self.xPos,self.yPos))
	#print("Me: {0}".format(id(self)))
            
        if (self.time>=self.timeDone) :
            # Vacuum operation is complete
            if (self.status==2) :
                #just finished cleaning
                # update world that location has been cleaned
                self.channel.sendWorldCleanedGrid(self.IDnum,self.xPos,self.yPos)
                self.status=3                         # waiting new instruction

                # report that cleaning complete, recieve new instruction
                self.sendReportFromVacuum2Commander(
                    self.xPos,self.yPos,2,self.getID());
                

            elif ((self.status==3) and (len(self.moveQueue)==0)) :
                # nothing in queue
		#print("Vacuum.timeStep - sending report to vacuum")
                self.sendReportFromVacuum2Commander(
                    self.xPos,self.yPos,self.status,self.getID());

                
            elif (self.status==3) :
                # next job is in the queue
                pos = self.moveQueue.pop()
		#print("Vaccum.timeStep - moving vacuum to new pos: {0},{1}".format(pos[0],pos[1]))
                self.moveAndClean(pos[0],pos[1]);

                
            elif (self.status==4) :
                #repairs complete
                #start cleaning sequence
                self.status=2;          
                self.timeDone=self.time+self.timeToClean;
                    

            elif (self.Moisture):
                # vacuum is still doing something
                if ((self.status==2) and (self.Moisture(self.xPos,self.yPos)>0)) :
                    # region still wet
                    # assume world will dry, then 8 more time units to complete cleaning
                    self.timeDone=self.time+self.timeToClean

	    if(self.queueUse) :
		self.queue.put([self.xPos,self.yPos])



    # Method to handle an incoming message and determine what to do
    def handleMessage(self,type,passedInformation) :
	#print("Vacuum.handleMessage: {0} - {1}".format(type,passedInformation))

	if (type=="Move Order") :
	    posX      = int(passedInformation["xPos"])
	    posY      = int(passedInformation["yPos"])
	    self.moveord(posX,posY)

	elif (type=="World Time") :
	    time     = int(passedInformation["time"])
            vacuumID = int(passedInformation["vacuumID"])
	    self.timeStep(time,passedInformation["array"])



    ## sendReportFromVacuum2Commander
    #
    # Routine to take a message from the vacuum that is a report for
    # the commander. This routine relays that report to the commander.
    def sendReportFromVacuum2Commander(self,xPos,yPos,status,IDnum) :
	#Channel.checkInfoType = True
	#print("Vacuum.sendReportFromVacuum2Commander - sending vacuum to commander")
	report = XMLMessageForAgent()
	report.ReportFromVacuum2Commander(xPos,yPos,status,IDnum)
	self.channel.sendString(Router.COMMANDER,report.xml2Char(),-1,False)



    ## sendPlannerVacuumMovedPosition
    #
    # Routine to send the new position of a vacuum. This comes from a
    # vacuum and is sent to a planner.
    def sendPlannerVacuumMovedPosition(self,idnum,xpos,ypos) :
	#print("Vacuum.sendPlannerVacuumMovedPosition sending information.")
        update = XMLMessageForAgent()
        update.PlannerVacuumMovedPosition(idnum,xpos,ypos)
	self.channel.sendString(Router.PLANNER,update.xml2Char())



    ## sendVacuumWorldExpenditure
    #
    # Routine to send an expenditure from a vacuum to the world. 
    def sendVacuumWorldExpenditure(self,expenditure,id) :
	#print("Vacuum.sendVacuumWorldExpenditure - sending information")
	newExpenditure = XMLMessageForAgent()
	newExpenditure.VacuumWorldExpenditure(expenditure,id)
	self.channel.sendString(Router.WORLD,newExpenditure.xml2Char(),id)






    # Routine to handle the reset requests
    def restart(self) :
	#self..shutdownServer()
	self.setWorking(True)
	self.setStatus(3)
	self.initializeTime(0.0)




    # Static method that is used as a helper to make it easier to
    # create a vacuum object.
    @staticmethod
    def spawnVacuum(IDnum,currentTime=0.0) :
	vacuum = Vacuum(IDnum,currentTime,None)
	channel = vacuum.initializeChannel()
	return(vacuum)

    
    
if (__name__ =='__main__') :

    vacuum = Vacuum(1,0.0)
