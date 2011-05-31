#!/usr/bin/python
#
#   XMLParser.py
#  
#    Created on: Jan 27, 2011
#        Author: black
#  
#    Base class for the data class. This class is inherited by
#    most of the data classes. It is used to manipulate the char
#    buffer that has the xml data and convert it into a parsed
#    xml tree. It also has the associated routines to clean up
#    the xml data structures.
#  
#   This material is based on research sponsored by DARPA under agreement
#   number FA8750-10-2-0165. The U.S. Government is authorized to
#   reproduce and distribute reprints for Governmental purposes
#   notwithstanding any copyright notation thereon.
#  
#   The views and conclusions contained herein are those of the authors
#   and should not be interpreted as necessarily representing the official
#   policies or endorsements, either expressed or implied, of DARPA or the
#   U.S. Government.
#  
#   ==========================================================================
#  
#   For use by entities other than the U.S. Government the following
#   additional limitations apply:
#  
#   Copyright (c) 2011, Clarkson University
#   All rights reserved.
#  
#   Redistribution and use in source and binary forms, with or without
#   modification, are permitted provided that the following conditions are
#   met:
#  
#   * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#  
#   * Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the following
#   disclaimer in the documentation and/or other materials provided
#   with the distribution.
#  
#   * Neither the name of the Clarkson University nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#  
#   THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
#   "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
#   LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
#   A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
#   HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
#   SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
#   LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
#   DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
#   THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
#   (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
#   OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#  
#   (license copied from http://www.opensource.org/licenses/bsd-license)
#  
#  
#  
#

import xml.sax     #.handler


class XMLParser (xml.sax.handler.ContentHandler):

    SIZE_READ_FILE_BUFFER =	131072
    SIZE_READ_DTD_BUFFER  = 262144
    DEBUG = False



    # Constants used to determine what kind of message was
    # passed. This number is assigned based on the contents of the
    # message and help the base object decide what variables should be
    # parsed from the message that is passed.
    EMPTY, CHECK_INCOMING, VACUUM_NETWORK, \
	   VACUUM_STATE, CONTROLER_NETWORK, \
           MESSAGE_PLANNER_REPORT_VACUUM_ORDERS, \
           MESSAGE_RECOMMEND_ORDER_COMMANDER_PLANNER, \
           MESSAGE_RECOMMEND_ORDER_PLANNER_COMMANDER, \
           MESSAGE_MOVE_ORDER_COMMANDER_VACUUM, \
           MESSAGE_MOVE_ORDER_COMMANDER_PLANNER, \
           MESSAGE_GET_REPORT_VACUUM_COMMANDER, \
           MESSAGE_WORLD_STATUS, \
           MESSAGE_WORLD_WETNESS, \
           MESSAGE_UPDATE_WORLD_PLANNER, \
           MESSAGE_UPDATE_REQUEST_PLANNER_SENSOR, \
           MESSAGE_STATUS_SENSOR_PLANNER, \
           MESSAGE_WETNESS_SENSOR_PLANNER, \
           MESSAGE_VACUUM_NEW_POSITION_PLANNER, \
           MESSAGE_WORLD_VACUUM_CURRENT_TIME, \
           MESSAGE_VACUUM_WORLD_ADD_EXPENDITURE, \
           MESSAGE_VACUUM_WORLD_CLEAN_GRID, \
	   MESSAGE_EXTERNAL_PARAMETER, \
	   MESSAGE_EXTERNAL_COMMAND = range(23)
	


    #char fileBuffer[SIZE_READ_FILE_BUFFER];
    #char dtdBuffer[SIZE_READ_DTD_BUFFER];


    def __init__(self) : 
	# *
	# constructor for the XMLParser class. Initializes the xml variables.
	# Initializes the character buffers.
	#
	#

	# Buffer variables
        self.cleanUpXML()

	#  initialize my type
	self.setMyInformationType(XMLParser.EMPTY);

	if(self.DEBUG) :
	    print("XML Parser initialized.");



    def __del__(self):
	#  Destructor for the XMLParser class. Release and
	# delete the parsed XML data structures.
	#  


	#  Delete/release the xml data structures.
	self.cleanUpXML();


    def getBuffer(self) :
        return self.XMLStack      #  returns the pointer to the buffer


    def setBuffer(self,value) :
        self.XMLStack = value
	
    def getXMLDocument(self) :
        return self.doc           #  returns the pointer to the document.

	
    def setMyInformationType(self,value) :
        self.myType = value;
		
    def getMyInformationType(self) :
        return self.myType;


    def startDocument(self):
        self.XMLStack = []
	self.currentStack = []
	xml.sax.handler.ContentHandler.startDocument(self)

	if(self.DEBUG):
	     print("starting to read the document");


    def endDocument(self):
         if(len(self.currentStack)>0) :
	     if(self.DEBUG) :
	         print("There is an error in the XML.")
	 self.currentStack = []
	 xml.sax.handler.ContentHandler.endDocument(self)

	 if(self.DEBUG):
	     print("End of the document:\n{0}".format(self.XMLStack));


    def startElement(self, name, attributes):

        self.currentStack.append([name,attributes.copy(),"",[]])
			
	if(self.DEBUG) :
	    for child in attributes.getNames():
	        print("Child: {0} - {1}".format(child,attributes.getValue(child)))

	self.currentName = name
	if(name == "objectclass"):
	      pass

    def characters(self,data) :
        last = self.currentStack[-1]
        last[-2] += data

    def endElement(self, name):

	thisElement = []
	if((type(self.currentStack) is list) and (len(self.currentStack)>0)) :
	     thisElement = self.currentStack.pop()
	else:
	     if(self.DEBUG):
	         print("There is an error in the xml file.")

	if((type(self.currentStack) is list) and (len(self.currentStack)>0)) :
	    previousElement = self.currentStack.pop()
	    previousElement[-1].append(thisElement)
	    self.currentStack.append(previousElement)

	else :
	    # This is a top level element.
	    self.XMLStack.append(thisElement)
	    previousElement = [""]

	#if(self.DEBUG) :
	#       print("End: {0}".format(name))
	#        print("XML Stack: {0}".format(self.XMLStack))
	#        print("Current Stack: {0}\n\n\n".format(self.currentStack))

                
	self.currentName = previousElement[0]


    ## parseXMLString
    #
    # Parse the contents of an xml string and put them into an
    # XML tree.
    #  
    def parseXMLString(self,xmlString) :
	parser = xml.sax.make_parser(['IncrementalParser'])
	parser.setContentHandler(self)
	parser.reset()
        parser.feed(xmlString)
	parser.close()




    def readXMLFile(self,fileName) :
	# Read an XML file and put it into the local buffer.
	# This routine is mostly in place for testing and
	# debugging 4 the xml codes. 
	#

	parser = xml.sax.make_parser(['IncrementalParser'])
	parser.setContentHandler(self)
	parser.reset()

	file = open(fileName,"r")
	#theXML = ""
	for line in file:
		#theXML += line
		parser.feed(line)
                if(self.DEBUG) :
                    print(line[0:-1])

	parser.close()
	#print(theXML)
        #xml.sax.parseString(theXML,handler)






    def walkObjectChildrenByNameContents(self,currentNode,nodeName,name,contents) :
        # Routine to walk through the tree and find the node
        # that contains a child with the given name and
        # associated contents.
        #  


        if(self.DEBUG) :
            print("\nSearching for node name: {0} with contents {1} node pointer: {2}".format(name,contents,currentNode))

        if(currentNode==None) :
            return(None); #  The node passed in was null.


        for sibling in currentNode:
            #  Go through each of the children of the passed node.

            #print("   now checking node name: ".format(sibling[0]))
            if (sibling[0]==nodeName):
                if (self.checkChildrenForNameAndContents(sibling[3],name,contents)):
                    return (sibling);

            #  Check to see if the target is any of this node's children.
            checkChildren = self.walkObjectChildrenByNameContents \
                (sibling[3],nodeName,name,contents);
            if(checkChildren) :
                #  A match was found. Return it.
                return(checkChildren);


        #  No match was found. Return null.
        return(None);



    def checkChildrenForNameAndContents(self,currentNode,name,contentsToMatch) :
        # Routine to walk through each of the children of the
        # current node. If it has a node with the given name
        # and whose contents match the given value then the
        # result is "true." Otherwise return "false."
        # 

        if(not currentNode) :
            return None
        
        for sibling in currentNode:

            content = sibling[2];
            if(self.DEBUG) :
                print("      checking node name:{0}-{1} #{2}#contents#{3}#".format(sibling[0],name,sibling[2],contentsToMatch))

            if ((sibling[0]==name) and (sibling[2]==contentsToMatch)):
                #  The name of the node matches the name that was passed.
                #  Return this node.
                if(self.DEBUG) :
                    print("   THIS IS A MATCH!")
                return (True)

        return(False)



	
    def getChildWithName(self,currentNode,name) :
        # Routine to walk through the children and return the node whose name
        # matches the value passed through.
        #
        if(currentNode) :
            for sibling in currentNode:
		if (sibling[0]==name):
		    return (sibling);

		checkChildren = self.getChildWithName(sibling[3],name)
		if(checkChildren) :
		    #  A match was found. Return it.
		    return(checkChildren);

                
        return(None);




    def xml2Char(self,debug=False) :
        # Convert the parsed XML file in the local root and then
        # put the char file into the local buffer.
        #
        if(debug) :
            return(self.doc.toprettyxml(indent="  ",newl="\n"))
        else :
            return(self.doc.toprettyxml(indent="",newl=""))

		


    def cleanUpDocument(self) :
        # free the document # 
        self.doc = None


    def cleanUpXML(self):
        # Clean up and free the data and variables associated with the parsed
        # XML tree.
        #  

        #  Clean up the document
        self.cleanUpDocument();

	self.XMLStack = []
	self.currentStack = []

	#  initialize the xml parameters
	self.root_node = None;
	self.currentName = ""









if (__name__ =='__main__') :

    handler = XMLParser()
    handler.readXMLFile("networkSample.xml")

    child = handler.walkObjectChildrenByNameContents(handler.getBuffer(),"dimension","name","networkID")
    print("\n\nThe child: {0}".format(child))
    print("Current stack:\n{0}".format(handler.getBuffer()))
    exit(0)

    parser = xml.sax.make_parser(['IncrementalParser'])
    handler = XMLParser()
    parser.setContentHandler(handler)
    parser.reset()

    file = open("networkSample.xml","r")
    theXML = ""
    for line in file:
	theXML += line
	parser.feed(line)
	#print(line[0:-1])

    parser.close()
    print(theXML)
    #xml.sax.parseString(theXML,handler)
