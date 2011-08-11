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
#  This material is based on research sponsored by AFRL under agreement
#  number FA8750-10-2-0245. The U.S. Government is authorized to
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

class  World (Agent):



    def __init__(self,r=1.0,s=1.0,v=1.0,cloudsize=1.0) :
	Agent.__init__(self,Agent.WORLD)
        self.time = 0
    
        self.N=5                   # %size of grid
        self.expenditure = 0.0     # cummulative funds expended since last reset
        self.numberVacuums = 0     # No vacuums assigned yet.
	self.vacuumArray = []      # array of object handles
        self.intializeVariables(r,s,v,cloudsize)

	self.setSensor(None)
	self.setPlanner(None)


    def setSensor(self,sensor) :
        self.sensor = sensor

    def getSensor(self) :
        return(self.sensor)

    def setPlanner(self,planner) :
        self.planner = planner

    def getPlanner(self) :
        return(self.planner)


    def quit(self) :
	from XML.XMLMessageExternalCommand import XMLMessageExternalCommand

	# Send a set of exit commands to the different agents. First
	# create the message itself.
	parameter = XMLMessageExternalCommand()
	parameter.setParameterValue(XMLMessageExternalCommand.EXIT)
	parameter.createRootNode()

	# Send the message to each agent.
	self.channel.sendString(Router.COMMANDER,parameter.xml2Char(False))
	self.channel.sendString(Router.PLANNER,parameter.xml2Char(False))
	self.channel.sendString(Router.SENSORARRAY,parameter.xml2Char(False))

	
	for definedVacuum in self.vacuumArray :
	    # Send the message to each vacuum
	    self.channel.sendString(Router.VACUUM,parameter.xml2Char(False),definedVacuum.getID())
	    definedVacuum.checkIncomingQueue()  # Make sure the vacuum processes its world queue.
	    
		    
        exit(0) # Say bye bye!

    
    def intializeVariables(self,r,s,v,cloudsize) :
        # initialize the variables this class keeps track of (input rate and size constants)
        self.time=0;                 # The initial time is zero.
	self.setDirtRate(r)          # rate constant for - events per unit time(world wide)
	self.setDirtSize(s)          # size constant for exponential distribution of sizes
	self.setRainRate(v)          # rate constant for RAIN events - events per unit
	                             # time (world wide)
	self.setRainSize(cloudsize)  # average size of rain event


	# Send all of these paramaters off to the agents
	if(self.channel) :
	    from XML.XMLMessageExternalParameter import XMLMessageExternalParameter
	    parameter = XMLMessageExternalParameter()
	    parameter.setParameterValue(XMLMessageExternalParameter.DUST_RATE,r)
	    parameter.setParameterValue(XMLMessageExternalParameter.RAIN_RATE,v)
	    parameter.setParameterValue(XMLMessageExternalParameter.DUST_SIZE,s)
	    parameter.setParameterValue(XMLMessageExternalParameter.RAIN_SIZE,cloudsize)
	    parameter.createRootNode()

	    self.channel.sendString(Router.SENSORARRAY,parameter.xml2Char(False))
	    self.channel.sendString(Router.PLANNER,parameter.xml2Char(False))
	    self.channel.sendString(Router.COMMANDER,parameter.xml2Char(False))

	

        self.A = zeros((self.N,self.N),dtype=float64)        # array of values for dirt levels
        self.Moisture = zeros((self.N,self.N),dtype=float64) # array of values for moisture level


    def setNumberVacuums(self,number) :
	# Routine to set the value that tracks the number of vacuums.
	self.numberVacuums = number


    def addVacuum(self,vacuum,debug=False) :
        # routine to add a vacuum to the list of vacuums tracked by
        # the world. This overrides the method of the same name in the
        # base class.

	if(debug) :
	    print("About to add a Vacuum: {0}".format(vacuum))
	    self.printVacuumInfo(0)


	for definedVacuum in self.vacuumArray :
	    # Check to see if this vacuum is already defined. We need
	    # to do this because the channel adds a vacuum to the
	    # world automatically. It is possible that the channel
	    # already added this vacuum.
	    if(vacuum == definedVacuum) :
		if(debug) :
		    print("Found this one...{0}".format(vacuum))
		return
	    
        self.vacuumArray.append(vacuum)
	self.setNumberVacuums(len(self.vacuumArray))
	if(debug) :
	    print("Adding Vacuum: {0}".format(vacuum))
	    self.printVacuumInfo(0)

    def deleteVacuum(self,vacuum):
        # routine to delete a vacuum from the list of vacuums tracked
        # by the world. This overrides the method of the same name in
        # the base class.
	for i in range(len(self.vacuumArray)):
	    # Loop through all the vacuums
	    if(self.vacuumArray[i]==vacuum):
		# This is the one to delete.
		self.vacuumArray.pop(i)
		self.setNumberVacuums(len(self.vacuumArray))
		return

    def getVacuums(self) :
        return(self.vacuumArray)


    def printVacuumInfo(self,time) :
	# Convencience routine for printing out the vacuum info - used
	# for debugging.
	j = 0
	for vacuum in self.vacuumArray:
	    print("{0} - {1} ({2})".format(j,vacuum,time))
	    j += 1
	print("\n\n")


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
	#print("Cleaning grid {0},{1}".format(x,y))
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


    def inc(self) :
        # Take a single time step of the simulated world

	# First check the queue for pending requests
	self.getChannel().getRouter().checkIncomingQueue()   # check to see if there is any
	                                                     # information that is waiting to
							     # process. This could be from the
							     # vacuums.
            
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
        self.sendWorldStatusToSensor(self.A)
        
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


	# Let the sensor know the current state of the world.
        self.sendWorldWetnessToSensor(self.Moisture)
        self.sendPlannerUpdateRequest()

	# Make sure that the vacuums update themselves.
        for vacuum in range(self.numberVacuums):
	    #print("World.inc: Sending to vacuum {0}".format(vacuum))
            self.sendVacuumWorldTime(T,vacuum,self.Moisture)


	# Check the message queue one last time just in case something
	# came in during the intermediate execution.
	self.getChannel().getRouter().checkIncomingQueue()
        self.time=T;



    # Method to handle an incoming message and determine what to do
    def handleMessage(self,type,passedInformation) :
	#print("World.handleMessage: {0} - {1}".format(type,passedInformation))

	if (type=="Add Expenditure") :
	    expenditure = int(passedInformation["expenditure"])
	    vacuumID    = int(passedInformation["vacuumID"])
	    self.addExpenditure(expenditure)

	elif (type=="Clean Grid") :
	    posX      = int(passedInformation["xPos"])
	    posY      = int(passedInformation["yPos"])
	    vacuumID  =  int(passedInformation["vacuumID"])
	    self.clean(posX,posY)




    ## sendWorldStatusToSensor
    #
    # Routine to send the world's status to a sensor.
    def sendWorldStatusToSensor(self,A) :
	#print("World.sendWorldStatusToSensor - sending information")
        worldData = XMLMessageForAgent()
        worldData.createRootNode(False)
	worldData.createObjectClassElements(Agent.SENSORARRAY,"World Status")
	worldData.addArrayNode(A)
	#print(self.xml2Char())

	self.channel.sendString(Router.SENSORARRAY,worldData.xml2Char(),-1)


    ## sendWorldWetnessToSensor
    #
    # Routine to send the world's wetness levels to a sensor.
    def sendWorldWetnessToSensor(self,Moisture):
	#print('World.sendWorldWetnessToSensor - sending information.')
	worldWetness = XMLMessageForAgent()
        worldWetness.createRootNode(False)
	worldWetness.createObjectClassElements(Agent.SENSORARRAY,"World Wetness")
	worldWetness.addArrayNode(Moisture)
	#print(self.xml2Char())


	self.channel.sendString(Router.SENSORARRAY,worldWetness.xml2Char())


    ## sendPlannerUpdateRequest
    #
    # Routine to send a request for an update to the planner. This
    # tells the planner that it needs to take whatever actions are
    # necessary during a world time step.
    def sendPlannerUpdateRequest(self) :
	#print("World.sendPlannerUpdateRequest - sending information.")
	report = XMLMessageForAgent()
	report.createRootNode(False)
	report.createObjectClassElements(Agent.PLANNER,"Update")
	#print(self.xml2Char())


	self.channel.sendString(Router.PLANNER,report.xml2Char()) #,-1,False,True)


    ## sendVacuumWorldTime
    #
    # Routine to send the current world time from the world to a
    # vacuum. This tells the vacuum that it needs to take whatever
    # actions are appropriate for a given time step.
    def sendVacuumWorldTime(self,T,id,wetness) :
	#print("World.sendVacuumWorldTime - sending information")
	newTime = XMLMessageForAgent()
        newTime.createRootNode(False)
	newTime.createObjectClassElements(Agent.VACUUM,"World Time")
	newTime.addArrayNode(wetness)
	newTime.vacuumID(id)
	newTime.addTime(T)
	#print(self.xml2Char())

	self.channel.sendString(Router.VACUUM,newTime.xml2Char(),id,False,False)


    # Routines that are overridden from the Agent class. These are
    # handlers for requests that come from an outside data source.


    # Routine to handle the poll requests
    def poll(self) :
	pass


    # Routine to handle the reset requests
    def reset(self) :
	pass


    # Routine to handle the reset requests
    def restart(self) :
	pass


    # Routine to handle the start requests
    def startSimulation(self) :
	pass


    # Routine to handle the stop requests
    def stopSimulation(self) :
	pass



    # Routine to perform a number of time steps of the simulation. It
    # assumes that all of the parameters are set and proceeds with the
    # time steps.
    def stepInTime(self,numSteps,start=0,skip=1):
    
	for i in range(numSteps) :
	    import time      # DEBUG
	    time.sleep(0.06) # DEBUG

	    if(self.getDataCollection()) :
		if(i%self.dataSkip == 0) :
		    # We need to collect data on this time step.
		    pass
		
	    self.inc()
	    if((skip>0) and (i%skip==0)) :
		print(i)



    # Static method that is used as a helper to make it easier to
    # create a world object.
    @staticmethod
    def spawnWorld(r=1.0,s=1.0,v=1.0,cloudsize=1.0) :
	world = World(r,s,v,cloudsize)
	channel = world.initializeChannel()
	return(world)

            
            
if (__name__ =='__main__') :
    from Vacuum import Vacuum

    
    # Set the host addresses and ports for the different agents
    agentInterfaces = {Router.SENSORARRAY:['10.0.1.10',10000],
		       Router.PLANNER    :['10.0.1.11',10001],
		       Router.COMMANDER  :['10.0.1.12',10002],
		       Router.WORLD      :['10.0.1.13',10003]}

    # Set the host addresses and ports for the different vacuums 
    vacummInterfaces = [ ['10.0.1.14',10004],
			 ['10.0.1.15',10005],
			 ['10.0.1.16',10006]]

    # Set the other mission parameters
    numVacs=len(vacummInterfaces)

    # Set the parameters associated with the world.
    # Set the rate and size for dirtfall
    r = 1.8
    s = 12.0

    # Set the rate constant and size for rain
    v         = .2
    cloudsize = 20


    # Create the world and get the gridsize
    W = World.spawnWorld(r,s,v,cloudsize);
    #print("World channel: {0}".format(W.getChannel()))
    N = W.getNumber()
    chan = W.getChannel()                     # Get the world's channel object
    chan.setNumberVacuums(numVacs)            # Let the world's channel know how many vac's to use
    W.setIPInformation(agentInterfaces)       # Let the world know all the ip info about the agents.




    # Create vacuums
    vacArray = []
    for i in range(numVacs) :
	vacuum = Vacuum.spawnVacuum(i,0)
	#print("New Vacuum: {0} - {1}, {2}".format(vacuum,id(vacuum),i))
	vacuum.getChannel().setNumberVacuums(numVacs)      # Tell the vacuum how many other
							   # vacuums there will be
	vacuum.setQueueUse(True)                           # Tell the vacuum to get info
							   # from the world through the queue.
	vacArray.append(vacuum)                            # Append this to the vac's kept track of here.
	pos = vacuum.getPosition()                         # get the default pos.
	chan.getRouter().addVacuum(vacuum.getChannel(),i)  # Tell the world where the vacuum starts.

	W.addVacuum(vacuum,False)                          # Add the vacuum to the world's list of vac's


	chan.addVacuum(vacuum,i,pos[0],pos[1],False)       # Let the world's channel know about this vac

	# Let this vacuum know about the ip information about all of the other agents and the world.
	vacuum.setIPInformation(agentInterfaces)
	vacuum.setRouterChannel(Router.WORLD,W.getChannel())


	# Set the ip information for this particular vacuum.
	#print("Setting vacuum {0} - {1}:{2}".format(i,vacummInterfaces[i][0],vacummInterfaces[i][1]))
	vacuum.setHostname(vacummInterfaces[i][0])
	vacuum.setPort(vacummInterfaces[i][1])

	# If you want the vacuum to run in its own process then uncomment out the next line (.start)
	#vacuum.start()

	# If you want the vacuum to run in this process with a direct
	# connection to the world then uncomment out the next line.
	vacuum.getChannel().getRouter().createAndInitializeSocket()



    # Set the ip info for the world and start up the graphical interface
    W.setHostname(agentInterfaces[Router.WORLD][0])
    W.setPort(agentInterfaces[Router.WORLD][1])
    W.getChannel().getRouter().createAndInitializeSocket()


    from XML.XMLMessageExternalCommand import XMLMessageExternalCommand
    parameter = XMLMessageExternalCommand()
    parameter.setParameterValue(XMLMessageExternalCommand.RESTART)
    parameter.createRootNode()
    for vacuum in vacArray:
	# Turn on each of the vacuums - i.e. reset the vacuum.
	# print("GraphicalWorld.start - Vacuum: {0}".format(vacuum))
	#vacuum.setWorking(True)
	#vacuum.setStatus(3)
	#vacuum.initializeTime(0.0)
	W.channel.getRouter().sendString(
	    Router.VACUUM,parameter.xml2Char(False),vacuum.getID())

    H = []
    R = []
    skip = 10;
    numSteps = 20
    for i in range(numSteps) :
	#import time # DEBUG
	#time.sleep(1) # DEBUG
	W.inc()
	#if(i%skip==0) :
	print(i)



    W.quit()
    
