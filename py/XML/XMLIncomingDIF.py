#!/usr/bin/python
#
#  XMLIncomingDIF.c++
# 
#   Created on: Jan 15, 2011
#       Author: black
# 
#       Methods for the XMLIncomingDIF class. Used to decide what
#       kind of object is associated with the information passed
#       in through the socket connection.
#
# This material is based on research sponsored by DARPA under agreement
# number FA8750-10-2-0165. The U.S. Government is authorized to
# reproduce and distribute reprints for Governmental purposes
# notwithstanding any copyright notation thereon.
#
# The views and conclusions contained herein are those of the authors
# and should not be interpreted as necessarily representing the official
# policies or endorsements, either expressed or implied, of DARPA or the
# U.S. Government.
#
# ==========================================================================
#
# For use by entities other than the U.S. Government the following
# additional limitations apply:
#
# Copyright (c) 2011, Clarkson University
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
# * Redistributions of source code must retain the above copyright
#   notice, this list of conditions and the following disclaimer.
#
# * Redistributions in binary form must reproduce the above
#   copyright notice, this list of conditions and the following
#   disclaimer in the documentation and/or other materials provided
#   with the distribution.
#
# * Neither the name of the Clarkson University nor the names of its
#   contributors may be used to endorse or promote products derived
#   from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# (license copied from http:# www.opensource.org/licenses/bsd-license)
#
#


#include <iostream>
#include <fstream>
#include <string.h>

from XMLParser import XMLParser
from XMLMessageVacuumIDPosBase import XMLMessageVacuumIDPosBase

from XMLMessageGetReportVacuumCommander import \
     XMLMessageGetReportVacuumCommander

from XMLMessageWorldStatus import \
     XMLMessageWorldStatus

from XMLMessageWorldWetness import \
     XMLMessageWorldWetness

from XMLMessageUpdateWorldPlanner import \
     XMLMessageUpdateWorldPlanner

from XMLMessageUpdatePlannerSensor import \
     XMLMessageUpdatePlannerSensor

from XMLMessageSensorStatus import \
     XMLMessageSensorStatus

from XMLMessageSensorWetness import \
     XMLMessageSensorWetness

from XMLMessageWorldVacuumCurrentTime import \
     XMLMessageWorldVacuumCurrentTime

from XMLMessageVacuumAddExpenditureWorld import \
     XMLMessageVacuumAddExpenditureWorld

from XMLMessageExternalParameter import \
     XMLMessageExternalParameter

from XMLMessageExternalCommand import \
     XMLMessageExternalCommand

class XMLIncomingDIF (XMLParser) :

    DEBUG = False

    def __init__(self) :
        XMLParser.__init__(self)
        self.setMyInformationType(XMLParser.CHECK_INCOMING);


    def __del__(self):
        pass


    def getObjectClassName(self,name) :
        # Routine to determine the name associated with objectClass
        # part of the xml file.

	# Walk through the tree and find the object class node.
        objectClass = self.walkObjectName(self.getBuffer(),"objectClass");

	if(objectClass) :
            # The object class node was found.
            if(self.DEBUG):
                print("\n\nobjectClass: {0}\n".format(objectClass))

            for sibling in objectClass[3] :
                # Go through each of the children and look for a name node.
                if(self.DEBUG):
                    print("This node name: {0}".format(sibling[0]))

                if(sibling[0]=="name") :
                     # Found the name node. Report the value for this node.
                    return(sibling[2])

        return(None)



    def getObjectClassNameAndType(self) :
        # Routine to determine the name and type associated with
        # objectClass part of the xml file.
        name = None
        type = None

	# Walk through the tree and find the object class node.
        objectClass = self.walkObjectName(self.getBuffer(),"objectClass");

	if(objectClass) :
            # The object class node was found.
            if(self.DEBUG):
                print("\n\nobjectClass: {0}\n".format(objectClass))

            for sibling in objectClass[3] :
                # Go through each of the children and look for a name node.
                if(self.DEBUG):
                    print("This node name: {0}".format(sibling[0]))

                if(sibling[0]=="name") :
                     # Found the name node. Report the value for this node.
                    name = sibling[2]

                elif(sibling[0] == "type") :
                    type = sibling[2]

        #print("my buffer: {0}".format(self.getBuffer()))
        return([name,type])

        


    def walkObjectName(self,currentNode,name) :
        # Walk through the current parsed tree and look for the object node.

        if(currentNode) :
            for sibling in currentNode:
                #  Go through each of the children of the passed node.

                if(sibling[0]==name) :
                    # The name of the node matches the name that was
                    # passed.  Return this node.
                    return(sibling)

                # Check to see if the target is any of this object's children.
                checkChildren = self.walkObjectName(sibling[3],name);
                if(checkChildren) :
                    # A match was found. Return it.
                    return(checkChildren)

        # No match was found. Return null.
        return(None)



    ## determineXMLInformation(self,passedXML)
    #
    #  Method that takes information in the form of the parsed XML
    #  tree and decides what kind of information it contains. It then
    #  creates the appropriate object to hold the information and
    #  returns it.
    def determineXMLInformation(self,passedXML) :
        self.parseXMLString(passedXML)
        [name,type] = self.getObjectClassNameAndType()
        incomingXML = None
	#print("Name: {0} Type: {1}".format(name,type))


        if( (name=="Planner") and (type == "Vacuum Orders")) :
            # This is a message to be sent to a planner that contains
            # the orders to a vacuum from the commander. Define the
            # vacuum and its position.
            
            incomingXML = XMLMessageVacuumIDPosBase()
            dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
                vacuum = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","vacuumID")
                xPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","xPos")
                yPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","yPos")
                #print("{0}\n{1}\n{2}".format(vacuum,xPos,yPos))

                if(vacuum) :
                    incomingXML.setVacuumID(vacuum[3][1][2])

                if(xPos) :
                    incomingXML.setXPos(xPos[3][1][2])

                if(yPos) :
                    incomingXML.setYPos(yPos[3][1][2])
                    

                if(self.DEBUG) :
                    print("This data represents information from a planner from a commander with the orders for a vacuum")

            incomingXML.specifyInformationType(XMLParser.MESSAGE_PLANNER_REPORT_VACUUM_ORDERS)



        elif( (name=="Planner") and (type == "Vacuum Recommendation")) :
            # This is a message from a commander sent to a planner to
            # let the planner know the recommendation made for the
            # movement of a vacuum. Define the vacuum and its
            # position.
            incomingXML = XMLMessageVacuumIDPosBase()
            dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
                vacuum = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","vacuumID")
                xPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","xPos")
                yPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","yPos")
                #print("{0}\n{1}\n{2}".format(vacuum,xPos,yPos))

                if(vacuum) :
                    incomingXML.setVacuumID(vacuum[3][1][2])

                if(xPos) :
                    incomingXML.setXPos(xPos[3][1][2])

                if(yPos) :
                    incomingXML.setYPos(yPos[3][1][2])
                    

                if(self.DEBUG) :
                    print("This data represents information from a commander to a planner with the suggested orders for a vacuum")

            incomingXML.specifyInformationType(XMLParser.MESSAGE_RECOMMEND_ORDER_COMMANDER_PLANNER)



        elif( (name=="Commander") and (type=="Vacuum Recommendation")) :
            # This is a message from Planner to send the
            # recommendation of a move to the commander. Define the
            # vacuum and its position.
            incomingXML = XMLMessageVacuumIDPosBase()
            dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
                vacuum = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","vacuumID")
                xPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","xPos")
                yPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","yPos")
                #print("{0}\n{1}\n{2}".format(vacuum,xPos,yPos))

                if(vacuum) :
                    incomingXML.setVacuumID(vacuum[3][1][2])

                if(xPos) :
                    incomingXML.setXPos(xPos[3][1][2])

                if(yPos) :
                    incomingXML.setYPos(yPos[3][1][2])
                    

                if(self.DEBUG) :
                    print("This data represents information from a planner to a commander with the suggested orders for a vacuum")


            incomingXML.specifyInformationType(XMLParser.MESSAGE_RECOMMEND_ORDER_PLANNER_COMMANDER)


        elif( (name=="World") and (type=="Clean Grid")) :
            # This is the message from a Vacuum to send its location
            # to the world. Define the vacuum and its position.
            incomingXML = XMLMessageVacuumIDPosBase()
            dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
                vacuum = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","vacuumID")
                xPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","xPos")
                yPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","yPos")
                #print("{0}\n{1}\n{2}".format(vacuum,xPos,yPos))

                if(vacuum) :
                    incomingXML.setVacuumID(vacuum[3][1][2])

                if(xPos) :
                    incomingXML.setXPos(xPos[3][1][2])

                if(yPos) :
                    incomingXML.setYPos(yPos[3][1][2])
                    

                if(self.DEBUG) :
                    print("This data represents information from a vacuum to the world to indicate a spot is cleaned.")

            incomingXML.specifyInformationType(XMLParser.MESSAGE_VACUUM_WORLD_CLEAN_GRID)




        elif( (name=="Vacuum") and (type=="Move Order")) :
            # This is a message send from a Commander to a Vacuum to
            # give the vacuum the order to move. Define the vacuum and
            # its future position.
            
            incomingXML = XMLMessageVacuumIDPosBase()
            dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
                vacuum = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","vacuumID")
                xPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","xPos")
                yPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","yPos")
                #print("{0}\n{1}\n{2}".format(vacuum,xPos,yPos))

                if(vacuum) :
                    incomingXML.setVacuumID(vacuum[3][1][2])

                if(xPos) :
                    incomingXML.setXPos(xPos[3][1][2])

                if(yPos) :
                    incomingXML.setYPos(yPos[3][1][2])
                    

                if(self.DEBUG) :
                    print("This data represents information from a planner to a commander with the suggested orders for a vacuum")

            incomingXML.specifyInformationType(XMLParser.MESSAGE_MOVE_ORDER_COMMANDER_VACUUM)




        elif( (name=="Planner") and (type=="Move Order")) :
            # This is a message from the commander to the planner to
            # let the planner know what order was sent. Define the
            # vacuum and its position.
            
            incomingXML = XMLMessageVacuumIDPosBase()
            dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
                vacuum = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","vacuumID")
                xPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","xPos")
                yPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","yPos")
                #print("{0}\n{1}\n{2}".format(vacuum,xPos,yPos))

                if(vacuum) :
                    incomingXML.setVacuumID(vacuum[3][1][2])

                if(xPos) :
                    incomingXML.setXPos(xPos[3][1][2])

                if(yPos) :
                    incomingXML.setYPos(yPos[3][1][2])
                    

                if(self.DEBUG) :
                    print("This data represents information from a planner to a commander with the suggested orders for a vacuum")

            incomingXML.specifyInformationType(XMLParser.MESSAGE_MOVE_ORDER_COMMANDER_PLANNER)



        elif( (name=="Commander") and (type=="Get Report")) :
            # This is a message from the Vacuum to the commander to
            # let the commander know the position and status of a
            # vacuum. Need to define the position and status.
            incomingXML = XMLMessageGetReportVacuumCommander()
            dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
                vacuum = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","vacuumID")
                xPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","xPos")
                yPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","yPos")

                status = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","status")

                if(vacuum) :
                    incomingXML.setVacuumID(vacuum[3][1][2])

                if(xPos) :
                    incomingXML.setXPos(xPos[3][1][2])

                if(yPos) :
                    incomingXML.setYPos(yPos[3][1][2])

                if(status) :
                    incomingXML.setStatus(status[3][1][2])

                pos = incomingXML.getPos()
                #print("id: {0} pos: {1},{2} Status: {3}".format(
                #    incomingXML.getVacuumID(),pos[0],pos[1],incomingXML.getStatus()))
                                

                if(self.DEBUG) :
                    print("This data represents information from a planner to a commander with the suggested orders for a vacuum")



        elif( (name=="Sensor") and (type=="World Status")) :
            # This is a message from the World to the Sensor to let it
            # know the status of the world.
            incomingXML = XMLMessageWorldStatus()



        elif( (name=="Sensor") and (type=="World Wetness")) :
            # This is a message from the world to the Sensor to let it
            # know the wetness levels of the world.
            incomingXML = XMLMessageWorldWetness()



        elif( (name=="Planner") and (type=="Update")) :
            # This is a message from the Sensor to the planner to let
            # it know the status of the world.
            incomingXML = XMLMessageUpdateWorldPlanner()



        elif( (name=="Sensor") and (type=="Send Planner Update")) :
            # This is a message from the planner to the sensor to
            # request an update.
            incomingXML = XMLMessageUpdatePlannerSensor()



        elif( (name=="Planner") and (type=="Sensor Status")) :
            # This is a message from the Sensor to the Planner to
            # provide a status of the world as the Sensor currently
            # understands it.
            incomingXML = XMLMessageSensorStatus()



        elif( (name=="Planner") and (type=="Sensor Wetness")) :
            # This is message from the Sensor to the Planner to let
            # the Planner know what the Sensor thinks is the current
            # wetness levels of the world.
            incomingXML = XMLMessageSensorWetness()



        elif( (name=="Planner") and (type=="New Vacuum Location")) :
            # This is a message from the Vacuum to the planner to give
            # the planner a report of its activities. Define the
            # vacuum and its position.
            
            incomingXML = XMLMessageVacuumIDPosBase()
            dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
                vacuum = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","vacuumID")
                xPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","xPos")
                yPos = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","yPos")
                #print("{0}\n{1}\n{2}".format(vacuum,xPos,yPos))

                if(vacuum) :
                    incomingXML.setVacuumID(vacuum[3][1][2])

                if(xPos) :
                    incomingXML.setXPos(xPos[3][1][2])

                if(yPos) :
                    incomingXML.setYPos(yPos[3][1][2])

            incomingXML.specifyInformationType(XMLParser.MESSAGE_VACUUM_NEW_POSITION_PLANNER)



        elif( (name=="Vacuum") and (type=="World Time")) :
            # This is a message from the world to the vacuum. It lets
            # the vacuum know what the world time is. Set the vacuum's
            # ID and the time.
            
            incomingXML = XMLMessageWorldVacuumCurrentTime()
            dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
                vacuum = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","vacuumID")
                time = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","time")
                #print("{0}\n{1}".format(vacuum,time))

                if(vacuum) :
                    incomingXML.setVacuumID(vacuum[3][1][2])

                if(time) :
                    incomingXML.setTime(time[3][1][2])


        elif( (name=="World") and (type=="Add Expenditure")) :
            # This is a message from a vacuum to the World. It sends
            # an expenditure required for the vacuum.
            incomingXML = XMLMessageVacuumAddExpenditureWorld()
            dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
                vacuum = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","vacuumID")
                expenditure = self.walkObjectChildrenByNameContents(
                    dimensions[3],"dimension","name","expenditure")
                #print("{0}\n{1}".format(vacuum,expenditure))

                if(vacuum) :
                    incomingXML.setVacuumID(vacuum[3][1][2])

                if(expenditure) :
                    incomingXML.setExpenditure(expenditure[3][1][2])


        elif( (name=="External") and (type=="parameter")) :
	    # This is an external message. It has information about a
	    # set of parameters.
	    incomingXML = XMLMessageExternalParameter()

	    # Get all of the information associated with the
	    # dimensions that were passed.
	    dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
		# For each dimension go through and decide what type of dimension it is.
		for dimension in dimensions[3]:
		    name  = self.getChildWithName([dimension],"name")    # Get the name leaf on the tree
		    value = self.getChildWithName([dimension],"value")   # Get the value leaf on the tree

		    #print("Value {0} - {1}".format(name[2],value[2]))
		    for key, val in XMLMessageExternalParameter.ParameterTitles.iteritems():
			# Go through each member of the possible parameters and check for a match
			#print("check {0} - {1}".format(key,val))
			if(val == name[2]) :
			    # This is the same type. Set the parameter
			    incomingXML.setParameterValue(key,value[2])
			    break


        elif( (name=="External") and (type=="command")) :
	    # This is an external message. It has information about an
	    # action to take.
	    incomingXML = XMLMessageExternalCommand()

	    # Get all of the information associated with the
	    # dimensions that were passed.
	    dimensions = self.getChildWithName(self.getBuffer(),"dimensions")

            if(dimensions) :
		# For each dimension go through and decide what type of dimension it is.
		for dimension in dimensions[3]:
		    name  = self.getChildWithName([dimension],"name")    # Get the name leaf on the tree


		    #print("Value {0} - {1}".format(name[2],value[2]))
		    for key, val in XMLMessageExternalCommand.ParameterTitles.iteritems():
			# Go through each member of the possible parameters and check for a match
			#print("check {0} - {1}".format(key,name[2]))
			if(val == name[2]) :
			    # This is the same type. Set the parameter
			    #print("Setting: {0}".format(key))
			    incomingXML.setParameterValue(key)
			    break



        if(incomingXML) :
            # If an incoming XML object was created then pass along
            # the array object that was set. If no array object was
            # set before calling this method then this will not do
            # anything. It is caught in the set buffer method.
            incomingXML.setBuffer(self.getBuffer())

        return(incomingXML)




if (__name__ =='__main__') :
    parameter = XMLMessageExternalCommand()
    parameter.setParameterValue(XMLMessageExternalCommand.STOP)
    parameter.setParameterValue(XMLMessageExternalCommand.START)
    parameter.setParameterValue(XMLMessageExternalCommand.RESTART)
    parameter.setParameterValue(XMLMessageExternalCommand.RESET)
    parameter.setParameterValue(XMLMessageExternalCommand.POLL)
    #print(parameter.parameterList)
    parameter.createRootNode()

    incoming = XMLIncomingDIF()
    incoming.determineXMLInformation(parameter.xml2Char(False))
