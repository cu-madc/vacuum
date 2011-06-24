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



# The xml classes used to define the messages being passed.
from XML.XMLParser import XMLParser
from XML.XMLIncomingDIF import XMLIncomingDIF
from XML.XMLMessageNetwork import XMLMessageNetwork

from XML.XMLMessageVacuumIDPosBase import XMLMessageVacuumIDPosBase

from XML.XMLMessageGetReportVacuumCommander import \
     XMLMessageGetReportVacuumCommander

from XML.XMLMessageWorldStatus import \
     XMLMessageWorldStatus

from XML.XMLMessageWorldWetness import \
     XMLMessageWorldWetness

from XML.XMLMessageUpdateWorldPlanner import \
     XMLMessageUpdateWorldPlanner

from XML.XMLMessageUpdatePlannerSensor import \
     XMLMessageUpdatePlannerSensor

from XML.XMLMessageSensorWetness import \
     XMLMessageSensorWetness

from XML.XMLMessageSensorWetness import \
     XMLMessageSensorWetness

from XML.XMLMessageSensorStatus import \
     XMLMessageSensorStatus

from XML.XMLMessageWorldVacuumCurrentTime import \
     XMLMessageWorldVacuumCurrentTime

from XML.XMLMessageVacuumAddExpenditureWorld import \
     XMLMessageVacuumAddExpenditureWorld

from XML.XMLMessageExternalCommand import \
     XMLMessageExternalCommand     

from XML.XMLMessageExternalParameter import \
     XMLMessageExternalParameter

# The xml classes used to define the messages being passed.
from XML.XMLParser import XMLParser
from XML.XMLIncomingDIF import XMLIncomingDIF
from XML.XMLMessageNetwork import XMLMessageNetwork

#from XML.XMLMessagePlannerReportVacuumOrders import \
#     XMLMessagePlannerReportVacuumOrders

#from XML.XMLMessageRecommendOrderCommander2Planner import \
#     XMLMessageRecommendOrderCommander2Planner

#from XML.XMLMessageRecommendOrderPlanner2Commander import \
#     XMLMessageRecommendOrderPlanner2Commander

from XML.XMLMessageVacuumIDPosBase import XMLMessageVacuumIDPosBase

from XML.XMLMessageMoveOrderCommanderVacuum import \
     XMLMessageMoveOrderCommanderVacuum

from XML.XMLMessageMoveOrderCommanderPlanner import \
     XMLMessageMoveOrderCommanderPlanner

from XML.XMLMessageGetReportVacuumCommander import \
     XMLMessageGetReportVacuumCommander

from XML.XMLMessageWorldStatus import \
     XMLMessageWorldStatus

from XML.XMLMessageWorldWetness import \
     XMLMessageWorldWetness

from XML.XMLMessageUpdateWorldPlanner import \
     XMLMessageUpdateWorldPlanner

from XML.XMLMessageUpdatePlannerSensor import \
     XMLMessageUpdatePlannerSensor

from XML.XMLMessageSensorWetness import \
     XMLMessageSensorWetness

from XML.XMLMessageSensorWetness import \
     XMLMessageSensorWetness

from XML.XMLMessageSensorStatus import \
     XMLMessageSensorStatus

from XML.XMLMessageVaccumMovedReportToPlanner import \
     XMLMessageVaccumMovedReportToPlanner

from XML.XMLMessageWorldVacuumCurrentTime import \
     XMLMessageWorldVacuumCurrentTime

from XML.XMLMessageVacuumAddExpenditureWorld import \
     XMLMessageVacuumAddExpenditureWorld

from XML.XMLMessageVacuumCleanWorld import \
     XMLMessageVacuumCleanWorld

## Channel
#
# Creates a channel, which is a medium through which simulated agents communicate.
#
# This channel uses local function calls, not sockets, for communication.
class Channel:

    checkInfoType = False
    DEBUG = False
    
    
    def __init__(self,world=None,sensor=None,planner=None,commander=None) :

        self.setWorking(True)        
        self.delay = 0.0           # transmission delay - not yet implemented

        self.setWorld(world)
        self.vacuumArray = [] # array of object handles
        self.setSensor(sensor)
        self.setPlanner(planner)
        self.setCommander(commander)

	self.router = SocketRouter(self)
	self.vacuum = None

	self.myAgent = None


    # Utility routines.
    #
    # These methods are used for setting the values of certain
    # parameters and is primarily used for outside objects when it is
    # necessary to make a change to a Channel object.
    
    def setWorking(self,value) :
        self.isWorking = value

    def getWorking(self) :
        return(self.isWorking)

    def setSensor(self,sensor) :
        self.sensor = sensor

    def getSensor(self) :
        return(self.sensor)

    def setCommander(self,value):
        self.commander = value

    def getCommander(self) :
        return(self.commander)

    def setPlanner(self,planner) :
        self.planner = planner

    def getPlanner(self) :
        return(self.planner)

    def getRouter(self) :
	return(self.router)

    def setVacuum(self,vacuum) :
	self.vacuum = vacuum

    def getVacuum(self):
	return(self.vacuum)

    def setDebug(self,value) :
	Channel.DEBUG = value
	self.router.setDebug(value)

    def getDebug(self) :
	return(Channel.DEBUG)

    def setRouterChannel(self,type,channel) :
	self.router.setChannel(type,channel)

    def setMyAgent(self,myAgent) :
	self.myAgent = myAgent

    def getMyAgent(self) :
	return(self.myAgent)

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

	if (vacuum and self.world):
	    self.world.addVacuum(vacuum,debug)


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
		
		if (self.world):
		    self.world.deleteVacuum(vacuum)
		    


    def setWorld(self,value) :
        self.world = value

    def getWorld(self) :
        return(self.world)



    ## receiveXMLReportParseAndDecide
    #
    # This is a generic routine. It receives an xml report and decides
    # what it is and who it is for. It then calls the specific routine
    # necessary to pass along the information.
    def receiveXMLReportParseAndDecide(self,xmlString) :
        dif = XMLIncomingDIF()
        info = dif.determineXMLInformation(xmlString)
	if(Channel.checkInfoType) :
	    print("Got information: {0}".format(info.getMyInformationType()))
	    Channel.checkInfoType = False


        if(info.getMyInformationType() ==
           XMLParser.MESSAGE_PLANNER_REPORT_VACUUM_ORDERS) :
            
            if(self.planner) :
                pos = info.getPos()
                #print("sending report to planner for {0} - {1},{2}".format(
                #    info.getVacuumID(),pos[0],pos[1]))
                self.planner.receiveReport(pos[0],pos[1]) #,info.getVacuumID())



        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_RECOMMEND_ORDER_COMMANDER_PLANNER) :
	    #print("Channel.recieveXMLReportParseAndDecide - send!")
            if(self.planner) :
                pos = info.getPos()
                #print("sending report to planner for {0} - {1},{2}".format(
                #    info.getVacuumID(),pos[0],pos[1]))
                self.planner.recommendOrder(info.getVacuumID(),pos[0],pos[1])



        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_RECOMMEND_ORDER_PLANNER_COMMANDER) :
            
            if(self.commander) :
                pos = info.getPos()
                #print("Channel.receiveXMLReportParseAndDecide sending report to commander for {0} - {1},{2}".format(
                #    info.getVacuumID(),pos[0],pos[1]))
                self.commander.receiveReport(pos[0],pos[1],info.getVacuumID())



        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_MOVE_ORDER_COMMANDER_VACUUM) :
            
            pos = info.getPos()
            vacuumID = info.getVacuumID()
            #print("Channel: sending report to vacuum for {0} - {1},{2}".format(
            #    info.getVacuumID(),pos[0],pos[1]))

            #if(vacuumID < len(self.vacuumArray)) :
	    if(self.vacuum) :
		#print("Moving this vacuum {0} - {1},{2}".format(vacuumID,pos[0],pos[1]))
		self.vacuum.moveord(pos[0],pos[1])
                #self.vacuumArray[vacuumID].moveord(pos[0],pos[1])


        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_VACUUM_WORLD_CLEAN_GRID) :

            if(self.world) :
                pos = info.getPos()
                vacuumID = info.getVacuumID()
                #print("sending cleaning report to world from vacuum for {0} - {1},{2}".format(
                #   info.getVacuumID(),pos[0],pos[1]))

                self.world.clean(pos[0],pos[1])


        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_WORLD_VACUUM_CURRENT_TIME) :
            
            time = info.getTime()
            vacuumID = info.getVacuumID()
            #print("sending report to vacuum for {0}".format(vacuumID))

            #if(vacuumID < len(self.vacuumArray)) :
	    if(self.vacuum) :
		#print("sending to vacuum.")
		self.vacuum.timeStep(time,info.getMatrixFromArray())
                #self.vacuumArray[vacuumID].timeStep(time,info.getMatrixFromArray())


        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_VACUUM_WORLD_ADD_EXPENDITURE) :

            if(self.world) :
                expenditure = info.getExpenditure()
                vacuumID = info.getVacuumID()
                #print("sending expenditure report to world for {0} - {1}".format(
                #    info.getVacuumID(),expenditure))

                self.world.addExpenditure(expenditure)


        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_MOVE_ORDER_COMMANDER_PLANNER) :
            
            if(self.planner) :
                pos = info.getPos()
                #print("sending report to planner for {0} - {1},{2}".format(
                #    info.getVacuumID(),pos[0],pos[1]))
                self.planner.receiveOrder(info.getVacuumID(),pos[0],pos[1])


        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_VACUUM_NEW_POSITION_PLANNER) :
            
            if(self.planner) :
                pos = info.getPos()
                #print("sending vacuum position to planner for {0} - {1},{2}".format(
                #    info.getVacuumID(),pos[0],pos[1]))
                self.planner.setVacuumLocation(info.getVacuumID(),pos[0],pos[1])



        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_GET_REPORT_VACUUM_COMMANDER) :

            if(self.commander) :
                pos = info.getPos()
                #print("sending report to commander for {0} - {1},{2} - {3}".format(
                #    info.getVacuumID(),pos[0],pos[1],info.getStatus()))
                self.commander.getReport(pos[0],pos[1],info.getStatus(),info.getVacuumID())


        elif(info.getMyInformationType() == XMLParser.MESSAGE_WORLD_STATUS) :
	    #print("Send world status to the sensor.")
            if(self.sensor) :
                # let the sensor know the world status.
		# print("Channel.receiveXMLReportParseAndDecide-XMLParser.MESSAGE_WORLD_STATUS")
                self.sensor.setArray(info.getMatrixFromArray())
    


        elif(info.getMyInformationType() == XMLParser.MESSAGE_WORLD_WETNESS) :
            if(self.sensor) :
                # Let the sensor know the wetness levels of the world.
		#print("Channel.receiveXMLReportParseAndDecide - XMLParser.MESSAGE_WORLD_WETNESS")
                self.sensor.setWet(info.getMatrixFromArray())



        elif(info.getMyInformationType() == XMLParser.MESSAGE_UPDATE_WORLD_PLANNER) :

	    #print("Send world update to planner");
            if(self.planner):
                # Request that the planner make an update to its view.
		#print("Update planner")
                self.planner.updateView()



        elif(info.getMyInformationType() == XMLParser.MESSAGE_UPDATE_REQUEST_PLANNER_SENSOR) :
            if(self.sensor) :
                # Request that the sensor make a request to measure
                # the world.
		#print("asking sensor to measure.")
		#print("Channel.receiveXMLReportParseAndDecide - XMLParser.MESSAGE_UPDATE_REQUEST_PLANNER_SENSOR")
                self.sensor.measure()



        elif(info.getMyInformationType() == XMLParser.MESSAGE_STATUS_SENSOR_PLANNER) :
            if(self.planner) :
                # Send the planner what the sensor things the world status is.
		#print("Send planner dirt levels.")
                self.planner.setDirtLevels(info.getMatrixFromArray())



        elif(info.getMyInformationType() == XMLParser.MESSAGE_WETNESS_SENSOR_PLANNER) :
            if(self.planner) :
                # Send the planner what the sensor things is the world
                # wetness levels.
		#print("send planner wet levels")
                self.planner.setWet(info.getMatrixFromArray())



	elif(info.getMyInformationType() == XMLParser.MESSAGE_EXTERNAL_PARAMETER) :
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
		    if(self.planner) :
			#print("send planner dirt rate")
			self.planner.setUnnormalizedDirtRate(float(item[1]))

		    if(self.world) :
			self.world.setDirtRate(float(item[1]))
		    
		elif(item[0] == XMLMessageExternalParameter.DUST_SIZE) :
		    if(self.planner) :
			#print("send planner dirt size")
			self.planner.setUnnormalizedDirtSize(float(item[1]))

		    if(self.world) :
			self.world.setDirtSize(float(item[1]))

		    
		elif(item[0] == XMLMessageExternalParameter.RAIN_RATE):
		    if(self.world) :
			self.world.setRainRate(float(item[1]))

			
		elif(item[0] == XMLMessageExternalParameter.RAIN_SIZE):
		    if(self.world) :
			self.world.setRainSize(float(item[1]))

		    
		elif(item[0] == XMLMessageExternalParameter.GRID_SIZE):
		    if(self.world) :
			self.world.setGridSize(int(item[1]))

		    if(self.sensor):
			#print("Channel.receiveXMLReportParseAndDecide - XMLParser.GRID_SIZE")
			self.sensor.setGridSize(int(item[1]))

		    if(self.planner):
			#print("send planner grid size")
			self.planner.setGridSize(int(item[1]))
		    
		elif(item[0] == XMLMessageExternalParameter.NUMBER_OF_VACUUMS):
		    #print("number vacs: {0}".format(int(item[1])))
		    self.setNumberVacuums(int(item[1]))
		    
		    if(self.world) :
			self.world.setNumberVacuums(int(item[1]))


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

		    

	elif(info.getMyInformationType() == XMLParser.MESSAGE_EXTERNAL_COMMAND) :
	    # This is a message from the outside with information
	    # about a command request
	    #print("External Command")
	    for item in info.parameterList:

		if(item == XMLMessageExternalCommand.STOP) :
		    print("stop: {0}".format(item))
		    if(self.world) :
			pass

		elif(item == XMLMessageExternalCommand.START) :
		    print("start: {0}".format(item))
		    if(self.world) :
			pass

		elif(item == XMLMessageExternalCommand.RESTART) :
		    #print("restart: {0}".format(item))
		    if(self.world) :
			pass


	            if(self.sensor) :
			#self.sensor.shutdownServer()
			pass
		    
		    if(self.planner):
			#self.planner.shutdownServer()
			pass

		    if(self.commander) :
			#self.commander.shutdownServer()
			pass

		    if(self.vacuum) :
			#self.vacuum.shutdownServer()
			self.vacuum.setWorking(True)
			self.vacuum.setStatus(3)
			self.vacuum.initializeTime(0.0)


		    if(self.world) :
			#self.world.shutdownServer()
			pass



		elif(item == XMLMessageExternalCommand.RESET) :
		    print("reset: {0}".format(item))
		    if(self.world) :
			pass

		elif(item == XMLMessageExternalCommand.POLL) :
		    print("poll: {0}".format(item))
		    if(self.world) :
			pass

		elif(item == XMLMessageExternalCommand.EXIT) :
		    #print("exit: {0}".format(item))

		    if(self.sensor) :
			#print("Shutting down the server")
			self.sensor.shutdownServer()
		    
		    if(self.planner):
			#print("Shutting down the planner")
			self.planner.shutdownServer()

		    if(self.commander) :
			#print("Shutting down the commander")
			self.commander.shutdownServer()

		    if(self.vacuum) :
			#print("Shutting down the vacuum")
			self.vacuum.shutdownServer()

		    if(self.world) :
			#print("Shutting down the world")
			self.world.shutdownServer()


    ## sendVacuumReportFromCommander2Planner
    #
    # Routine that takes a report from the commander that identifies a
    # particular vacuum and converts it into XML and passes it along
    # to the planner so it will know where the vacuum was sent.
    #
    def sendVacuumReportFromCommander2Planner(self,xPos,yPos,IDnum) :
        
        #print("Sending to id: {0} pos: {1},{2}".format(IDnum,xPos,yPos))
        #network = XMLMessagePlannerReportVacuumOrders()
        network = XMLMessageVacuumIDPosBase()
        network.setVacuumID(IDnum)
        network.setPos(xPos,yPos)
        network.createRootNode()
        network.specifyInformationType(XMLParser.MESSAGE_PLANNER_REPORT_VACUUM_ORDERS)

	self.sendString(Router.PLANNER,network.xml2Char())
	#self.receiveXMLReportParseAndDecide(network.xml2Char())




    ## sendRecommendOrderFromCommander2Planner
    #
    # Routine that takes a recommendation order from the commander
    # that identifies a particular vacuum and converts it into XML and
    # passes the XML tree on to the planner.
    def sendRecommendOrderFromCommander2Planner(self,vacuumID,xPos,yPos) :            
        
        #print("Sending to id: {0} pos: {1},{2}".format(vacuumID,xPos,yPos))
        #orders = XMLMessageRecommendOrderCommander2Planner()
        orders = XMLMessageVacuumIDPosBase()
        orders.setVacuumID(vacuumID)
        orders.setPos(xPos,yPos)
        orders.createRootNode()
        orders.specifyInformationType(XMLParser.MESSAGE_RECOMMEND_ORDER_COMMANDER_PLANNER)
        

	self.sendString(Router.PLANNER,orders.xml2Char())
	#self.receiveXMLReportParseAndDecide(orders.xml2Char())
            


    ## sendRecommendOrderFromPlanner2Commander
    #
    # Routine that takes a recomendation order from the planner that
    # identifies a particular vacuum and converts it into XML and
    # passes the XML tree on to the commander.
    def sendRecommendOrderFromPlanner2Commander(self,xPos,yPos,IDnum) :
        
        #print("Sending to id: {0} pos: {1},{2}".format(IDnum,xPos,yPos))
        #orders = XMLMessageRecommendOrderPlanner2Commander()
        orders = XMLMessageVacuumIDPosBase()
        orders.setVacuumID(IDnum)
        orders.setPos(xPos,yPos)
        orders.createRootNode()
        orders.specifyInformationType(XMLParser.MESSAGE_RECOMMEND_ORDER_PLANNER_COMMANDER)

	self.sendString(Router.COMMANDER,orders.xml2Char())
	#self.receiveXMLReportParseAndDecide(orders.xml2Char())




    ## sendMoveOrderFromCommander2Vacuum
    #
    # Routine that takes an order from the commander and converts it
    # into XML and passed the XML to the vacuum.
    def sendMoveOrderFromCommander2Vacuum(self,xPos,yPos,vacuumID) :
        
        #print("Sending to id: {0} pos: {1},{2}".format(vacuumID,xPos,yPos))
        #orders = XMLMessageMoveOrderCommanderVacuum()
        orders = XMLMessageVacuumIDPosBase()
        orders.setVacuumID(vacuumID)
        orders.setPos(xPos,yPos)
        orders.createRootNode()
        orders.specifyInformationType(XMLParser.MESSAGE_MOVE_ORDER_COMMANDER_VACUUM)

	self.sendString(Router.VACUUM,orders.xml2Char(),vacuumID)
	#self.receiveXMLReportParseAndDecide(orders.xml2Char())




    ## sendReportFromVacuum2Commander
    #
    # Routine to take a message from the vacuum that is a report for
    # the commander. This routine relays that report to the commander.
    def sendReportFromVacuum2Commander(self,xPos,yPos,status,IDnum) :
        
        #print("Sending status to id: {0} pos: {1},{2} - {3}".format(
        #    IDnum,xPos,yPos,status))
        report = XMLMessageGetReportVacuumCommander()
        report.setVacuumID(IDnum)
        report.setPos(xPos,yPos)
        report.setStatus(status)
        report.createRootNode()

	#Channel.checkInfoType = True
	#print("sending vacuum to commander")
	self.sendString(Router.COMMANDER,report.xml2Char(),-1,False)
	#self.receiveXMLReportParseAndDecide(report.xml2Char())



    ## sendMoveOrderFromCommander2Planner
    #
    # Routine to take a message from the commander that is an order to
    # move a vacuum and relay it to the planner.
    def sendMoveOrderFromCommander2Planner(self,xPos,yPos,IDnum) :
        
        #print("Sending to id: {0} pos: {1},{2}".format(IDnum,xPos,yPos))
        #orders = XMLMessageMoveOrderCommanderPlanner()
        orders = XMLMessageVacuumIDPosBase()
        orders.setVacuumID(IDnum)
        orders.setPos(xPos,yPos)
        orders.createRootNode()
        orders.specifyInformationType(XMLParser.MESSAGE_MOVE_ORDER_COMMANDER_PLANNER)

	self.sendString(Router.PLANNER,orders.xml2Char(),IDnum)
	#self.sendString(Router.PLANNER,orders.xml2Char())
	#self.receiveXMLReportParseAndDecide(orders.xml2Char())



    ## sendMeasuredFromPlanner2Sensor
    #
    # Routine to take a request from the planner to get information
    # from the sensor and send it to the sensor.
    def sendMeasuredFromPlanner2Sensor(self) :
        sensorData = XMLMessageUpdatePlannerSensor()
	#print("Channel.sendMeasuredFromPlanner2Sensor: {0}".format(sensorData.getMyInformationType()))
        sensorData.createRootNode()

	#Channel.checkInfoType = True
	self.sendString(Router.SENSORARRAY,sensorData.xml2Char()) #,-1,True)
	#self.receiveXMLReportParseAndDecide(sensorData.xml2Char())


    def sendStatusSensor2Planner(self,noisyView) :
        sensorData = XMLMessageSensorStatus(noisyView)
	#print("Channel.sendStatusSensor2Planner: {0}".format(sensorData.getMyInformationType()))
        sensorData.createRootNode()

	#Channel.checkInfoType = True
	self.sendString(Router.PLANNER,sensorData.xml2Char()) #,-1,True)
	#self.receiveXMLReportParseAndDecide(sensorData.xml2Char())


    ## sendWorldStatusToSensor
    #
    # Routine to send the world's status to a sensor.
    def sendWorldStatusToSensor(self,A) :
        worldData = XMLMessageWorldStatus(A)
        worldData.createRootNode()
	#print("Channel.sendWorldStatusToSensor: sending data")
	self.sendString(Router.SENSORARRAY,worldData.xml2Char(),-1)
	#self.receiveXMLReportParseAndDecide(worldData.xml2Char())



    ## sendWorldWetnessToSensor
    #
    # Routine to send the world's wetness levels to a sensor.
    def sendWorldWetnessToSensor(self,Moisture):
        worldWetness = XMLMessageWorldWetness(Moisture)
        worldWetness.createRootNode()

	self.sendString(Router.SENSORARRAY,worldWetness.xml2Char())
	#self.receiveXMLReportParseAndDecide(worldWetness.xml2Char())



    ## sendPlannerUpdateRequest
    #
    # Routine to send a request for an update to the planner. This
    # tells the planner that it needs to take whatever actions are
    # necessary during a world time step.
    def sendPlannerUpdateRequest(self) :
        update = XMLMessageUpdateWorldPlanner()
	#print("Channel.sendPlannerUpdateRequest: {0}".format(update.getMyInformationType()))
        update.createRootNode()

	#Channel.checkInfoType = True
	self.sendString(Router.PLANNER,update.xml2Char()) #,-1,True)
	#self.receiveXMLReportParseAndDecide(update.xml2Char())


    ## sendPlannerVacuumMovedPosition
    #
    # Routine to send the new position of a vacuum. This comes from a
    # vacuum and is sent to a planner.
    def sendPlannerVacuumMovedPosition(self,idnum,xpos,ypos) :
        #update = XMLMessageVaccumMovedReportToPlanner()
        update = XMLMessageVacuumIDPosBase()
        update.setVacuumID(idnum)
        update.setPos(xpos,ypos)
        update.createRootNode()
        update.specifyInformationType(XMLParser.MESSAGE_VACUUM_NEW_POSITION_PLANNER)

	self.sendString(Router.PLANNER,update.xml2Char())
	#self.receiveXMLReportParseAndDecide(update.xml2Char())


    ## sendVacuumWorldTime
    #
    # Routine to send the current world time from the world to a
    # vacuum. This tells the vacuum that it needs to take whatever
    # actions are appropriate for a given time step.
    def sendVacuumWorldTime(self,T,id,wetness) :
        newTime = XMLMessageWorldVacuumCurrentTime(T,wetness)
        newTime.setVacuumID(id)
        newTime.createRootNode()
        #print(newTime.xml2Char())

	#print("Channel.sendVacuumWorldTime - {0}".format(id))
	self.sendString(Router.VACUUM,newTime.xml2Char(),id,False)
	#self.receiveXMLReportParseAndDecide(newTime.xml2Char())


    ## sendVacuumWorldExpenditure
    #
    # Routine to send an expenditure from a vacuum to the world. 
    def sendVacuumWorldExpenditure(self,expenditure,id) :
        newExpenditure = XMLMessageVacuumAddExpenditureWorld(expenditure)
        newExpenditure.setVacuumID(id)
        newExpenditure.createRootNode()
        #print(newExpenditure.xml2Char())

	self.sendString(Router.WORLD,newExpenditure.xml2Char(),id)
	#self.receiveXMLReportParseAndDecide(newExpenditure.xml2Char())


    ## sendWorldCleanedGrid
    #
    # Routine to let a vacuum send an update to the world to let it
    # know that a grid area has been cleaned.
    def sendWorldCleanedGrid(self,idnum,xpos,ypos) :
        #update = XMLMessageVacuumCleanWorld()
        update = XMLMessageVacuumIDPosBase()
        update.setVacuumID(idnum)
        update.setPos(xpos,ypos)
        update.createRootNode()
        update.specifyInformationType(XMLParser.MESSAGE_VACUUM_WORLD_CLEAN_GRID)

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
