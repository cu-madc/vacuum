#!/usr/bin/python
#
#  Agent.py
# 
#   Created on: 15 June, 2011
#       Author: Kelly Black
# 
#       class definition for the base object used by all of the agents.
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

from multiprocessing import Process, Queue
from Router import Router


class Agent (Process):

    COMMANDER, \
	       PLANNER, \
	       SENSORARRAY, \
	       VACUUM, \
	       WORLD, \
	       DATACOLLECTOR = range(6)

    EXTERNAL = "ext"

    DEBUG = False

    def __init__(self,type) :
	# Define the other objects that need to be tracked.
	Process.__init__(self)
        self.setChannel(None)
	self.setMyType(type)
	self.queue = Queue()
	self.queueUse = False

	# Initialize the data collection.
	self.worldDataFile = None
	self.vacuumDataFile = None
	self.setWorldFileName("")
	self.setVacuumFileName("")

	self.setDataCollection()
	self.setDataCollectionFrequency()



	self.setWorking(True)

    def __del__(self) :
	if(Agent.DEBUG):
	    print("Agent.__del__: {0}".format(self.getMyType()))


    # This is for setting/getting the channel used by this agent.
    def setChannel(self,value) :
        self.channel = value

    def getChannel(self) :
        return(self.channel)


    def setReliability(self,value) :
        self.channel.setReliability(value)

    def getReliability(self) :
        return(self.channel.getReliability())


    # This is for setting/getting the type of agent this is. The types
    # are kept track of in the Router class.
    def setMyType(self,type) :
	self.myType = type

    def getMyType(self) :
	return(self.myType)

    # This is for setting/getting the thread safe queue used for
    # exchanging information to/from the world.
    def setQueueUse(self,value) :
	self.queueUse = value

    def getQueueUse(self) :
	return(queueUse)


    # This is used to set/get whether or not this agent is working.
    def setWorking(self,value) :
        self.isWorking = value

    def getWorking(self) :
        return(self.isWorking)

    # Used for the output of data
    def setWorldFileName(self,name) :
    	self.worldFileName  = name
	
	if(self.worldDataFile) :
	    self.worldDataFile.close()
	    self.worldDataFile = None

    # Get the file name
    def getWorldFileName(self):
	return(self.worldFileName);

    # open the file object
    def openWorldDataFile(self,mode) :
	if(self.worldDataFile) :
	    self.worldDataFile.close()

	try:
	    self.worldDataFile  = open(self.worldFileName,mode)
	except IOError:
	    self.worldDataFile = None
	    print("Could not open up file: {0}".format(self.worldFileName))
	    
	#self.worldDataFile.close()

    def setVacuumFileName(self,name) :
	self.vacuumFileName = name

	if(self.vacuumDataFile) :
	    self.vacuumDataFile.close()
	    self.vacuumDataFile = None

    def getVacuumFileName(self):
	return(self.vacuumFileName)

    # Open the vacuum file
    def openVacuumDataFile(self,mode) :
	if(self.vacuumDataFile) :
	    self.vacuumDataFile.close()

	try:
	    self.vacuumDataFile = open(self.vacuumFileName,mode)
	except IOError:
	    self.vacuumDataFile = None
	    print("Could not open up file: {0}".format(self.vacuumFileName))

	#self.vacuumDataFile.close()


    def setDataCollection(self,value=False) :
	self.collectData = value

    def getDataCollection(self) :
	return(self.collectData)

    def setDataCollectionFrequency(self,skip=1) :
	# Set which time steps should be used to collect data. If
	# skip=1 then data is collected at every time step. If skip=2
	# then every other step is used.
	if(skip > 0) :
	    self.dataSkip = skip

	else:
	    self.dataSkip = 1


    # call this routine when you want to poll the hostname/socket
    # assigned to this agent. This is called when the start method is
    # called and will spawn a new agent. It should not be called
    # directly.
    def run(self) :

	#if(self.getDataCollection()) :
	#    print("Data collection is on!")
	#    
	#    if(self.getWorldFileName()) :
	#	print("opening the world data file: {0}".format(self.getWorldFileName()))
	#	self.openWorldDataFile("a")

        #   if(self.getVacuumFileName()) :
	#	print("opening the vacuum data file: {0}".format(self.getVacuumFileName()))
	#	self.openVacuumDataFile("a")
		
	self.channel.getRouter().createAndInitializeSocketForever()


    # For specifying the hostname/port number used by this agent. 
    def setHostname(self,hostname) :
	#print("Setting agent hostname: {0}".format(hostname))
        self.channel.getRouter().setHostname(hostname)

    def setPort(self,port) :
	#print("Setting agent port number: {0}".format(port))
        self.channel.getRouter().setPort(port)


    # This is for setting the host information for other agents.
    def setHostInformation(self,hostType,host,port,vacuumID=None) :

	if(self.channel and self.channel.getRouter()) :
	    self.channel.getRouter().setHostInformation(hostType,host,port,vacuumID)

    # This is for setting the channel information for other agents.
    def setRouterChannel(self,type,channel) :

	if(self.channel and self.channel.getRouter()) :
	    self.channel.getRouter().setChannel(type,channel)


    # This is for setting the channel information for a vacuum.
    def setVacuumRouterInformation(self,channel,vacuumID=None,xPos=0,yPos=0) :

	if(self.channel) :
	    if(Agent.DEBUG):
		print("Adding vacuum: {0} - {1}".format(channel,vacuumID))
            self.channel.addVacuum(channel,vacuumID,xPos,yPos)
            self.channel.getRouter().addVacuum(channel,vacuumID)


    # This is used for printing out debug information about the router.
    def printRouterInformation(self,toPrint) :
        if(self.channel) :
            self.channel.getRouter().printHostInformation(toPrint)


    # Helper routine to create a channel and assign it to this
    # agent. Used for creating a new agent.
    def initializeChannel(self):
	from Channel import Channel
	channel = Channel()
	self.setChannel(channel)
	channel.addAgent(self,self.getMyType(),0,False)
	return(channel)



    # This is for setting the tcp information for a dictionary of
    # objects. this way the ip information can be set in one
    # dictionary and changed all at one time.
    def setIPInformation(self,interfaces) :

	for agentType, ipInfo in interfaces.iteritems():

	    if(agentType == Router.VACUUM) :
		# This is a list of ip info for each vacuum
		id = 0
		for row in ipInfo :
		    #print("Setting vaccum information {0}: {1}:{2}".format(
                    #      id,row[0],row[1]))
		    self.setHostInformation(Router.VACUUM,row[0],row[1],id)
		    id += 1

	    else :
		#print("setting ip information for object {0} with info {1}".format(
		#    agentType,ipInfo))
		self.setHostInformation(agentType,ipInfo[0],ipInfo[1],None)

    # Tell the router to shut down its socket.
    def shutdownServer(self) :
	if(self.channel and self.channel.getRouter()) :
	    #print("Agent.shutdownServer - shutting down server: {0}".format(self.getMyType()))
	    self.channel.getRouter().stopServerSocket(self.getMyType())


    # Tell the channel to check its queue for commands that have come
    # in from another agent or the world.
    def checkIncomingQueue(self,debug=False) :
	self.getChannel().getRouter().checkIncomingQueue(debug)


    # Routines that are expected to be overridden in their respective
    # super classes. These are handlers for requests that come from an
    # outside data source.

    # Routine to deal with incoming poll data
    def pollData(self,data):
	pass

    # Routine to handle the poll requests
    def poll(self,dest=None,info=None,label=None) :
	if(dest and info and label) :

	    from XML.XMLMessageForAgent import XMLMessageForAgent
	    localData = XMLMessageForAgent()
	    localData.createRootNode(False)
	    localData.createObjectClassElements(Agent.DATACOLLECTOR,label)
	    localData.addData(info)

	    #if(label=="vacuum data") :
	    #     print(localData.xml2Char())
	    #      self.channel.sendString(dest,localData.xml2Char(),-1,False,True)

	    #else :
	    self.channel.sendString(dest,localData.xml2Char(),-1,False,False)

	    #self.channel.sendInfoViaCallback(dest,info)



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
