#!/usr/bin/python
#
#  XMLMessageNetwork.py
# 
#   Created on: Jan 29, 2011
#       Author: black
# 
#       Methods for the class that keeps track of the information specific
#       to the network associated with a given vacumm.
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

from xml.dom.minidom import Document
from XMLIncomingDIF import XMLIncomingDIF
from XMLParser import XMLParser


class XMLMessageNetwork (XMLIncomingDIF) :


    def __init__(self) :
	XMLIncomingDIF.__init__(self)
	self.setMyInformationType(self.VACUUM_NETWORK);
	self.dimensionsNode = None
	self.objectClassNode = None
	self.networkIDNode = None
	self.probSuccessNode = None
        self.networkID = 0
	self.probSuccessfulTransmission = 1.0



    def __del__(self) :
        pass


    def getNetworkID(self) :
        return(self.networkID)


    def setNetworkID(self,value) :
        self.networkID = value
        self.updateNetworkIDNode()

    def getProbSuccessfulTransmission(self) :
        return(self.probSuccessfulTransmission)


    def setProbSuccessfulTransmission(self,value) :
        self.probSuccessfulTransmission = value
        self.updateProbTransmission()


    def createRootNode(self) :
	# Method to create the root node in the xml tree. Sets the
        #  scheme information as well.
        #

	self.cleanUpDocument()
        self.doc = Document()
	self.root_node = self.doc.createElement("objectModel");
        self.doc.appendChild(self.root_node)

        self.root_node.setAttribute("xmlns","http://standards.ieee.org/IEEE1516-2010")
        self.root_node.setAttribute("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
        self.root_node.setAttribute("xsi:schemaLocation","http://standards.ieee.org/IEEE1516-2010 http://standards.ieee.org/downloads/1516/1516.2-2010/IEEE1516-DIF-2010.xsd")

        self.createObjectClass()


    def createObjectClass(self) :
        # Creates the node that contains the object class definition
        # and all of its children.
        node = self.doc.createElement("objects")
        self.root_node.appendChild(node)

        self.objectClassNode = self.doc.createElement("objectClass")
        node.appendChild(self.objectClassNode)

        nameNode = self.doc.createElement("name")
        nameNode.appendChild(self.doc.createTextNode("vacuumNetwork"))
        self.objectClassNode.appendChild(nameNode)

        self.createDimensions()


    def createDimensions(self):
        # Creates the dimensions node in the xml tree. It adds the
        # objectClass node as a child of the dimensions node. Finally
        # a "name" node is added as a child of the dimensions node.

        self.dimensionsNode = self.doc.createElement("dimensions")
        self.objectClassNode.appendChild(self.dimensionsNode)
        self.setNetworkIDNode()
        self.setProbSuccessNode()
        
        


    def setNetworkIDNode(self) :
        # Method to set the value of the id for this vacuum. It
        # indicates which vacumm this structure is associated
        # with. The value is then added to the xml tree under the
        # dimensions node.

        self.networkIDNode = self.doc.createElement("dimension")
        self.dimensionsNode.appendChild(self.networkIDNode)

        dimension = self.doc.createElement("name")
        node = self.doc.createTextNode("networkID")
        dimension.appendChild(node)
        self.networkIDNode.appendChild(dimension)

        dimension = self.doc.createElement("value")
        node = self.doc.createTextNode(str(self.getNetworkID()))
        dimension.appendChild(node)
        self.networkIDNode.appendChild(dimension)



    def updateNetworkIDNode(self) :
        # Method to change the network ID node to reflect the current
        # value of the network id.
        self.updateValue("networkID",self.getNetworkID())


    def updateProbTransmission(self) :
        # Method to change the network ID node to reflect the current
        # value of the network id.
        self.updateValue("probabilitySuccessfulTransmission",
                         self.getProbSuccessfulTransmission())


    def updateValue(self,valueName,newValue) :
        # Method to change the network ID node to reflect the current
        # value of the network id.

        if(self.dimensionsNode) :
            nodes = self.dimensionsNode.getElementsByTagName("dimension")
            if(nodes.length>0) :

                for dimension in nodes :
                    # Get the value of the network ID in the tree and set
                    # it for this instance
                    networks = dimension.getElementsByTagName("name");
                    for network in networks:
                        for detail in network.childNodes:
                            if((detail.nodeType == Document.TEXT_NODE) and
                               (detail.nodeValue == valueName)) :
                                    # This dimension node is for the network id
                                    values = dimension.getElementsByTagName("value");
                                    for value in values:
                                        for id in value.childNodes:
                                            if(id.nodeType == Document.TEXT_NODE) :
                                                id.nodeValue = newValue




    def setProbSuccessNode(self) :
        # Method to set the value of the prob. of a successful
        # transmission. 

        self.probSuccessNode = self.doc.createElement("dimension")
        self.dimensionsNode.appendChild(self.probSuccessNode)

        dimension = self.doc.createElement("name")
        node = self.doc.createTextNode("probabilitySuccessfulTransmission")
        dimension.appendChild(node)
        self.probSuccessNode.appendChild(dimension)

        dimension = self.doc.createElement("value")
        node = self.doc.createTextNode("{0:22.14E}".format(self.getProbSuccessfulTransmission()))
        dimension.appendChild(node)
        self.probSuccessNode.appendChild(dimension)



    def copyXMLTree(self,existingDocument) :
        # Copy the given parsed XML tree into the local tree. Also set
        # the relevant nodes that this class tracks from the tree.

	#self.copyXMLTree(existingDocument)
        self.root_node = existingDocument.cloneNode(True)

        #print("{0} {1} {2} {3} {4} {5} {6} {7} {8}".format(Document.ELEMENT_NODE, Document.ATTRIBUTE_NODE, Document.TEXT_NODE, Document.CDATA_SECTION_NODE, Document.ENTITY_NODE, Document.PROCESSING_INSTRUCTION_NODE, Document.COMMENT_NODE, Document.DOCUMENT_NODE, Document.DOCUMENT_TYPE_NODE, Document.NOTATION_NODE))

	if(self.root_node) :
            nodes = self.root_node.getElementsByTagName("objectClass")
            if(nodes.length==1) :
                self.objectClassNode = nodes.item(0)

                nodes = self.root_node.getElementsByTagName("dimensions")
                if(nodes.length==1) :
                    self.dimensionsNode = nodes.item(0)

                    # Get the value of the network ID in the tree and set
                    # it for this instance
                    nodes = self.dimensionsNode.getElementsByTagName("dimension");
                    for node in nodes:

                        name = None
                        value = None
                        for detail in node.childNodes:
                            for child in detail.childNodes:
                                if(child.nodeType == Document.TEXT_NODE) :
                                    
                                    if(detail.localName == "name") :
                                        name = child.nodeValue

                                    elif(detail.localName == "value") :
                                        value = child.nodeValue

                        #print("  Name: {0} Value: {1}".format(name,value))
                                
                        if(name == "networkID") :
                            self.setNetworkID(int(value))
                            
                        elif(name == "probabilitySuccessfulTransmission") :
                            self.setProbSuccessfulTransmission(float(value))

                    #print("network: {0} - prob: {1}".format(
                    #    self.getNetworkID(),self.getProbSuccessfulTransmission()))
                        

            else :
                # Error - there is more than one object class node.
                if(self.DEBUG) :
                    print("Error - too many object class nodes.")
                self.objectClassNode = None


                





if (__name__ =='__main__') :
    network = XMLMessageNetwork()
    network.setNetworkID(3)
    network.setProbSuccessfulTransmission(0.3)
    network.createRootNode()
    print(network.xml2Char())


    network.setNetworkID(1)
    network.setProbSuccessfulTransmission(0.22)
    print(network.xml2Char(True))

    #root_node = network.root_node.cloneNode(True)
    #network.copyXMLTree(root_node)
