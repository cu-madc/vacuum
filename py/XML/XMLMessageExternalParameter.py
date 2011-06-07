#!/usr/bin/python
#
#  XMLMessageExternalParameter.py
# 
#   Created on: 31 May, 2011
#       Author: black
# 
#       Methods for the class that keeps track of the information
#       specific to passing the values of global parameters used in a
#       simulation. This is for a request that comes in from the
#       outside of the simulation.
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
#from XMLIncomingDIF import XMLIncomingDIF
from XMLParser import XMLParser


class XMLMessageExternalParameter (XMLParser) :


    DUST_RATE, DUST_SIZE, \
       RAIN_RATE, RAIN_SIZE, \
       GRID_SIZE, \
       NUMBER_OF_VACUUMS, \
       HOST_ADDRESS, \
       HOST_PORT, \
       HOST_TYPE, \
       VACUUM_ID = range(10)

    ParameterTitles = {DUST_RATE:'dust rate', \
                       DUST_SIZE:'dust size', \
                       RAIN_RATE:'rain rate', \
                       RAIN_SIZE:'rain size', \
                       GRID_SIZE:'grid size', \
                       NUMBER_OF_VACUUMS:'number vacuums', \
		       HOST_ADDRESS:'host address',\
		       HOST_PORT:'host port', \
		       HOST_TYPE:'host type', \
		       VACUUM_ID:"vacuum id"
		       }


    def __init__(self) :
	XMLParser.__init__(self)
	self.setMyInformationType(self.MESSAGE_EXTERNAL_PARAMETER);
	self.dimensionsNode = None
	self.objectClassNode = None


        # Initialize the list of parameters that will be defined in
        # this XML tree. This is a list of things that will be
        # defined. Each entry in the list is a list of information
        # used to define a parameter.
        #
        #    An entry in the previous list has the following form:
        #        [parameter type (ex: DUST_RATE), parameter value (ex: 0.2)]
        #
        self.parameterList = []




    def __del__(self) :
        pass


    def setParameterValue(self,type,value) :

	# Check to see if this parameter has been defined
	for item in self.parameterList:
	    if(item[0] == type) :
		# this parameter has already been defined
		item[1] = value
		return

	# It has not been defined yet. Add it to the list.
        self.parameterList.append([type,value])


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
        nameNode.appendChild(self.doc.createTextNode("External"))
        self.objectClassNode.appendChild(nameNode)

	typeNode = self.doc.createElement("type")
        typeNode.appendChild(self.doc.createTextNode("parameter"))
        self.objectClassNode.appendChild(typeNode)

        self.createDimensions()


    def createDimensions(self):
        # Creates the dimensions node in the xml tree. It adds the
        # objectClass node as a child of the dimensions node. Finally
        # a "name" node is added as a child of the dimensions node.

	self.dimensionsNode = self.doc.createElement("dimensions")
        for type in self.parameterList:
            self.objectClassNode.appendChild(self.dimensionsNode)

            if(type[0] in self.ParameterTitles) :
                self.makeNodeSingleValue(self.ParameterTitles[type[0]],type[1])


    def makeNodeSingleValue(self,name,value) :
        # Method to set the value of the id for this vacuum. It
        # indicates which vacumm this structure is associated
        # with. The value is then added to the xml tree under the
        # dimensions node.

        self.newNode = self.doc.createElement("dimension")
        self.dimensionsNode.appendChild(self.newNode)

        dimension = self.doc.createElement("name")
        node = self.doc.createTextNode(name)
        dimension.appendChild(node)
        self.newNode.appendChild(dimension)

        dimension = self.doc.createElement("value")
        if(type(value) is float) :
            node = self.doc.createTextNode("{0:22.14E}".format(value))
        else :
            node = self.doc.createTextNode(str(value))
                
        dimension.appendChild(node)
        self.newNode.appendChild(dimension)




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
                                


            else :
                # Error - there is more than one object class node.
                if(self.DEBUG) :
                    print("Error - too many object class nodes.")
                self.objectClassNode = None


                





if (__name__ =='__main__') :
    #DUST_RATE, DUST_SIZE, \
	#       RAIN_RATE, RAIN_SIZE, \
	#       GRID_SIZE, \
	#       NUMBER_OF_VACUUMS = range(6)

    parameter = XMLMessageExternalParameter()
    parameter.setParameterValue(XMLMessageExternalParameter.DUST_RATE,0.2)
    parameter.setParameterValue(XMLMessageExternalParameter.RAIN_RATE,0.4)
    parameter.setParameterValue(XMLMessageExternalParameter.GRID_SIZE,5)
    parameter.setParameterValue(XMLMessageExternalParameter.DUST_SIZE,0.3)
    parameter.setParameterValue(XMLMessageExternalParameter.RAIN_SIZE,2.0)
    parameter.setParameterValue(XMLMessageExternalParameter.GRID_SIZE,6)
    parameter.setParameterValue(XMLMessageExternalParameter.NUMBER_OF_VACUUMS,5)
    parameter.setParameterValue(XMLMessageExternalParameter.NUMBER_OF_VACUUMS,8)
    parameter.setParameterValue(XMLMessageExternalParameter.HOST_ADDRESS,'192.168.0.1')
    parameter.setParameterValue(XMLMessageExternalParameter.HOST_PORT,'43811')
    parameter.setParameterValue(XMLMessageExternalParameter.HOST_TYPE,1)
    parameter.setParameterValue(XMLMessageExternalParameter.VACUUM_ID,5)
    print(parameter.parameterList)

    parameter.createRootNode()
    print(parameter.xml2Char(True))


    #print(parameter.xml2Char(True))
    ##root_node = parameter.root_node.cloneNode(True)
    ##parameter.copyXMLTree(root_node)
