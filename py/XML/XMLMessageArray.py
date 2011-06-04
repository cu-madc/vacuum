#!/usr/bin/python
#
#  XMLMessageArray.py
# 
#   Created on: 24 Feb, 2011
#       Author: black
# 
#       Methods for the base class that manages information stored in
#       an array.
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
#from XMLIncomingDIF import XMLIncomingDIF
from XMLParser import XMLParser


class XMLMessageArray (XMLParser) :

    DEBUG = False

    def __init__(self,A=None) :
        XMLParser.__init__(self)
        self.setArray(A)
	self.dimensionsNode = None
	self.objectClassNode = None
	self.arrayNode = None



    def __del__(self) :
        pass


    def setArray(self,value) :
        self.A = value

        if(self.DEBUG) :
            print("The array:\n{0}".format(self.A))
        

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




    def createObjectClassNodes(self,nodeName,nodeType) :
        # Creates the node that contains the object class definition
        # and all of its children.
        node = self.doc.createElement("objects")
        self.root_node.appendChild(node)

        self.objectClassNode = self.doc.createElement("objectClass")
        node.appendChild(self.objectClassNode)

        nameNode = self.doc.createElement("name")
        nameNode.appendChild(self.doc.createTextNode(nodeName))
        self.objectClassNode.appendChild(nameNode)

        typeNode = self.doc.createElement("type")
        typeNode.appendChild(self.doc.createTextNode(nodeType))
        self.objectClassNode.appendChild(typeNode)

        self.createDimensions()




    def createDimensions(self):
        # Creates the dimensions node in the xml tree. It adds the
        # objectClass node as a child of the dimensions node. Finally
        # a "name" node is added as a child of the dimensions node.

        self.dimensionsNode = self.doc.createElement("dimensions")
        self.objectClassNode.appendChild(self.dimensionsNode)
        self.setArrayNode()
        



    def setArrayNode(self) :
        # Method to set the value of the id for this vacuum. It
        # indicates which vacumm this structure is associated
        # with. The value is then added to the xml tree under the
        # dimensions node.

        rowNum = 0
        #print(self.A)
        for row in self.A:
            colNum = 0
            for col in row:

                # Go through each entry in the array.
                # Create a dimension element for each entry in the array.
                self.arrayNode = self.doc.createElement("dimension")
                self.dimensionsNode.appendChild(self.arrayNode)

                # Specify which row this is coming from.
                dimension = self.doc.createElement("row")
                node = self.doc.createTextNode(str(rowNum))
                dimension.appendChild(node)
                self.arrayNode.appendChild(dimension)

                # specify which column this is coming from.
                dimension = self.doc.createElement("column")
                node = self.doc.createTextNode(str(colNum))
                dimension.appendChild(node)
                self.arrayNode.appendChild(dimension)

                # Specify the value in the array.
                dimension = self.doc.createElement("value")
                # This is a cheap hack. Need to properly treat the
                # boolean arrays. Question - how to do it? *TODO*
                if(type(col)==bool_) :
                    if(col) :
                        node = self.doc.createTextNode("1.0")
                    else:
                        node = self.doc.createTextNode("0.0")
                else:
                    node = self.doc.createTextNode("{0:22.14E}".format(col))
                dimension.appendChild(node)
                self.arrayNode.appendChild(dimension)

                colNum += 1


            rowNum += 1

        # Specify the number of rows in the array.
        self.arrayNode = self.doc.createElement("dimension")
        self.dimensionsNode.appendChild(self.arrayNode)
        dimension = self.doc.createElement("NumberRows")
        node = self.doc.createTextNode(str(rowNum))
        dimension.appendChild(node)
        self.arrayNode.appendChild(dimension)

        # specify the number of columns in the array.
        self.arrayNode = self.doc.createElement("dimension")
        self.dimensionsNode.appendChild(self.arrayNode)
        dimension = self.doc.createElement("NumberColumns")
        node = self.doc.createTextNode(str(colNum))
        dimension.appendChild(node)
        self.arrayNode.appendChild(dimension)






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


    def setMatrixFromXML(self) :
        # Method to pull out the matrix data from the XML tree.

        if(self.dimensionsNode) :
            nodes = self.dimensionsNode.getElementsByTagName("dimensions")
            if(nodes.length>0) :

                for dimension in nodes :
                    # Get the value of this leaf in the tree. This
                    # should include a row number, a column number,
                    # and the value of the matrix.
                    row = dimension.getElementsByTagName("row");
                    col = dimension.getElementsByTagName("column");
                    value = dimension.getElementsByTagName("value");

                    rowNum = int(self.getValueOfNode(row))
                    colNum = int(self.getValueOfNode(col))
                    arrayVal = float64(self.getValueOfNode(value))
                    self.A[rowNum,colNum] = arrayVal


    def getValueOfNode(self,node) :
        for leaf in node :
            for detail in leaf.childNodes:
                if(detail.nodeType == Document.TEXT_NODE) :
                    # This is the row to be used.
                    return(detail.nodeValue)


    def getMatrixFromArray(self) :

        # Set the default value of the array.
        A = None

        # Get the start of the dimensions.
        nodes = self.getChildWithName(self.getBuffer(),"dimensions")
        if(nodes) :

            # The dimensions was found. Determine the number of rows
            # and columns.
            columns = self.getChildWithName([nodes],"NumberColumns")
            rows    = self.getChildWithName([nodes],"NumberRows")

            if( rows and columns) :
                # the rows and columns was found. Allocate the array.
                numCols = int(columns[2]);
                numRows = int(rows[2]);
                A = zeros((numRows,numCols),dtype=float64)

                # Go through the whole set of dimensions and get the
                # coresponding entry in the array.
                for dimension in nodes[3]:
                    if(dimension[0] == "dimension") :

                        thisRow = -1;
                        thisCol = -1;
                        thisVal = None;
                        for leaf in dimension[3]:
                            
                            if(leaf[0] == "row") :
                                thisRow = int(leaf[2])

                            elif(leaf[0] == "column") :
                                thisCol = int(leaf[2])

                            elif(leaf[0] == "value") :
                                thisVal = float64(leaf[2])
                                
                        if((thisRow>=0) and (thisCol>=0) and thisVal) :
                            A[thisRow,thisCol] = thisVal


        return(A)





    def copyXMLTree(self,existingDocument) :
        # Copy the given parsed XML tree into the local tree. Also set
        # the relevant nodes that this class tracks from the tree.

        self.root_node = existingDocument.cloneNode(True)

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
                            self.setVacuumID(int(value))
                            
                        elif(name == "xPos") :
                            self.setXPos(int64(value))

                        elif(name == "yPos") :
                            self.setYPos(int64(value))

                    #print("network: {0} - prob: {1}".format(
                    #    self.getNetworkID(),self.getProbSuccessfulTransmission()))
                        

            else :
                # Error - there is more than one object class node.
                if(self.DEBUG) :
                    print("Error - too many object class nodes.")
                self.objectClassNode = None


                


if (__name__ =='__main__') :
    XMLParser.DEBUG = True
    A = random.rand(1.0,5,5)[0]
    worldData = XMLMessageWorldStatus(A)
    worldData.createRootNode()
    worldData.setMatrixFromXML()
    print("Array:\n{0}".format(worldData.xml2Char()))

    sensorData = XMLMessageWorldStatus()
    sensorData.parseXMLString(worldData.xml2Char())
    B = sensorData.getMatrixFromArray()
    print(A)
    print(B)
    #print("\n\n\nDimensions:\n{0}".format(node))

