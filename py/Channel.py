#!/usr/bin/python
#
#  Channel.py
# 
#   Created on: 2 Feb, 2011
#       Author: Skufka - adapted by black - adapted by PW
# 
#       class definition for the channel object not using sockets
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
#  ==========================================================================# 
# 
#  Helpful References:
#    http://docs.python.org/library/socketserver.html
# 
#

from numpy import *
from numpy.linalg import *

#from World import World
#from Vacuum import Vacuum

from Router import Router
from SocketRouter import SocketRouter

from Agent import Agent


# The xml classes used to define the messages being passed.
from XML.XMLParser import XMLParser
from XML.XMLIncomingDIF import XMLIncomingDIF
from XML.XMLMessageForAgent import XMLMessageForAgent
#from XML.XMLMessageNetwork import XMLMessageNetwork


from XML.XMLMessageExternalCommand import \
     XMLMessageExternalCommand     

from XML.XMLMessageExternalParameter import \
     XMLMessageExternalParameter


## Channel
#
# Creates a channel, which is a medium through which simulated agents communicate.
#
# This channel uses local function calls, not sockets, for communication.
class Channel:

    checkInfoType = False
    DEBUG = False
    
    
    def __init__(self) :

        self.setWorking(True)        
        self.delay = 0.0           # transmission delay - not yet implemented

	self.myAgents = []
        self.vacuumArray = [] # array of object handles
	
	self.router = SocketRouter(self)



    # Utility routines.
    #
    # These methods are used for setting the values of certain
    # parameters and is primarily used for outside objects when it is
    # necessary to make a change to a Channel object.
    
    def setWorking(self,value) :
        self.isWorking = value

    def getWorking(self) :
        return(self.isWorking)

    def getRouter(self) :
	return(self.router)

    def setDebug(self,value) :
	Channel.DEBUG = value
	self.router.setDebug(value)

    def getDebug(self) :
	return(Channel.DEBUG)

    def setRouterChannel(self,type,channel) :
	self.router.setChannel(type,channel)

    def printChannelInformation(self,toPrint) :
        print("Channel information {0}: {1} - {2}".format(toPrint,self,self.vacuumArray))


    def sendString(self,type,message,id=-1,debug=False) :
	if(self.router) :
	    self.router.sendString(type,message,id,debug)

    def addVacuum(self,vacuum,id,xpos,ypos,debug=False) :

	if(vacuum != None):
	    for definedVacuum in self.vacuumArray :
		# Check to see if this vacuum is already defined. We can
		# get into this routine from a variety of places. It might
		# be possible to have already called this routine.
		if(vacuum == definedVacuum) :
		    if(debug):
			print("Channel.addVacuum, Found this one...")
		    return

        while(id>=len(self.vacuumArray)) :
            # There are not enough vacuum objects defined. Create
            # place holders.
            self.vacuumArray.append(None)

        self.vacuumArray[id] = vacuum
        #self.sendPlannerVacuumMovedPosition(id,xpos,ypos) #TODO - should this be commented out?
	if(debug):
	    print("Channel.addVacuum - vacuum array: {0}".format(self.vacuumArray))

	if (vacuum and 
	    ((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0])) :
	    #print("Shutting down the world")
	    self.myAgents[Agent.WORLD][0].addVacuum(vacuum,debug)


    def setNumberVacuums(self,number,x=0,y=0) :
	
	self.router.setNumberVacuums(number) # set the number of vacuums for the router.
	#print("Channel.setNumbervacuums: {0} - {1}, {2}".format(len(self.vacuumArray),self.vacuumArray,self))
	
	# Routine to set the number of vacuums that are being tracked.
	if(number > len(self.vacuumArray)) :
	    # There are more vacuums to be used than currently
	    # defined. Add the extras to the list.
	    for i in range(number-len(self.vacuumArray)):
		#vacuum = Vacuum(len(self.vacuumArray))
		self.addVacuum(None,len(self.vacuumArray),x,y)

	elif (number < len(self.vacuumArray)) :
	    # Need to have fewer vacuums than what are currently
	    # defined. Delete the extras.
	    while(len(self.vacuumArray)>number) :
		vacuum = self.vacuumArray.pop()
		
		if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
		    self.myAgents[Agent.WORLD][0].deleteVacuum(vacuum)
		    



    def addAgent(self,agent,type,id,debug=False) :

	#if(debug):
	#    print("\n\nChannel.addAgent - request to agent: {0},{1}\n{3}-{2}".format(
	#	type,id,self.myAgents,agent))


	if(agent != None):
	    for agentList in self.myAgents :
		# Check to see if this agent is already defined. We can
		# get into this routine from a variety of places. It might
		# be possible to have already called this routine.
		if(agent in agentList) :
		    if(debug):
			print("Channel.addAgent - This agent is already defined {1},{2}".format(type,id))
		    return

        while(type >= len(self.myAgents)) :
            # There are not enough agent objects defined. Create
            # place holders as empty lists.
            self.myAgents.append([None])


        while(id >= len(self.myAgents[type])) :
            # There are not enough agents of this type  defined. Create
            # place holders.
            self.myAgents[type].append(None)

	# All the spaces are allocated. Go ahead and specify this agent.
        self.myAgents[type][id] = agent

	if(debug):
	    print("Channel.addAgent - Added agent: {0},{1}\n{2}".format(
		type,id,self.myAgents))




    ## receiveXMLReportParseAndDecide
    #
    # This is a generic routine. It receives an xml report and decides
    # what it is and who it is for. It then calls the specific routine
    # necessary to pass along the information.
    def receiveXMLReportParseAndDecide(self,xmlString) :
        dif = XMLIncomingDIF()
        info = dif.determineXMLInformation(xmlString)

	
	if(Channel.checkInfoType) :
	    if(info) :
		print("Got information: {0}".format(info.getMyInformationType()))
	    else:
		print("No object returned from the parsing routine.")
	    Channel.checkInfoType = False

	try:
	    if(info) :
		theType = info.getMyInformationType()
	    else :
		theType = -1

	except AttributeError:
	    print("Error - the XML information is not valid.")
	    return

	name = dif.getName()



	if(name == Agent.COMMANDER) :
	    #print("this is a message for the commander: {0}\n{1}".format(
	    #    dif.getType(),dif.getPassedInformation()))

	    if((len(self.myAgents)>=name) and self.myAgents[name][0]) :
	       self.myAgents[name][0].handleMessage(dif.getType(),dif.getPassedInformation())




	elif (name == Agent.WORLD) :
	    #print("this is a message for the world: {0}\n{1}".format(
	    #    dif.getType(),dif.getPassedInformation()))

	    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
		self.myAgents[Agent.WORLD][0].handleMessage(dif.getType(),
							    dif.getPassedInformation())



	elif (name == Agent.VACUUM) :
	    #print("this is a message for the vacuum: {0}\n{1}".format(
	    #    dif.getType(),dif.getPassedInformation()))

	    if((len(self.myAgents)>Agent.VACUUM) and self.myAgents[Agent.VACUUM][0]) :
		self.myAgents[Agent.VACUUM][0].handleMessage(dif.getType(),
							    dif.getPassedInformation())
		



	if (name == Agent.PLANNER) :
	    #print("this is a message for the planner: {0}\n{1}".format(
	    #    dif.getType(),dif.getPassedInformation()))

	    if((len(self.myAgents)>Agent.PLANNER) and self.myAgents[Agent.PLANNER][0]) :
		self.myAgents[Agent.PLANNER][0].handleMessage(dif.getType(),
							      dif.getPassedInformation())



	if (name == Agent.SENSORARRAY) :
	    #print("this is a message for the sensor: {0}\n{1}".format(
	    #    dif.getType(),dif.getPassedInformation()))

	    if((len(self.myAgents)>=name) and self.myAgents[name][0]) :
		self.myAgents[name][0].handleMessage(dif.getType(),dif.getPassedInformation())



	elif(theType == XMLParser.MESSAGE_EXTERNAL_PARAMETER) :
	    # This is a message from the outside with information
	    # about a parameter to set.
	    # print("External message")
	    host = ''
	    port = -1
	    hostType = -1
	    vacuumID = -1
	
	    for item in info.parameterList:

		if(item[0] == XMLMessageExternalParameter.DUST_RATE) :
		    #print("dust rate: {0}".format(item[1]))

		    if((len(self.myAgents)>Agent.PLANNER) and self.myAgents[Agent.PLANNER][0]) :
			#print("send planner dirt rate")
			self.myAgents[Agent.PLANNER][0].setUnnormalizedDirtRate(float(item[1]))


		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			self.myAgents[Agent.WORLD][0].setDirtRate(float(item[1]))

		    #print("this is a message for external data: *{0}*\n{1}".format(
			#dif.getType(),dif.getPassedInformation()))

		    
		elif(item[0] == XMLMessageExternalParameter.DUST_SIZE) :

		    if((len(self.myAgents)>Agent.PLANNER) and self.myAgents[Agent.PLANNER][0]) :
			#print("send planner dirt size")
			self.myAgents[Agent.PLANNER][0].setUnnormalizedDirtSize(float(item[1]))


		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			self.myAgents[Agent.WORLD][0].setDirtSize(float(item[1]))

		    
		elif(item[0] == XMLMessageExternalParameter.RAIN_RATE):

		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			self.myAgents[Agent.WORLD][0].setRainRate(float(item[1]))

			
		elif(item[0] == XMLMessageExternalParameter.RAIN_SIZE):

		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			self.myAgents[Agent.WORLD][0].setRainSize(float(item[1]))

		    
		elif(item[0] == XMLMessageExternalParameter.GRID_SIZE):
		    
		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			self.myAgents[Agent.WORLD][0].setGridSize(int(item[1]))

		    if(len(self.myAgents)>Agent.SENSORARRAY):
			if (self.myAgents[Agent.SENSORARRAY][0]) :

			    #print("Channel.receiveXMLReportParseAndDecide - XMLParser.GRID_SIZE")
			    self.myAgents[Agent.SENSORARRAY][0].setGridSize(int(item[1]))


		    if((len(self.myAgents)>Agent.PLANNER) and self.myAgents[Agent.PLANNER][0]) :
			#print("send planner grid size")
			self.myAgents[Agent.PLANNER][0].setGridSize(int(item[1]))
		    
		elif(item[0] == XMLMessageExternalParameter.NUMBER_OF_VACUUMS):
		    #print("number vacs: {0}".format(int(item[1])))
		    self.setNumberVacuums(int(item[1]))

		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			self.myAgents[Agent.WORLD][0].setNumberVacuums(int(item[1]))


		elif(item[0] == XMLMessageExternalParameter.HOST_ADDRESS):
		    #print("set host: {0}".format(item[1]))
		    #self.router.setHost(item[1])
		    host = item[1]


		elif(item[0] == XMLMessageExternalParameter.HOST_PORT):
		    #print("set port: {0}".format(item[1]))
		    #self.router.setPort(item[1])
		    port = int(item[1])

		elif(item[0] == XMLMessageExternalParameter.HOST_TYPE) :
		    #print("host type: {0}".format(item[1]))
		    hostType = int(item[1])

		elif(item[0] == XMLMessageExternalParameter.VACUUM_ID) :
		    #print("vacuum id: {0}".format(item[1]))
		    vacuumID = int(item[1])



	    if(host or (port>-1) or (hostType>-1) or (vacuumID>-1)):
		# information was passed that provides information
		# about the setup of the simulation.

		if(host and (port>-1) and (hostType>-1)):
		    # There is enough information to define another
		    # agent in the system. If it is a vacuum, though
		    # we will need the vacuum id which has to be
		    # checked.

		    if(hostType == Router.VACUUM) :
			if(vacuumID>-1):
			    #print("Set up vacuum's host information: {0} - {1} - {2} - {3}".format(hostType,host,port,vacuumID))
			    self.router.setHostInformation(hostType,host,port,vacuumID)

			#else :
			#    print("Error - Badly formed message came in. Message with vacuum information did not include a vacuum id.")

		    else:
			# This is information for an agent that is not
			# a vacuum.
			#print("Set up agent's host information: {0} - {1} - {2} - {3}".format(hostType,host,port,vacuumID))
			self.router.setHostInformation(hostType,host,port,vacuumID)


		else:
		    # If you get down here then incomplete information
		    # was given. Assume that the file had details
		    # about this particular agent.

		    if(host) :
			self.router.setHost(host)

		    if(port > -1) :
			self.router.setPort(port)

		    #if(hostType > -1) :
		    #     print("Error - badly formed message came in. The host type was specified but the other required information was incomplete.")

		    

	elif(theType == XMLParser.MESSAGE_EXTERNAL_COMMAND) :
	    # This is a message from the outside with information
	    # about a command request
	    #print("External Command")
	    for item in info.parameterList:

		if(item == XMLMessageExternalCommand.STOP) :
		    print("stop: {0}".format(item))

		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			pass

		elif(item == XMLMessageExternalCommand.START) :
		    print("start: {0}".format(item))

		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			pass

		elif(item == XMLMessageExternalCommand.RESTART) :
		    #print("restart: {0}".format(item))

		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			pass


		    if(len(self.myAgents)>Agent.SENSORARRAY):
			if (self.myAgents[Agent.SENSORARRAY][0]) :
                            #self.myAgents[Agent.SENSORARRAY][0].shutdownServer()
			    pass


		    if((len(self.myAgents)>Agent.PLANNER) and self.myAgents[Agent.PLANNER][0]) :
			#self.myAgents[Agent.PLANNER][0].shutdownServer()
			pass

		    if(len(self.myAgents)>Agent.COMMANDER) :
			if (self.myAgents[Agent.COMMANDER][0]) :
			    #self.myAgents[Agent.COMMANDER][0].shutdownServer()
			    pass
			    

		    if((len(self.myAgents)>Agent.VACUUM) and self.myAgents[Agent.VACUUM][0]) :
			#self.myAgents[Agent.VACUUM][0].shutdownServer()
			self.myAgents[Agent.VACUUM][0].setWorking(True)
			self.myAgents[Agent.VACUUM][0].setStatus(3)
			self.myAgents[Agent.VACUUM][0].initializeTime(0.0)


		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			#self.myAgents[Agent.WORLD][0].shutdownServer()
			pass



		elif(item == XMLMessageExternalCommand.RESET) :
		    print("reset: {0}".format(item))

		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			pass

		elif(item == XMLMessageExternalCommand.POLL) :
		    print("poll: {0}".format(item))

		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			pass

		elif(item == XMLMessageExternalCommand.EXIT) :
		    #print("exit: {0}".format(item))

		    if(len(self.myAgents)>Agent.SENSORARRAY):
			if (self.myAgents[Agent.SENSORARRAY][0]) :
			     #print("Shutting down the server")
			     self.myAgents[Agent.SENSORARRAY][0].shutdownServer()


		    if((len(self.myAgents)>Agent.PLANNER) and self.myAgents[Agent.PLANNER][0]) :
			#print("Shutting down the planner")
			self.myAgents[Agent.PLANNER][0].shutdownServer()

		    if(len(self.myAgents)>Agent.COMMANDER):
			if (self.myAgents[Agent.COMMANDER][0]) :
		              #print("Shutting down the commander")
			      self.myAgents[Agent.COMMANDER][0].shutdownServer()


		    if((len(self.myAgents)>Agent.VACUUM) and self.myAgents[Agent.VACUUM][0]) :
			#print("Shutting down the vacuum")
			self.myAgents[Agent.VACUUM][0].shutdownServer()


		    if((len(self.myAgents)>Agent.WORLD) and self.myAgents[Agent.WORLD][0]) :
			#print("Shutting down the world")
			self.myAgents[Agent.WORLD][0].shutdownServer()


    ## sendVacuumReportFromCommander2Planner
    #
    # Routine that takes a report from the commander that identifies a
    # particular vacuum and converts it into XML and passes it along
    # to the planner so it will know where the vacuum was sent.
    #
    def sendVacuumReportFromCommander2Planner(self,xPos,yPos,IDnum) :

        network = XMLMessageForAgent()
	network.VacuumReportFromCommander2Planner(xPos,yPos,IDnum)
	self.sendString(Router.PLANNER,network.xml2Char())
	#self.receiveXMLReportParseAndDecide(network.xml2Char())




    ## sendRecommendOrderFromCommander2Planner
    #
    # Routine that takes a recommendation order from the commander
    # that identifies a particular vacuum and converts it into XML and
    # passes the XML tree on to the planner.
    def sendRecommendOrderFromCommander2Planner(self,vacuumID,xPos,yPos) :            
	orders = XMLMessageForAgent()
	orders.RecommendOrderFromCommander2Planner(vacuumID,xPos,yPos)
	self.sendString(Router.PLANNER,orders.xml2Char())
	#self.receiveXMLReportParseAndDecide(orders.xml2Char())
            


    ## sendRecommendOrderFromPlanner2Commander
    #
    # Routine that takes a recomendation order from the planner that
    # identifies a particular vacuum and converts it into XML and
    # passes the XML tree on to the commander.
    def sendRecommendOrderFromPlanner2Commander(self,xPos,yPos,IDnum) :
	orders = XMLMessageForAgent()
	orders.RecommendOrderFromPlanner2Commander(xPos,yPos,IDnum)
	self.sendString(Router.COMMANDER,orders.xml2Char())
	#self.receiveXMLReportParseAndDecide(orders.xml2Char())




    ## sendMoveOrderFromCommander2Vacuum
    #
    # Routine that takes an order from the commander and converts it
    # into XML and passed the XML to the vacuum.
    def sendMoveOrderFromCommander2Vacuum(self,xPos,yPos,vacuumID) :
	orders = XMLMessageForAgent()
	orders.MoveOrderFromCommander2Vacuum(xPos,yPos,vacuumID)        
	self.sendString(Router.VACUUM,orders.xml2Char(),vacuumID)
	#self.receiveXMLReportParseAndDecide(orders.xml2Char())




    ## sendReportFromVacuum2Commander
    #
    # Routine to take a message from the vacuum that is a report for
    # the commander. This routine relays that report to the commander.
    def sendReportFromVacuum2Commander(self,xPos,yPos,status,IDnum) :
	#Channel.checkInfoType = True
	#print("sending vacuum to commander")
	report = XMLMessageForAgent()
	report.ReportFromVacuum2Commander(xPos,yPos,status,IDnum)
	self.sendString(Router.COMMANDER,report.xml2Char(),-1,False)
	#self.receiveXMLReportParseAndDecide(report.xml2Char())



    ## sendMoveOrderFromCommander2Planner
    #
    # Routine to take a message from the commander that is an order to
    # move a vacuum and relay it to the planner.
    def sendMoveOrderFromCommander2Planner(self,xPos,yPos,IDnum) :
	report = XMLMessageForAgent()
	report.MoveOrderFromCommander2Planner(xPos,yPos,IDnum)
	self.sendString(Router.PLANNER,report.xml2Char(),IDnum)



    ## sendMeasuredFromPlanner2Sensor
    #
    # Routine to take a request from the planner to get information
    # from the sensor and send it to the sensor.
    def sendMeasuredFromPlanner2Sensor(self) :
	report = XMLMessageForAgent()
	report.MeasuredFromPlanner2Sensor()
	self.sendString(Router.SENSORARRAY,report.xml2Char()) #,-1,True)
	#self.receiveXMLReportParseAndDecide(sensorData.xml2Char())


    ## sendStatusSensor2Planner
    #
    # Routine to send a noisy view of the world's grids to the planner
    # from the sensor.
    def sendStatusSensor2Planner(self,noisyView) :
        sensorData = XMLMessageForAgent()
        sensorData.StatusSensor2Planner(noisyView)
	self.sendString(Router.PLANNER,sensorData.xml2Char()) #,-1,True)
	#self.receiveXMLReportParseAndDecide(sensorData.xml2Char())


    ## sendWorldStatusToSensor
    #
    # Routine to send the world's status to a sensor.
    def sendWorldStatusToSensor(self,A) :
        worldData = XMLMessageForAgent()
	worldData.sendWorldStatusToSensor(A)
	self.sendString(Router.SENSORARRAY,worldData.xml2Char(),-1)
	#self.receiveXMLReportParseAndDecide(worldData.xml2Char())



    ## sendWorldWetnessToSensor
    #
    # Routine to send the world's wetness levels to a sensor.
    def sendWorldWetnessToSensor(self,Moisture):
	worldWetness = XMLMessageForAgent()
	worldWetness.WorldWetnessToSensor(Moisture)
	self.sendString(Router.SENSORARRAY,worldWetness.xml2Char())
	#self.receiveXMLReportParseAndDecide(worldWetness.xml2Char())



    ## sendPlannerUpdateRequest
    #
    # Routine to send a request for an update to the planner. This
    # tells the planner that it needs to take whatever actions are
    # necessary during a world time step.
    def sendPlannerUpdateRequest(self) :
	report = XMLMessageForAgent()
	report.PlannerUpdateRequest()
	self.sendString(Router.PLANNER,report.xml2Char()) #,-1,True)
	#self.receiveXMLReportParseAndDecide(update.xml2Char())


    ## sendPlannerVacuumMovedPosition
    #
    # Routine to send the new position of a vacuum. This comes from a
    # vacuum and is sent to a planner.
    def sendPlannerVacuumMovedPosition(self,idnum,xpos,ypos) :
        #update = XMLMessageVaccumMovedReportToPlanner()
        update = XMLMessageForAgent()
        update.PlannerVacuumMovedPosition(idnum,xpos,ypos)
	self.sendString(Router.PLANNER,update.xml2Char())
	#self.receiveXMLReportParseAndDecide(update.xml2Char())


    ## sendVacuumWorldTime
    #
    # Routine to send the current world time from the world to a
    # vacuum. This tells the vacuum that it needs to take whatever
    # actions are appropriate for a given time step.
    def sendVacuumWorldTime(self,T,id,wetness) :
	newTime = XMLMessageForAgent()
	newTime.sendVacuumWorldTime(T,id,wetness)
	self.sendString(Router.VACUUM,newTime.xml2Char(),id,False)
	#self.receiveXMLReportParseAndDecide(newTime.xml2Char())


    ## sendVacuumWorldExpenditure
    #
    # Routine to send an expenditure from a vacuum to the world. 
    def sendVacuumWorldExpenditure(self,expenditure,id) :
	newExpenditure = XMLMessageForAgent()
	newExpenditure.VacuumWorldExpenditure(expenditure,id)
	self.sendString(Router.WORLD,newExpenditure.xml2Char(),id)
	#self.receiveXMLReportParseAndDecide(newExpenditure.xml2Char())


    ## sendWorldCleanedGrid
    #
    # Routine to let a vacuum send an update to the world to let it
    # know that a grid area has been cleaned.
    def sendWorldCleanedGrid(self,idnum,xpos,ypos) :
	update = XMLMessageForAgent()
	update.WorldCleanedGrid(idnum,xpos,ypos)
	self.sendString(Router.WORLD,update.xml2Char(),idnum)
	#self.receiveXMLReportParseAndDecide(update.xml2Char())



if (__name__ =='__main__') :
    from XML.XMLMessageExternalCommand import XMLMessageExternalCommand
    import sys
    #parameter = XMLMessageExternalCommand()
    #parameter.setParameterValue(XMLMessageExternalCommand.STOP)
    #parameter.setParameterValue(XMLMessageExternalCommand.START)
    #parameter.setParameterValue(XMLMessageExternalCommand.RESTART)
    #parameter.setParameterValue(XMLMessageExternalCommand.RESET)
    #parameter.setParameterValue(XMLMessageExternalCommand.POLL)
    #parameter.createRootNode()
    #print(parameter.xml2Char(True))

    channel = Channel()
    from Agent import Agent
    channel.addAgent(Agent(Agent.COMMANDER),0,1,True)
    channel.addAgent(Agent(Agent.SENSORARRAY),2,4,True)
    sys.exit()

    channel = Channel()
    channel.getRouter().setNumberVacuums(7)
    #channel.receiveXMLReportParseAndDecide(parameter.xml2Char(False))
    #sys.exit(0)
    
    
    from XML.XMLMessageExternalParameter import XMLMessageExternalParameter
    from XML.XMLIncomingDIF import XMLIncomingDIF
    parameter = XMLMessageExternalParameter()
    parameter.setParameterValue(XMLMessageExternalParameter.DUST_RATE,0.2)
    parameter.setParameterValue(XMLMessageExternalParameter.RAIN_RATE,0.4)
    parameter.setParameterValue(XMLMessageExternalParameter.GRID_SIZE,5)
    parameter.setParameterValue(XMLMessageExternalParameter.DUST_SIZE,0.3)
    parameter.setParameterValue(XMLMessageExternalParameter.RAIN_SIZE,2.0)
    parameter.setParameterValue(XMLMessageExternalParameter.GRID_SIZE,6)
    #parameter.setParameterValue(XMLMessageExternalParameter.NUMBER_OF_VACUUMS,10)
    parameter.setParameterValue(XMLMessageExternalParameter.HOST_ADDRESS,'192.168.0.1')
    parameter.setParameterValue(XMLMessageExternalParameter.HOST_PORT,'43811')
    parameter.setParameterValue(XMLMessageExternalParameter.HOST_TYPE,Router.VACUUM)
    parameter.setParameterValue(XMLMessageExternalParameter.VACUUM_ID,2)

    parameter.createRootNode()
    message = parameter.xml2Char(False)
    print("\n\n{0}".format(parameter.xml2Char(True)))
    channel.receiveXMLReportParseAndDecide(message)
    #dif = XMLIncomingDIF()
    #incoming = dif.determineXMLInformation(message)
    sys.exit(0)
    
    
    from Planner import Planner
    channel = Channel()
    planner = Planner(1.0,1.0,1.0,1.0,4)
    channel.setPlanner(planner)
    channel.receiveXMLReportParseAndDecide(message)
    print(message)


    print("one: {1}\n{0}".format(channel.vacuumArray,len(channel.vacuumArray)))
    channel.setNumberVacuums(7)
    print("two: {1}\n{0}".format(channel.vacuumArray,len(channel.vacuumArray)))
    channel.setNumberVacuums(3)
    print("three: {1}\n{0}".format(channel.vacuumArray,len(channel.vacuumArray)))
