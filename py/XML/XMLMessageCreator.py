#!/usr/bin/python
#
#  XMLMessageCreator.py
# 
#   Created on: 29 June, 2011
#       Author: black
# 
#       Methods for the class that is a base class to help in the
#       creation of an XML string. This helps create the basic nodes
#       and allows for routines for creation of other nodes.
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
from XMLParser import XMLParser

import sys
import os
sys.path.append( os.path.join( os.getcwd(), '..' ) )

from Agent import Agent


class XMLMessageCreator (XMLParser) :


    def __init__(self) :
        XMLParser.__init__(self)
	self.dimensionsNode = None
	self.objectClassNode = None


    def __del__(self) :
        pass



    ## createRootNode
    # 
    # Method to create the root node in the xml tree. Sets the
    # scheme information as well.
    #
    def createRootNode(self) :

	self.cleanUpDocument()
        self.doc = Document()
	self.root_node = self.doc.createElement("objectModel");
        self.doc.appendChild(self.root_node)

        self.root_node.setAttribute("xmlns","http://standards.ieee.org/IEEE1516-2010")
        self.root_node.setAttribute("xmlns:xsi","http://www.w3.org/2001/XMLSchema-instance")
        self.root_node.setAttribute("xsi:schemaLocation","http://standards.ieee.org/IEEE1516-2010 http://standards.ieee.org/downloads/1516/1516.2-2010/IEEE1516-DIF-2010.xsd")

        self.createObjectClass()




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
            self.createObjectClassElements(Agent.Commander,"Vacuum Recommendation")

        elif(informationType==self.MESSAGE_MOVE_ORDER_COMMANDER_VACUUM) :
            self.createObjectClassElements(Agent.VACUUM,"Move Order")

        elif(informationType==self.MESSAGE_MOVE_ORDER_COMMANDER_PLANNER) :
            self.createObjectClassElements(Agent.PLANNER,"Move Order")

        elif(informationType==self.MESSAGE_VACUUM_NEW_POSITION_PLANNER) :
            self.createObjectClassElements(Agent.PLANNER,"New Vacuum Location")

        elif(informationType==self.MESSAGE_VACUUM_WORLD_CLEAN_GRID) :
            self.createObjectClassElements(Agent.WORLD,"Clean Grid")


            


    ## createObjectClassElements
    #
    # Creates the node that contains the object class definition and
    # all of its children.
    #
    def createObjectClassElements(self,name,type) :
        if(not self.root_node) :
            self.createRootNode()
            
        node = self.doc.createElement("objects")
        self.root_node.appendChild(node)

        self.objectClassNode = self.doc.createElement("objectClass")
        node.appendChild(self.objectClassNode)

        nameNode = self.doc.createElement("name")
        nameNode.appendChild(self.doc.createTextNode(str(name)))
        self.objectClassNode.appendChild(nameNode)

        typeNode = self.doc.createElement("type")
        typeNode.appendChild(self.doc.createTextNode(str(type)))
        self.objectClassNode.appendChild(typeNode)

        self.createDimensions()



    ## createDimensions
    #
    # Creates the dimensions node in the xml tree. It adds the
    # objectClass node as a child of the dimensions node. Finally a
    # "name" node is added as a child of the dimensions node.
    def createDimensions(self):
        self.dimensionsNode = self.doc.createElement("dimensions")
        self.objectClassNode.appendChild(self.dimensionsNode)
        


    ## makeNodeSingleValue
    #
    # Method to set a value by adding a leaf on to the current
    # tree. The value is then added to the xml tree under the
    # dimensions node.
    def makeNodeSingleValue(self,name) :

        self.newNode = self.doc.createElement("dimension")
        self.dimensionsNode.appendChild(self.newNode)

        dimension = self.doc.createElement("name")
        node = self.doc.createTextNode(name)
        dimension.appendChild(node)
        self.newNode.appendChild(dimension)




    ## getMatrixFromArray
    #
    # Routine to traverse the current tree and search for a set of
    # dimensions that have array elements. All of the array elements
    # are returned in an array
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







    ## getValueOfNode
    #
    # Routine to get the value of a node. It searches the subnodes and
    # returns the first child of text type.
    def getValueOfNode(self,node) :
        for leaf in node :
            for detail in leaf.childNodes:
                if(detail.nodeType == Document.TEXT_NODE) :
                    # This is the row to be used.
                    return(detail.nodeValue)




    ## updateValue(self,valueName,newValue)
    # 
    # Method to change the network ID node to reflect the current
    # value of the network id.
    def updateValue(self,valueName,newValue) :

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







    ## copyXMLTree
    # 
    # Copy the given parsed XML tree into the local tree. Also set
    # the relevant nodes that this class tracks from the tree.
    def copyXMLTree(self,existingDocument) :

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
    pass
