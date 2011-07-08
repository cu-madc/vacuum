#!/usr/bin/python
#
#  XMLMessageForAgent.py
# 
#   Created on: 7 July, 2011
#       Author: black
# 
#       Methods for the class that is used to create specific nodes of
#       the xml tree based on what they are supposed to provide.
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

#from xml.dom.minidom import Document
from XMLMessageCreator import XMLMessageCreator

import sys
import os
sys.path.append( os.path.join( os.getcwd(), '..' ) )

from Agent import Agent


class XMLMessageForAgent (XMLMessageCreator) :


    def __init__(self) :
        XMLMessageCreator.__init__(self)


    def __del__(self) :
        pass



    def addPosition(self,posX,posY) :
	self.addNodeWithValue("xPos",posX)
	self.addNodeWithValue("yPos",posY)

    def vacuumID(self,IDnum) :
	self.addNodeWithValue("vacuumID",IDnum)

    def addStatus(self,status):
	self.addNodeWithValue("status",status)

    def addExpenditure(self,expenditure) :
	self.addNodeWithValue("expenditure",str(expenditure))


    ## VacuumReportFromCommander2Planner
    #
    # Routine that takes a report from the commander that identifies a
    # particular vacuum and converts it into XML.
    #
    def VacuumReportFromCommander2Planner(self,xPos,yPos,IDnum) :
	self.createRootNode(False)
	self.createObjectClassElements(Agent.PLANNER,"Vacuum Orders")
	self.addPosition(xPos,yPos)
	self.vacuumID(IDnum)
	#print(self.xml2Char())


    ## RecommendOrderFromCommander2Planner
    #
    # Routine that takes a recommendation order from the commander
    # that identifies a particular vacuum and converts it into XML.
    def RecommendOrderFromCommander2Planner(self,IDnum,xPos,yPos) :
	self.createRootNode(False)
	self.createObjectClassElements(Agent.PLANNER,"Vacuum Recommendation")
	self.addPosition(xPos,yPos)
	self.vacuumID(IDnum)
	#print(self.xml2Char())



    ## RecommendOrderFromPlanner2Commander
    #
    # Routine that takes a recomendation order from the planner that
    # identifies a particular vacuum and converts it into XML.
    def RecommendOrderFromPlanner2Commander(self,xPos,yPos,IDnum) :
	self.createRootNode(False)
	self.createObjectClassElements(Agent.COMMANDER,"Vacuum Recommendation")
	self.addPosition(xPos,yPos)
	self.vacuumID(IDnum)
	#print(self.xml2Char())


    ## MoveOrderFromCommander2Vacuum
    #
    # Routine that takes an order from the commander and converts it
    # into XML.
    def MoveOrderFromCommander2Vacuum(self,xPos,yPos,IDnum) :
	self.createRootNode(False)
	self.createObjectClassElements(Agent.VACUUM,"Move Order")
	self.addPosition(xPos,yPos)
	self.vacuumID(IDnum)
	#print(self.xml2Char())


    ## ReportFromVacuum2Commander
    #
    # Routine to take a message from the vacuum that is a report for
    # the commander.
    def ReportFromVacuum2Commander(self,xPos,yPos,status,IDnum) :
	self.createRootNode(False)
	self.createObjectClassElements(Agent.COMMANDER,"Get Report")
	self.addPosition(xPos,yPos)
	self.vacuumID(IDnum)
	self.addStatus(status)
	#print(self.xml2Char())



    ## MoveOrderFromCommander2Planner
    #
    # Routine to take a message from the commander that is an order to
    # move a vacuum for a planner.
    def MoveOrderFromCommander2Planner(self,xPos,yPos,IDnum) :
	self.createRootNode(False)
	self.createObjectClassElements(Agent.PLANNER,"Move Order")
	self.addPosition(xPos,yPos)
	self.vacuumID(IDnum)
	#print(self.xml2Char())


    ## MeasuredFromPlanner2Sensor
    #
    # Routine to take a request from the planner to get information
    # from the sensor to send it to the sensor.
    def MeasuredFromPlanner2Sensor(self) :
	self.createRootNode(False)
	self.createObjectClassElements(Agent.SENSOR,"Send Planner Update")
	#print(self.xml2Char())



    ## PlannerUpdateRequest
    #
    # Routine to send a request for an update to the planner. This
    # tells the planner that it needs to take whatever actions are
    # necessary during a world time step.
    def PlannerUpdateRequest(self) :
	self.createRootNode(False)
	self.createObjectClassElements(Agent.PLANNER,"Update")
	#print(self.xml2Char())



    ## PlannerVacuumMovedPosition
    #
    # Routine to send the new position of a vacuum. This comes from a
    # vacuum and is sent to a planner.
    def PlannerVacuumMovedPosition(self,idnum,xpos,ypos) :
        self.createRootNode(False)
	self.createObjectClassElements(Agent.PLANNER,"New Vacuum Location")
	self.addPosition(xpos,ypos)
	self.vacuumID(idnum)
	#print(self.xml2Char())


    ## VacuumWorldExpenditure
    #
    # Routine to create an expenditure from a vacuum to the world. 
    def VacuumWorldExpenditure(self,expenditure,id) :
        self.createRootNode(False)
	self.createObjectClassElements(Agent.WORLD,"Add Expenditure")
	self.vacuumID(id)
	self.addExpenditure(expenditure)
	#print(self.xml2Char())


    ## WorldCleanedGrid
    #
    # Routine to let a vacuum send an update to the world to let it
    # know that a grid area has been cleaned.
    def WorldCleanedGrid(self,idnum,xpos,ypos) :
        self.createRootNode(False)
	self.createObjectClassElements(Agent.WORLD,"Clean Grid")
	self.addPosition(xpos,ypos)
	self.vacuumID(idnum)
	#print(self.xml2Char())


    ## StatusSensor2Planner
    #
    # Routine to define the xml for a noisy view of the world's grids
    # to the planner from the sensor.
    def StatusSensor2Planner(self,noisyView) :
        self.createRootNode(False)
	self.createObjectClassElements(Agent.PLANNER,"Sensor Status")
	self.addArrayNode(noisyView)
	#print(self.xml2Char())



    ## WorldWetnessToSensor
    #
    # Routine to send the world's wetness levels to a sensor.
    def WorldWetnessToSensor(self,Moisture):
        self.createRootNode(False)
	self.createObjectClassElements(Agent.SENSOR,"World Wetness")
	self.addArrayNode(Moisture)
	#print(self.xml2Char())
	


if (__name__ =='__main__') :
    from XMLParser import XMLParser
    
    IDnum  = 0
    xPos   = 1
    yPos   = 2
    status = 4

    N = 5;
    A = zeros((N,N),dtype=float64)        # array of values for dirt levels
    for i in range(N) :
        for j in range(N) :
            A[i,j] = i*N+j


    from XMLMessageWorldWetness import XMLMessageWorldWetness
    sensorData = XMLMessageWorldWetness(A)
    sensorData.createRootNode()
    print(sensorData.xml2Char(True))

    network = XMLMessageForAgent()
    network.WorldWetnessToSensor(A)
    print(network.xml2Char(True))

    
#    from XMLIncomingDIF import XMLIncomingDIF
#    dif = XMLIncomingDIF()
#    dif.parseXMLString(network.xml2Char())
#    for dimension in dif:
#	print(dimension)
