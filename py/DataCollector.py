#!/usr/bin/python
#
#  DataCollector.py
# 
#   Created on: 24 Aug, 2011
#       Author: Kelly Black
# 
#       class definition for the a data collector object
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

#from numpy import *
#from numpy.linalg import *

import csv
import re
#import sys

from Channel import Channel
from Router import Router
from Agent import Agent
from XML.XMLMessageForAgent import XMLMessageForAgent


class DataCollector (Agent): 
    # Data collector object


    def __init__(self,channel=None) : #class constructor
	Agent.__init__(self,Router.DATACOLLECTOR)
	self.setChannel(channel)              #channel to commander



    def setChannel(self,value) :
        Agent.setChannel(self,value)

    # Method to handle an incoming message and determine what to do
    def handleMessage(self,type,passedInformation) :
	#print("DataCollector.handleMessage: {0} - {1}".format(type,passedInformation))

	if (type=="Move Order") :
	    pass

	elif (type=="World Time") :
	    pass



    def shutdownServer(self) :
	Agent.shutdownServer(self)
	
	if(self.worldDataFile) :
	    print("Closing the world data file");
	    self.worldDataFile.close()
	    self.worldDataFile = None

	if(self.vacuumDataFile) :
	    print("Closing the vacuum data file");
	    self.vacuumDataFile.close()
	    self.vacuumDataFile = None
	    
        #exit(0) # Say bye bye!
	

    # Used for the output of data
    def setWorldFileName(self,name) :
	Agent.setWorldFileName(self,name)

	#self.worldDataWriter  = csv.writer(self.worldDataFile, delimiter=',',
	#				   quotechar='\'',
	#				   quoting=csv.QUOTE_MINIMAL)

	#self.worldDataWriter.writerow(["time","row","col","dust","moisture"])

	if(name) :
	    self.openWorldDataFile("w")
	    if(self.worldDataFile) :
		self.worldDataFile.write("time,row,col,dust,moisture\n")
		self.worldDataFile.close()
		self.worldDataFile = None
	


    def setVacuumFileName(self,name) :
	Agent.setVacuumFileName(self,name)

	#self.vacuumDataWriter = csv.writer(self.vacuumDataFile, delimiter=',',
	#				   quotechar='\'',
	#				   quoting=csv.QUOTE_MINIMAL)

	#self.vacuumDataWriter.writerow(["time","id","status","working",
	#			       "xpos","ypos","repairs","odomoter","missions"])

	if(name) :
	    self.openVacuumDataFile("w")
	    if(self.vacuumDataFile) :
		self.vacuumDataFile.write(
		    "time,id,status,working,xpos,ypos,repairs,odomoter,missions\n")
		self.vacuumDataFile.close()
		self.vacuumDataFile = None



    # Method to handle an incoming message and determine what to do
    def handleMessage(self,type,passedInformation) :
	#print("DataCollector.handleMessage, type:/{0}/ - {1}".format(type,passedInformation))

	if (type=="world data") :
	    theData = passedInformation["data"]
	    #print("World data: {0}".format(theData))

	    if((not self.worldDataFile) and self.getWorldFileName()):
		self.openWorldDataFile("a")
		
	    if(self.worldDataFile) :
		self.worldDataFile.write(theData + "\n")
		#print(self.worldDataFile)

	elif (type=="vacuum data") :
	    theData = passedInformation["data"]
	    #print("vacuum data: {0}".format(theData))

	    if((not self.vacuumDataFile) and self.getVacuumFileName()) :
		self.openVacuumDataFile("a")
		
	    if(self.vacuumDataFile) :
		#print("writing the vacuum data...")
		self.vacuumDataFile.write(theData + "\n")
	    


    # Static method that is used as a helper to make it easier to
    # create a data colelctor object.
    @staticmethod
    def spawnDataCollector() :
	data = DataCollector()
	channel = data.initializeChannel()
	return(data)



# Simple class to accumulate a string of csv values.
class Accumulator :
   def __init__(self) :
        self.myData = ""
   def write(self,newInfo) :
        self.myData += newInfo
   def get(self) :
        return(self.myData)


# Simple class to take a list of information and make a single line to
# be used in a csv file.
class RowData :
    scrubLineEndings = re.compile(r'[\r\n]+')
    def __init__(self,info) :
	self.myAccumulator = Accumulator()
	self.myCSV = csv.writer(self.myAccumulator)
	self.addRow(info)

    def addRow(self,info) :
	self.myCSV.writerow(info)

    def getInfo(self) :
	current = self.myAccumulator.get()
	return(self.scrubLineEndings.sub('',current))

    
if (__name__ =='__main__') :


    # Set the host addresses and ports for the different agents
    agentInterfaces = {Router.SENSORARRAY  :['10.0.1.10',10000],
		       Router.PLANNER      :['10.0.1.11',10001],
		       Router.COMMANDER    :['10.0.1.12',10002],
		       Router.DATACOLLECTOR:['10.0.1.14',10004],
		       Router.WORLD        :['10.0.1.13',10003]}

    # Set the host addresses and ports for the different vacuums 
    vacummInterfaces = [ ['10.0.1.14',10004],
			 ['10.0.1.15',10005],
			 ['10.0.1.16',10006]]

    # create and set the data collector
    dataCollector = DataCollector()
    
    # Set the ip info for the dataCollector and start it in its own process
    dataCollector.setHostname(agentInterfaces[Router.DATACOLLECTOR][0])
    dataCollector.setPort(agentInterfaces[Router.DATACOLLECTOR][1])
    dataCollector.run()
