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
#from XMLParser import XMLParser
from XMLMessageCreator import XMLMessageCreator



class XMLMessageArray (XMLMessageCreator) :

    DEBUG = False

    def __init__(self,A=None) :
        XMLMessageCreator.__init__(self)
        self.setArray(A)
	self.arrayNode = None



    def __del__(self) :
        pass


    def setArray(self,value) :
        self.A = value

        if(self.DEBUG) :
            print("The array:\n{0}".format(self.A))
        


    def createDimensions(self):
        # Creates the dimensions node in the xml tree. It adds the
        # objectClass node as a child of the dimensions node. Finally
        # a "name" node is added as a child of the dimensions node.
	XMLMessageCreator.createDimensions(self)
        self.setArrayNode()
        



    def setArrayNode(self) :
        # Method to set the value of the id for this vacuum. It
        # indicates which vacumm this structure is associated
        # with. The value is then added to the xml tree under the
        # dimensions node.

	# First create an array node to hold the array
	self.arrayNode = self.doc.createElement("dimension")
	self.dimensionsNode.appendChild(self.arrayNode)

	array = self.doc.createElement("array")
	self.arrayNode.appendChild(array)


        rowNum = 0
        #print(self.A)
        for row in self.A:
            colNum = 0
            for col in row:

                # Go through each entry in the array.
                # Create a dimension element for each entry in the array.
                entryNode = self.doc.createElement("entry")
                array.appendChild(entryNode)

                # Specify which row this is coming from.
                dimension = self.doc.createElement("row")
                node = self.doc.createTextNode(str(rowNum))
                dimension.appendChild(node)
                entryNode.appendChild(dimension)

                # specify which column this is coming from.
                dimension = self.doc.createElement("column")
                node = self.doc.createTextNode(str(colNum))
                dimension.appendChild(node)
                entryNode.appendChild(dimension)

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
                entryNode.appendChild(dimension)

                colNum += 1


            rowNum += 1

        # Specify the number of rows in the array.
        #self.arrayNode = self.doc.createElement("dimension")
        #self.dimensionsNode.appendChild(self.arrayNode)
        dimension = self.doc.createElement("NumberRows")
        node = self.doc.createTextNode(str(rowNum))
        dimension.appendChild(node)
        array.appendChild(dimension)

        # specify the number of columns in the array.
        #self.arrayNode = self.doc.createElement("dimension")
        #self.dimensionsNode.appendChild(self.arrayNode)
        dimension = self.doc.createElement("NumberColumns")
        node = self.doc.createTextNode(str(colNum))
        dimension.appendChild(node)
        array.appendChild(dimension)





                


if (__name__ =='__main__') :
    from XMLParser import XMLParser
    from XMLMessageWorldStatus import XMLMessageWorldStatus
    
    XMLParser.DEBUG = True
    A = random.rand(1.0,5,5)[0]
    worldData = XMLMessageWorldStatus(A)
    worldData.createRootNode()
    print("Array:\n{0}".format(worldData.xml2Char(True)))

    sensorData = XMLMessageWorldStatus()
    sensorData.parseXMLString(worldData.xml2Char())
    B = sensorData.getMatrixFromArray()
    print(A)
    print(B)
    #print("\n\n\nDimensions:\n{0}".format(node))

