#!/usr/bin/python
#
#  Channel.py
# 
#   Created on: 2 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the channel object
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

# The xml classes used to define the messages being passed.
from XML.XMLParser import XMLParser
from XML.XMLIncomingDIF import XMLIncomingDIF
from XML.XMLMessageNetwork import XMLMessageNetwork

from XML.XMLMessagePlannerReportVacuumOrders import \
     XMLMessagePlannerReportVacuumOrders

from XML.XMLMessageRecommendOrderCommander2Planner import \
     XMLMessageRecommendOrderCommander2Planner

from XML.XMLMessageRecommendOrderPlanner2Commander import \
     XMLMessageRecommendOrderPlanner2Commander

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

class Channel:
    
    
    
    def __init__(self,world=None,vacuums=[],sensor=None,planner=None,commander=None) :

        self.setWorking(True)
        self.setReliability(1.0)   # Probability of properly transmitting the
                                   # message. Default is full reliability.
        
        self.delay = 0.0           # transmission delay - not yet implemented

        self.setWorld(world)
        self.vacuumArray = vacuums # array of object handles
        self.setSensor(sensor)
        self.setPlanner(planner)
        self.setCommander(commander)



    def setWorking(self,value) :
        self.isWorking = value

    def getWorking(self) :
        return(self.isWorking)

    def setReliability(self,value) :
        self.reliability = value

    def getReliability(self) :
        return(self.reliability)

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

    def addVacuum(self,vacuum,id) :
        while(id>=len(self.vacuumArray)) :
            self.vacuumArray.append(None)
        self.vacuumArray[id] = vacuum

    def setWorld(self,value) :
        self.world = value

    def getWorld(self) :
        return(self.world)

    def sendMessage(self) :
        if(self.reliability>random.rand(1)[0]) :
            return(True)
        return(False)


    ## receiveXMLReportParseAndDecide
    #
    # This is a generic routine. It receives an xml report and decides
    # what it is and who it is for. It then calls the specific routine
    # necessary to pass along the information.
    def receiveXMLReportParseAndDecide(self,xmlString) :
        dif = XMLIncomingDIF()
        info = dif.determineXMLInformation(xmlString)


        if(info.getMyInformationType() ==
           XMLParser.MESSAGE_PLANNER_REPORT_VACUUM_ORDERS) :
            
            pos = info.getPos()
            #print("sending report to commander for {0} - {1},{2}".format(
            #    info.getVacuumID(),pos[0],pos[1]))
            self.commander.receiveReport(pos[0],pos[1],info.getVacuumID())



        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_RECOMMEND_ORDER_COMMANDER_PLANNER) :
            
            pos = info.getPos()
            #print("sending report to planner for {0} - {1},{2}".format(
            #    info.getVacuumID(),pos[0],pos[1]))
            self.planner.recommendOrder(info.getVacuumID(),pos[0],pos[1])



        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_RECOMMEND_ORDER_PLANNER_COMMANDER) :
            
            pos = info.getPos()
            #print("sending report to commander for {0} - {1},{2}".format(
            #    info.getVacuumID(),pos[0],pos[1]))
            self.commander.receiveReport(pos[0],pos[1],info.getVacuumID())



        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_MOVE_ORDER_COMMANDER_VACUUM) :
            
            pos = info.getPos()
            vacuumID = info.getVacuumID()
            #print("sending report to vacuum for {0} - {1},{2}".format(
            #    info.getVacuumID(),pos[0],pos[1]))

            if(vacuumID < len(self.vacuumArray)) :
                self.vacuumArray[vacuumID].moveord(pos[0],pos[1])



        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_MOVE_ORDER_COMMANDER_PLANNER) :
            
            pos = info.getPos()
            #print("sending report to planner for {0} - {1},{2}".format(
            #    info.getVacuumID(),pos[0],pos[1]))
            self.planner.receiveOrder(info.getVacuumID(),pos[0],pos[1])



        elif(info.getMyInformationType() ==
             XMLParser.MESSAGE_GET_REPORT_VACUUM_COMMANDER) :
            
            pos = info.getPos()
            #print("sending report to planner for {0} - {1},{2} - {3}".format(
            #    info.getVacuumID(),pos[0],pos[1],info.getStatus()))
            self.commander.getReport(pos[0],pos[1],info.getStatus(),info.getVacuumID())


        elif(info.getMyInformationType() == XMLParser.MESSAGE_WORLD_STATUS) :
            self.sensor.setArray(info.getMatrixFromArray())
    


        elif(info.getMyInformationType() == XMLParser.MESSAGE_WORLD_WETNESS) :
            self.sensor.setWet(info.getMatrixFromArray())



        elif(info.getMyInformationType() == XMLParser.MESSAGE_UPDATE_WORLD_PLANNER) :
            self.planner.updateView()



        elif(info.getMyInformationType() == XMLParser.MESSAGE_UPDATE_REQUEST_PLANNER_SENSOR) :
            self.sensor.measure()



        elif(info.getMyInformationType() == XMLParser.MESSAGE_STATUS_SENSOR_PLANNER) :
            self.planner.setDirtLevels(info.getMatrixFromArray())



        elif(info.getMyInformationType() == XMLParser.MESSAGE_WETNESS_SENSOR_PLANNER) :
            self.planner.setWet(info.getMatrixFromArray())



    ## sendVacuumReportFromCommander2Planner
    #
    # Routine that takes a report from the commander that identifies a
    # particular vacuum and converts it into XML and passes it along
    # to the planner so it will know where the vacuum was sent.
    #
    def sendVacuumReportFromCommander2Planner(self,xPos,yPos,IDnum) :
        if(self.sendMessage()) :
            #print("Sending to id: {0} pos: {1},{2}".format(IDnum,xPos,yPos))
            network = XMLMessagePlannerReportVacuumOrders()
            network.setVacuumID(IDnum)
            network.setPos(xPos,yPos)
            network.createRootNode()
            self.receiveXMLReportParseAndDecide(network.xml2Char())




    ## sendRecommendOrderFromCommander2Planner
    #
    # Routine that takes a recommendation order from the commander
    # that identifies a particular vacuum and converts it into XML and
    # passes the XML tree on to the planner.
    def sendRecommendOrderFromCommander2Planner(self,vacuumID,xPos,yPos) :            
        if(self.sendMessage()) :
            #print("Sending to id: {0} pos: {1},{2}".format(vacuumID,xPos,yPos))
            orders = XMLMessageRecommendOrderCommander2Planner()
            orders.setVacuumID(vacuumID)
            orders.setPos(xPos,yPos)
            orders.createRootNode()
            self.receiveXMLReportParseAndDecide(orders.xml2Char())
            


    ## sendRecommendOrderFromPlanner2Commander
    #
    # Routine that takes a recomendation order from the planner that
    # identifies a particular vacuum and converts it into XML and
    # passes the XML tree on to the commander.
    def sendRecommendOrderFromPlanner2Commander(self,xPos,yPos,IDnum) :
        if(self.sendMessage()) :
            #print("Sending to id: {0} pos: {1},{2}".format(IDnum,xPos,yPos))
            orders = XMLMessageRecommendOrderPlanner2Commander()
            orders.setVacuumID(IDnum)
            orders.setPos(xPos,yPos)
            orders.createRootNode()
            self.receiveXMLReportParseAndDecide(orders.xml2Char())




    ## sendMoveOrderFromCommander2Vacuum
    #
    # Routine that takes an order from the commander and converts it
    # into XML and passed the XML to the vacuum.
    def sendMoveOrderFromCommander2Vacuum(self,xPos,yPos,vacuumID) :
        if(self.sendMessage()) :
            #print("Sending to id: {0} pos: {1},{2}".format(IDnum,xPos,yPos))
            orders = XMLMessageMoveOrderCommanderVacuum()
            orders.setVacuumID(vacuumID)
            orders.setPos(xPos,yPos)
            orders.createRootNode()
            self.receiveXMLReportParseAndDecide(orders.xml2Char())




    ## sendReportFromVacuum2Commander
    #
    # Routine to take a message from the vacuum that is a report for
    # the commander. This routine relays that report to the commander.
    def sendReportFromVacuum2Commander(self,xPos,yPos,status,IDnum) :
        if(self.sendMessage()) :
            #print("Sending status to id: {0} pos: {1},{2} - {3}".format(
            #    IDnum,xPos,yPos,status))
            report = XMLMessageGetReportVacuumCommander()
            report.setVacuumID(IDnum)
            report.setPos(xPos,yPos)
            report.setStatus(status)
            report.createRootNode()
            self.receiveXMLReportParseAndDecide(report.xml2Char())



    ## sendMoveOrderFromCommander2Planner
    #
    # Routine to take a message from the commander that is an order to
    # move a vacuum and relay it to the planner.
    def sendMoveOrderFromCommander2Planner(self,xPos,yPos,IDnum) :
        if(self.sendMessage()) :
            #print("Sending to id: {0} pos: {1},{2}".format(IDnum,xPos,yPos))
            orders = XMLMessageMoveOrderCommanderPlanner()
            orders.setVacuumID(IDnum)
            orders.setPos(xPos,yPos)
            orders.createRootNode()
            self.receiveXMLReportParseAndDecide(orders.xml2Char())



    def sendMeasuredFromPlanner2Sensor(self) :
        sensorData = XMLMessageUpdatePlannerSensor()
        sensorData.createRootNode()
        self.receiveXMLReportParseAndDecide(sensorData.xml2Char())


    def sendStatusSensor2Planner(self,noisyView) :
        sensorData = XMLMessageSensorStatus(noisyView)
        sensorData.createRootNode()
        self.receiveXMLReportParseAndDecide(sensorData.xml2Char())


    def sendWorldStatusToSensor(self,A) :
        worldData = XMLMessageWorldStatus(A)
        worldData.createRootNode()
        self.receiveXMLReportParseAndDecide(worldData.xml2Char())


    def sendWorldWetnessToSensor(self,Moisture):
        worldWetness = XMLMessageWorldWetness(Moisture)
        worldWetness.createRootNode()
        self.receiveXMLReportParseAndDecide(worldWetness.xml2Char())


    def sendPlannerUpdateRequest(self) :
        update = XMLMessageUpdateWorldPlanner()
        update.createRootNode()
        self.receiveXMLReportParseAndDecide(update.xml2Char())



if (__name__ =='__main__') :
    world = World()
    world.inc()

    channel1 = Channel(world)
    channel2 = Channel(world)

    def silly(a,*b) :
        print("type: {0}\n{1}".format(type(a),b))

