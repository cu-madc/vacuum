#!/usr/bin/python
#
#  XMLMessageWorldVacuumCurrentTime.py
# 
#   Created on: 6 March, 2011
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

from xml.dom.minidom import Document
from XMLMessageArray import XMLMessageArray
#rom XMLParser import XMLParser


class XMLMessageWorldVacuumCurrentTime (XMLMessageArray) :


    def __init__(self,time=0.0,A=None) :
        XMLMessageArray.__init__(self,A)
	self.setMyInformationType(self.MESSAGE_WORLD_VACUUM_CURRENT_TIME)
        self.vacuumID = -1
        self.setTime(time)


    def __del__(self) :
        pass


        
    def getTime(self) :
        return(self.time)


    def setTime(self,value) :
        self.time = int(value)


    def getVacuumID(self) :
        return(self.vacuumID)


    def setVacuumID(self,value) :
        self.vacuumID = int(value)
        self.updateVacuumIDNode()


    def createObjectClass(self) :
        # Creates the node that contains the object class definition
        # and all of its children.
        self.createObjectClassNodes("Vacuum","World Time")


    def updateVacuumIDNode(self) :
        # Method to change the network ID node to reflect the current
        # value of the network id.
        self.updateValue("vacuumID",self.getVacuumID())



    def setVacuumIDNode(self) :
        # Method to set the value of the id for this vacuum. It
        # indicates which vacumm this structure is associated
        # with. The value is then added to the xml tree under the
        # dimensions node.

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


    def setTimeNode(self) :
        # Method to set the value of the id for this vacuum. It
        # indicates which vacumm this structure is associated
        # with. The value is then added to the xml tree under the
        # dimensions node.

        self.timeNode = self.doc.createElement("dimension")
        self.dimensionsNode.appendChild(self.timeNode)

        dimension = self.doc.createElement("name")
        node = self.doc.createTextNode("time")
        dimension.appendChild(node)
        self.timeNode.appendChild(dimension)

        dimension = self.doc.createElement("value")
        node = self.doc.createTextNode(str(self.getTime()))
        dimension.appendChild(node)
        self.timeNode.appendChild(dimension)


    def createDimensions(self):
        # Creates the dimensions node in the xml tree. It adds the
        # objectClass node as a child of the dimensions node. Finally
        # a "name" node is added as a child of the dimensions node.

        # This overrides the one in the base class because the
        # positions are not needed.

        XMLMessageArray.createDimensions(self)
        self.setVacuumIDNode()
        self.setTimeNode()







if (__name__ =='__main__') :
    from XMLIncomingDIF import XMLIncomingDIF
    
    network = XMLMessageMoveOrderCommanderVacuum()
    network.setVacuumID(3)
    network.setPos(2,4)
    network.createRootNode()
    #print(network.xml2Char())


    network.setVacuumID(1)
    network.setXPos(5)
    network.setYPos(2)
    #print(network.xml2Char())

    #root_node = network.root_node.cloneNode(True)
    #network.copyXMLTree(root_node)


    dif = XMLIncomingDIF()
    xmlString = network.xml2Char()
    info = dif.determineXMLInformation(xmlString)
    info.createRootNode()
    print("theXML:\n{0}".format(info.xml2Char()))
