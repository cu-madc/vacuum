#!/usr/bin/python
#
#  XMLMessageRecommendOrderCommander2Planner.py
# 
#   Created on: 22 Feb, 2011
#       Author: black
# 
#       Methods for the class that keeps track of the information
#       specific to the commander. This is information that the
#       commander sends to the planner to let the planner know what
#       order went to a vacuum.
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


class XMLMessageVacuumIDPosBase (XMLMessageCreator) :


    def __init__(self) :
        XMLMessageCreator.__init__(self)
	self.vacuumIDNode = None
	self.probSuccessNode = None
        self.xPosNode = None;
        self.yPosNode = None;
	self.vacuumID = -1
        self.xPos = None
        self.yPos = None


    def __del__(self) :
        pass


    # Utility functions used for outside routines to define internal
    # parameters.

    def getVacuumID(self) :
        return(self.vacuumID)


    def setVacuumID(self,value) :
        self.vacuumID = int(value)
        self.updateVacuumIDNode()

    def getPos(self) :
        return([self.xPos,self.yPos])


    def setPos(self,x,y) :
        self.setXPos(x)
        self.setYPos(y)

    def setXPos(self,x) :
        self.xPos = int64(x)
        self.updatePositionNodes()

    def setYPos(self,y) :
        self.yPos = int64(y)
        self.updatePositionNodes()





    ## specifyInformationType
    # 
    # routine to specify what kind of information is being held in
    # this object. It also specifies the elements of the tree that are
    # used for other classes to determine what kind of information is
    # held in the XML that is eventually produced.
    def specifyInformationType(self,informationType) :
        
        self.setMyInformationType(informationType)

        if(informationType==self.MESSAGE_RECOMMEND_ORDER_COMMANDER_PLANNER) :
            self.createObjectClassElements(Agent.PLANNER,"Vacuum Recommendation")

        elif(informationType==self.MESSAGE_PLANNER_REPORT_VACUUM_ORDERS) :
            self.createObjectClassElements(Agent.PLANNER,"Vacuum Orders")

        elif(informationType==self.MESSAGE_RECOMMEND_ORDER_PLANNER_COMMANDER) :
            self.createObjectClassElements(Agent.COMMANDER,"Vacuum Recommendation")

        elif(informationType==self.MESSAGE_MOVE_ORDER_COMMANDER_VACUUM) :
            self.createObjectClassElements(Agent.VACUUM,"Move Order")

        elif(informationType==self.MESSAGE_MOVE_ORDER_COMMANDER_PLANNER) :
            self.createObjectClassElements(Agent.PLANNER,"Move Order")

        elif(informationType==self.MESSAGE_VACUUM_NEW_POSITION_PLANNER) :
            self.createObjectClassElements(Agent.PLANNER,"New Vacuum Location")

        elif(informationType==self.MESSAGE_VACUUM_WORLD_CLEAN_GRID) :
            self.createObjectClassElements(Agent.WORLD,"Clean Grid")


            




    ## createDimensions
    #
    # Creates the dimensions node in the xml tree. It adds the
    # objectClass node as a child of the dimensions node. Finally a
    # "name" node is added as a child of the dimensions node.
    def createDimensions(self):
	XMLMessageCreator.createDimensions(self)
        self.setVacuumIDNode()
        self.setxPositionNode()
        self.setyPositionNode()


    def createObjectClass(self) :
        # Creates the node that contains the object class definition
        # and all of its children. This is a no-op because if it is
        # not defined in a child class nothing needs to happen.
        pass


    ## setVacuumIDNode
    # 
    # Method to set the value of the id for this vacuum. It
    # indicates which vacumm this structure is associated
    # with. The value is then added to the xml tree under the
    # dimensions node.
    def setVacuumIDNode(self) :

        self.vacuumIDNode = self.doc.createElement("dimension")
        self.dimensionsNode.appendChild(self.vacuumIDNode)

        dimension = self.doc.createElement("name")
        node = self.doc.createTextNode("vacuumID")
        dimension.appendChild(node)
        self.vacuumIDNode.appendChild(dimension)

        dimension = self.doc.createElement("value")
        node = self.doc.createTextNode(str(self.getVacuumID()))
        dimension.appendChild(node)
        self.vacuumIDNode.appendChild(dimension)



    ## updateVacuumIDNode
    # 
    # Method to change the network ID node to reflect the current
    # value of the network id.
    def updateVacuumIDNode(self) :
        self.updateValue("vacuumID",self.getVacuumID())



    ## updatePositionNodes
    #
    # Method to change the network ID node to reflect the current
    # value of the network id.
    def updatePositionNodes(self) :
        position = self.getPos()
        self.updateValue("xPos",position[0])
        self.updateValue("yPos",position[1])





    ## setxPositionNode
    # 
    # Method to set the value of the prob. of a successful
    # transmission.
    def setxPositionNode(self) :

        self.xPosNode = self.doc.createElement("dimension")
        self.dimensionsNode.appendChild(self.xPosNode)

        dimension = self.doc.createElement("name")
        node = self.doc.createTextNode("xPos")
        dimension.appendChild(node)
        self.xPosNode.appendChild(dimension)

        position = self.getPos()
        dimension = self.doc.createElement("value")
        node = self.doc.createTextNode("{0}".format(position[0]))
        dimension.appendChild(node)
        self.xPosNode.appendChild(dimension)


    ## setyPositionNode
    #
    # Method to set the value of the prob. of a successful
    # transmission.
    def setyPositionNode(self) :

        self.yPosNode = self.doc.createElement("dimension")
        self.dimensionsNode.appendChild(self.yPosNode)

        dimension = self.doc.createElement("name")
        node = self.doc.createTextNode("yPos")
        dimension.appendChild(node)
        self.yPosNode.appendChild(dimension)

        position = self.getPos()
        dimension = self.doc.createElement("value")
        node = self.doc.createTextNode("{0}".format(position[1]))
        dimension.appendChild(node)
        self.yPosNode.appendChild(dimension)





if (__name__ =='__main__') :
    from XMLParser import XMLParser
    orders = XMLMessageVacuumIDPosBase()

    vacuumID = 0
    xPos = 1
    yPos = 2
    
    orders.setVacuumID(vacuumID)
    orders.setPos(xPos,yPos)
    orders.createRootNode()
    orders.specifyInformationType(XMLParser.MESSAGE_RECOMMEND_ORDER_COMMANDER_PLANNER)
    print(orders.xml2Char(True))

    from XMLIncomingDIF import XMLIncomingDIF
    dif = XMLIncomingDIF()
    dif.parseXMLString(orders.xml2Char())
    print(dif.walkObjectName(dif.getBuffer(),"dimension"))
