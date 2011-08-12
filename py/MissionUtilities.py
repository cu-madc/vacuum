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
	self.vacuumInfo    = {}
	self.worldInfo     = {}
	self.sensorInfo    = {}
	self.plannerInfo   = {}
	self.commanderInfo = {}


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


    ## setDefaultIPInformation(self,)
    #
    # Routine to set the default ip information to be used in the simulation
    def setDefaultIPInformation(self,vacuumInfo,worldInfo,sensorInfo,plannerInfo,commanderInfo) :
    	self.vacuumInfo    = copy.deepcopy(vacuumInfo)
	self.worldInfo     = copy.deepcopy(worldInfo)
	self.sensorInfo    = copy.deepcopy(sensorInfo)
	self.plannerInfo   = copy.deepcopy(plannerInfo)
	self.commanderInfo = copy.deepcopy(commanderInfo)

    ## getIPInformationVacuum(self,agent)
    #
    # Routine to get the  ip information to be used in the simulation for the vacuum
    def getIPInformationVacuum(self,agent) :
	
	if(agent in self.vacuumInfo) :
	    return(self.vacuumInfo[agent])

	else:
	    return(None)

    ## getIIPnformationWorld(self)
    #
    # Routine to get the  ip information to be used in the simulation for the world
    def getIPInformationWorld(self) :
	return(self.worldInfo)
	
    ## getIIPnformationSensor(self)
    #
    # Routine to get the  ip information to be used in the simulation for the sensor
    def getIPInformationSensor(self) :
	return(self.sensorInfo)
	
    ## getIIPnformationPlanner(self)
    #
    # Routine to get the  ip information to be used in the simulation for the planner
    def getIPInformationPlanner(self) :
	return(self.plannerInfo)
	
    ## getIIPnformationCommander(self)
    #
    # Routine to get the  ip information to be used in the simulation for the commander
    def getIPInformationCommander(self) :
	return(self.commanderInfo)


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
	    print(row)

	    if(len(row)>0) :
	
		if(row[0] == 'planner') :
		    #print("This is a planner line")
		    self.setIPInformation(self.plannerInfo,row,lineNumber)
		    #print(self.plannerInfo)

		elif(row[0] == 'commander') :
		    #print("This is a commander line")
		    self.setIPInformation(self.commanderInfo,row,lineNumber)
		    #print(self.commanderInfo)

		elif(row[0] == 'sensor') :
		    #print("This is a sensor line")
		    self.setIPInformation(self.sensorInfo,row,lineNumber)
		    #print(self.sensorInfo)

		elif(row[0] == 'world') :
		    #print("This is a world line")
		    self.setIPInformation(self.worldInfo,row,lineNumber)
		    #print(self.worldInfo)

		elif(row[0] == "vacuum") :
		    self.setVacuumIPInformation(self.vacuumInfo,row,lineNumber)

	    lineNumber += 1


	fp.close()


    ## setIPInformation(self,theInfo,agent,ipAddress,portNumber,lineNumber)
    #
    # Helper routine to set the information in the dictionary given by
    # theInfo
    def setIPInformation(self,theInfo,row,lineNumber):

	# determine which kind of agent this is for.
	agent = row[1]

	# Determine the port number and ip address.
	if(agent=='vacuum'):
	    
	    try:
		# determine the vacuum number.
		vacuumNumber = int(row[2])
	    except ValueError:
		print("Error reading the ip information file, line {0}. Vacuum number not valid. Ignoring the line.".format(lineNumber))
		return
	    
	    portNumber   = row[4]
	    ipAddress    = row[3]
	else :
	    portNumber = row[3]
	    ipAddress  = row[2]
	    

	# Convert the port number to an integer type.
	try:
	    portNumber = int(portNumber)
	except ValueError:
	    print("Error reading the ip information file, line {0}. Port number not valid. Ignoring the line.".format(lineNumber))
	    return


	if(agent == 'sensor') :
	    index = Router.SENSORARRAY
	    
	elif(agent == 'planner') :
	    index = Router.PLANNER
	    
	elif(agent == 'commander') :
	    index = Router.COMMANDER
	    
	elif(agent == 'world') :
	    index = Router.WORLD
	    

	elif(agent == 'vacuum') :
	    if(Router.VACUUM not in theInfo) :
		theInfo[Router.VACUUM] = []
		
	    #print("vacuum info: {0}, {1}".format(id(theInfo[Router.VACUUM]),theInfo[Router.VACUUM]))
	    while(len(theInfo[Router.VACUUM])<=vacuumNumber) :
		theInfo[Router.VACUUM].append([])

	    theInfo[Router.VACUUM][vacuumNumber] = [ipAddress,portNumber]
	    #print("added vacuum number {0} - {1}: {2}".format(vacuumNumber,ipAddress,theInfo[Router.VACUUM]))
	    return

	while(len(theInfo)<=index) :
	    theInfo.append([])

	theInfo[index] = [ipAddress,portNumber]

    ## setVacuumIPInformation(self,theInfo,agent,ipAddress,portNumber,lineNumber)
    #
    # Helper routine to set the information in the dictionary given by
    # theInfo
    def setVacuumIPInformation(self,theInfo,row,lineNumber):

	# determine which kind of agent this is for.
	agent = row[2]

	# Determine the port number and ip address.
	if(agent=='vacuum'):
	    
	    try:
		# determine the vacuum number.
		vacuumNumber = int(row[3])
	    except ValueError:
		print("Error reading the ip information file, line {0}. Vacuum number not valid. Ignoring the line.".format(lineNumber))
		return
	    
	    portNumber   = row[5]
	    ipAddress    = row[4]
	else :
	    portNumber = row[4]
	    ipAddress  = row[3]
	    

	# Convert the port number to an integer type.
	try:
	    portNumber = int(portNumber)
	except ValueError:
	    print("Error reading the ip information file, line {0}. Port number not valid. Ignoring the line.".format(lineNumber))
	    return

	try:
	    row[1] = int(row[1])
	except ValueError:
	    print("Error reading the ip information file, line {0}. Vacuum ID not valid. Ignoring the line.".format(lineNumber))
	    return
	    
	    

	if(agent == 'sensor') :
	    index = Router.SENSORARRAY
	    
	elif(agent == 'planner') :
	    index = Router.PLANNER
	    
	elif(agent == 'commander') :
	    index = Router.COMMANDER
	    
	elif(agent == 'world') :
	    index = Router.WORLD

	elif(agent == 'vacuum') :
	    if(Router.VACUUM not in theInfo) :
		theInfo[Router.VACUUM] = []
		
	    #print("vacuum info: {0}, {1}".format(id(theInfo[Router.VACUUM]),theInfo[Router.VACUUM]))
	    while(len(theInfo[Router.VACUUM])<=vacuumNumber) :
		theInfo[Router.VACUUM].append([])

	    theInfo[Router.VACUUM][vacuumNumber] = [ipAddress,portNumber]
	    #print("added vacuum number {0} - {1}: {2}".format(vacuumNumber,ipAddress,theInfo[Router.VACUUM]))
	    return

	while(len(theInfo)<=index) :
	    theInfo.append({})

	theInfo[index] = [ipAddress,portNumber]
	print(theInfo)
	    


if (__name__ =='__main__') :
    mission = MissionUtilities()
    mission.parseCommandLine()
    #print(mission.getWorldOutputFileName())
    #print(mission.getvacuumOutputFileName())
    #print(mission.getIIPnfoFileName())

    mission.setIPInfoFileName("trial.csv")
    mission.parseIPInformation()
