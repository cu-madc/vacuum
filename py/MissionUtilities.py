#!/usr/bin/python
#
#  MissionUtilities.py
# 
#   Created on: 11 Aug, 2011
#       Author: black
# 
#       script to offer some basic utilities that are helpful for
#       creating scripts to run the simulation.
# 
#  This material is based on research sponsored by AFRL under agreement
#  number FA8750-10-2-0245. The U.S. Government is authorized to
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


import sys
from datetime import date
import re
import getopt
import csv
import copy

from Router import Router

class MissionUtilities: 
    # Class to offer some helper utilities to make setting up a
    # simulation easier.


    def __init__(self) : #class constructor

	# First set the data file names.

	# Use the name from the command line argument.

	# Set the default file names
	self.setWorldOutputFileName("worldOutput-#DATESTAMP#.csv")
	self.setVacuumOutputFileName("vacuumOuput-#DATESTAMP#.csv")
	self.setIPInfoFileName("")


	# Create empty ip address information.
	self.ipInformation = []


    ## parseCommandLine(self)
    #
    # Routine to parse the command line options.
    #
    def parseCommandLine(self) :
	args = getopt.getopt(sys.argv[1:],'',["worldData=","vacuumData=","ipInfo="])
	for argument in args[0]:

	    if("--worldData" in argument) :
		self.setWorldOutputFileName(argument[1])

	    if("--vacuumData" in argument) :
		self.setVacuumOutputFileName(argument[1])

	    if("--ipInfo" in argument) :
		#print("setting ip information: {0}".format(argument[1]))
		self.setIPInfoFileName(argument[1])
		self.parseIPInformation()



    ## setWorldOutputFileName(self,fileName)
    #
    # Routine to set the value of the output file for the world data file.
    def setWorldOutputFileName(self,fileName) :
	# Replace the string #DATESTAMP# (if it exists) with
	# a... well, a date stamp of the form YYYY-MM-DD
	theDate = date.today()
	dateStamp = "{0:04d}-{1:02d}-{2:02d}".format(theDate.year,theDate.month,theDate.day)
	self.worldOutputFileName  = re.sub(r"#DATESTAMP#",dateStamp,fileName)


    ## setVacuumOutputFileName(self,fileName)
    #
    # Routine to set the value of the output file for the vacuum data file.
    def setVacuumOutputFileName(self,fileName) :
	# Replace the string #DATESTAMP# (if it exists) with
	# a... well, a date stamp of the form YYYY-MM-DD
	theDate = date.today()
	dateStamp = "{0:04d}-{1:02d}-{2:02d}".format(theDate.year,theDate.month,theDate.day)
	self.vacuumOutputFileName  = re.sub(r"#DATESTAMP#",dateStamp,fileName)



    ## getWorldOutputFileName(self)
    #
    # Routine to get the value of the file name for the world data file.
    def getWorldOutputFileName(self):
	return(self.worldOutputFileName)


    ## getVacuumOutputFileName(self)
    #
    # Routine to get the value of the file name for the vacuum data file.
    def getvacuumOutputFileName(self):
	return(self.vacuumOutputFileName)



    ## setIPInfoFileName(self,fileName)
    #
    # Routine to set the name of the data file that has the ip address information.
    def setIPInfoFileName(self,fileName) :
	self.ipInfoFileName = fileName


    ## getIPInfoFileName(self)
    #
    # Routine to get the name of the data file that has the ip address information.
    def getIPInfoFileName(self) :
	return(self.ipInfoFileName)


    ## setDefaultIPInformation(self,ipInfo,agentType)
    #
    # Routine to set the default ip information for an agent type.
    def setDefaultIPInformation(self,ipInfo,agentType,vacuumID=-1) :

	while(len(self.ipInformation) <= agentType) :
	    self.ipInformation.append(None)

	if(agentType != Router.VACUUM) :
	    self.ipInformation[agentType] = copy.deepcopy(ipInfo)

	else :
	    if(not self.ipInformation[agentType]) :
		self.ipInformation[agentType] = []
		
	    while(len(self.ipInformation[agentType]) <= vacuumID) :
		self.ipInformation[agentType].append(None)

		self.ipInformation[agentType][vacuumID] = copy.deepcopy(ipInfo)
	    


    ## getAgentInformation(self,agentType,id=-1) :
    #
    # Routine to get the ip information of the agent of the given type
    def getAgentInformation(self,agentType,id=-1) :

	if(agentType < len(self.ipInformation)) :
	    # There is an entry for agents of this type.
	    
	    if(agentType == Router.VACUUM) :
		# This is a vacuum. See if the vacuum is defined.
		# TODO test this for vacuums!
		
		if((len(self.ipInformation)>=agentType) and \
		   self.ipInformation[agentType] and 
		   (id>=0) and (id < len(self.ipInformation[agentType]))) :
		    # This vacuum exists.
		    return(self.ipInformation[agentType][id])
		
		else :
		    # This vacuum does not exist.
		    return(None)
		
	    else:
		# This is an agent that is not a vacuum
		return(self.ipInformation[agentType])

	else:
	    # We have no record of this item.
	    return(None)



    ## parseIIPnformation(self)
    #
    # Routine to read in the file that has the ip information and parse it.
    def parseIPInformation(self):

	try:
	    fp = open(self.getIPInfoFileName(),"r")
	except IOError:
	    return(False)

	reader = csv.reader(fp)
	lineNumber = 1;
	for row in reader:
	    #print(row)

	    if(len(row)>0) :
		#print("This is a planner line: {0}".format(row))
		self.setIPInformation(row,lineNumber)
		#print(self.plannerInfo)

	    lineNumber += 1


	fp.close()


    ## convertNameToIndex(self,agent) :
    #
    # Helper routine to take the name of an agent and convert it to
    # the index given in the router class.
    def convertNameToIndex(self,agent) :

	if(agent == 'sensor') :
	    return(Router.SENSORARRAY)
	    
	elif(agent == 'planner') :
	    return(Router.PLANNER)
	    
	elif(agent == 'commander') :
	    return(Router.COMMANDER)
	    
	elif(agent == 'world') :
	    return(Router.WORLD)

	elif(agent == 'vacuum') :
	    return(Router.VACUUM)

	return(-1)


    ## getVacuumID(self,id,lineNumber)
    #
    # Helper routine to determine the vacuum id from the given string.
    def getVacuumID(self,id,lineNumber):
	#print("get vacuum {0}".format(id))
	
	# Convert the name to an integer type.
	try:
	    id = int(id)
	except ValueError:
	    print("Error reading the ip information file, line {0}. Vacuum id not valid. Ignoring the line.".format(lineNumber))
	    return(-1)

	return(id)




    ## setIPInformation(self,row,lineNumber)
    #
    # Helper routine to set the information in the dictionary keeping
    # track of the ip info. 
    def setIPInformation(self,row,lineNumber):

	# determine the information on this line. It is assumed it is
	# not for a vacuum.

	# Get the type of agent that this is for.
	agent = self.convertNameToIndex(row.pop(0))
	if(agent < 0) :
	    print("Error reading the ip information file, line {0}. Agent id is not valid. Ignoring the line.".format(lineNumber))
	    return(False)

	if(agent == Router.VACUUM) :
	    # This is for a vacuum. Get its ID.
	    vacuumID = self.getVacuumID(row.pop(0),lineNumber)
	    if(vacuumID < 0) :
		print("Error reading the ip information file, line {0}. Vacuum number is not valid. Ignoring the line.".format(lineNumber))
		return(False)
	else :
	    vacuumID = -1

	

	# Get the destination agent for this line.
	destID = self.convertNameToIndex(row.pop(0))
	if(destID < 0) :
	    print("Error reading the ip information file, line {0}. Agent id is not valid. Ignoring the line.".format(lineNumber))
	    return(False)

	if(destID == Router.VACUUM) :
	    # It is a vacuum. Get its id.
	    destVacuumID = self.getVacuumID(row.pop(0),lineNumber)
	    if(destVacuumID < 0) :
		print("Error reading the ip information file, line {0}. Vacuum number is not valid. Ignoring the line.".format(lineNumber))
		return(False)
	else :
	    destVacuumID = -1


	ipAddress  = row[0]
	portNumber = row[1]



	# Convert the port number to an integer type.
	try:
	    portNumber = int(portNumber)
	except ValueError:
	    print("Error reading the ip information file, line {0}. Port number not valid. Ignoring the line.".format(lineNumber))
	    return(False)


	if((agent != Router.VACUUM) and (destID != Router.VACUUM)) :
	    # This is information for two agents and neither is a vacuum.
	    self.setAgentIPInformationForNonVacuum(self.ipInformation,agent,destID,
						   ipAddress,portNumber)

	elif(agent != Router.VACUUM) :
	    #This is information to be given to an agent that is not a
	    #vacuum, but the information is for a vacuum.
	    self.setAgentIPInformationForVacuum(self.ipInformation,agent,destVacuumID,ipAddress,portNumber)

	elif(destID != Router.VACUUM) :
	    # This is a vacuum that needs to set its information for a non-vacuum agent.
	    self.setVacuumIPInformationForNonVacuum(vacuumID,destID,ipAddress,portNumber)
	    

	else :
	    # This is vacuum information to be kept by a vacuum.
	    #print("Calling vacuum/vacuum {0} {1} {2} {3}".format(
	    #     vacuumID,destVacuumID,ipAddress,portNumber))
	    self.setVacuumInformationForVacuum(vacuumID,destVacuumID,ipAddress,portNumber)


    ## setAgentIPInformationForNonVacuum(self,agent,destID,ipAddress,portNumber)
    #
    # Routine to set the ip information for a nonvacuum that will be
    # used by an agent that is not a vacuum.
    def setAgentIPInformationForNonVacuum(self,ipInformation,agent,destID,ipAddress,portNumber) :
	
	while(len(ipInformation)<=agent) :
	    ipInformation.append(None)

	if(not ipInformation[agent]) :
	    ipInformation[agent] = {}
 
	ipInformation[agent][destID] = [ipAddress,portNumber]

    ## setAgentIPInformationForVacuum(self,ipInformation,agent,destID,ipAddress,portNumber)
    #
    # Routine to set the ip information for a vacuum (destID) that
    # will be used by an agent that is not a vacuum.
    def setAgentIPInformationForVacuum(self,ipInformation,agent,destID,ipAddress,portNumber) :
	#print("Setting information for {0} with dest {1}".format(agent,destID))
	
	while(len(ipInformation)<=agent) :
	    ipInformation.append(None)

	if(not ipInformation[agent]) :
	    ipInformation[agent] = {}

	if(Router.VACUUM not in ipInformation[agent]) :
	    ipInformation[agent][Router.VACUUM] = []

	while(len(ipInformation[agent][Router.VACUUM]) <= destID) :
	    ipInformation[agent][Router.VACUUM].append(None)

	
	ipInformation[agent][Router.VACUUM][destID] = [ipAddress,portNumber]


    ## setVacuumIPInformationForNonVacuum(self,vacuumID,destID,ipAddress,portNumber)
    #
    # Routine to set an agent's (that is not a vacuum) ip information
    # to be used by a vacuum
    def setVacuumIPInformationForNonVacuum(self,vacuumID,destID,ipAddress,portNumber):

	while(len(self.ipInformation)<=Router.VACUUM) :
	    self.ipInformation.append(None)

	if(not self.ipInformation[Router.VACUUM]) :
	    self.ipInformation[Router.VACUUM] = []

	while(len(self.ipInformation[Router.VACUUM])<=vacuumID) :
	    self.ipInformation[Router.VACUUM].append(None)

	if(not self.ipInformation[Router.VACUUM][vacuumID]) :
	    self.ipInformation[Router.VACUUM][vacuumID] = {}

	self.ipInformation[Router.VACUUM][vacuumID][destID] = [ipAddress,portNumber]
	    
	#print("Vacuum Info: {0}".format(self.ipInformation[Router.VACUUM]))
	


    ## setVacuumInformationForVacuum(self,vacuumID,destID,ipAddress,portNumber)
    #
    # Routine to set the ip information that a vacuum will use for
    # another vacuum.
    def setVacuumInformationForVacuum(self,vacuumID,destVacuumID,ipAddress,portNumber) :

	while(len(self.ipInformation) <= Router.VACUUM) :
	    self.ipInformation.append(None)

	if(not self.ipInformation[Router.VACUUM]) :
	    self.ipInformation[Router.VACUUM] = []

	while(len(self.ipInformation[Router.VACUUM]) <= vacuumID) :
	    self.ipInformation[Router.VACUUM].append(None)

	if(not self.ipInformation[Router.VACUUM][vacuumID]) :
	    self.ipInformation[Router.VACUUM][vacuumID] = {}

	#print("vacuum: {1}/{2}\n{0}".format(self.ipInformation[Router.VACUUM],
	#				    vacuumID,destVacuumID))

	if(Router.VACUUM not in self.ipInformation[Router.VACUUM][vacuumID]):	    
	    self.ipInformation[Router.VACUUM][vacuumID][Router.VACUUM] = []

	while(len(self.ipInformation[Router.VACUUM][vacuumID][Router.VACUUM]) <= destVacuumID) :
	    self.ipInformation[Router.VACUUM][vacuumID][Router.VACUUM].append(None)
	    
	self.ipInformation[Router.VACUUM][vacuumID][Router.VACUUM][destVacuumID] = \
	    [ipAddress,portNumber]
	    
	#print("vacuum: {1}/{2}\n{0}".format(self.ipInformation[Router.VACUUM],
	#				    vacuumID,destVacuumID))


if (__name__ =='__main__') :
    mission = MissionUtilities()
    mission.parseCommandLine()
    #print(mission.getWorldOutputFileName())
    #print(mission.getvacuumOutputFileName())
    #print(mission.getIIPnfoFileName())

    mission.setIPInfoFileName("trial.csv")
    mission.parseIPInformation()

    print("\n\n\nSensor info: {0}".format(\
	mission.getAgentInformation(Router.SENSORARRAY)))

    print("Commander info: {0}".format(\
	mission.getAgentInformation(Router.COMMANDER)))

    print("Planner info: {0}".format(\
	mission.getAgentInformation(Router.PLANNER)))

    print("World info: {0}".format(\
	mission.getAgentInformation(Router.WORLD)))

    print("Vacuum 0 info: {0}".format(\
	mission.getAgentInformation(Router.VACUUM,0)))

    print("Vacuum 1 info: {0}".format(\
	mission.getAgentInformation(Router.VACUUM,1)))

    print("Vacuum 2 info: {0}".format(\
	mission.getAgentInformation(Router.VACUUM,2)))
