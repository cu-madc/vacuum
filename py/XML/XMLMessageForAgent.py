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



if (__name__ =='__main__') :
    from XMLMessageVacuumIDPosBase import XMLMessageVacuumIDPosBase
    from XMLParser import XMLParser
    
    IDnum = 0
    xPos  = 1
    yPos  = 2


    orders = XMLMessageVacuumIDPosBase()
    orders.setVacuumID(IDnum)
    orders.setPos(xPos,yPos)
    orders.createRootNode()
    orders.specifyInformationType(XMLParser.MESSAGE_MOVE_ORDER_COMMANDER_VACUUM)
    print(orders.xml2Char(True))

    network = XMLMessageForAgent()
    network.createRootNode(False)
    network.createObjectClassElements(Agent.VACUUM,"Move Order")
    network.addPosition(xPos,yPos)
    network.vacuumID(IDnum)
    print(network.xml2Char(True))

    
    from XMLIncomingDIF import XMLIncomingDIF
    dif = XMLIncomingDIF()
    dif.parseXMLString(network.xml2Char())
    for dimension in dif:
	print(dimension)
