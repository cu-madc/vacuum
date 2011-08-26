#!/usr/bin/python
#
#  Vacuum.py
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



    def quit(self) :

	if(self.getDataCollection()) :
	    self.worldDataFile.close()
	    self.vacuumDataFile.close()
	    
        exit(0) # Say bye bye!
	

    # Used for the output of data
    def setWorldFileName(self,name) :
	Agent.setWorldFileName(self,name)

	self.worldDataWriter  = csv.writer(self.worldDataFile, delimiter=',',
					   quotechar='\'',
					   quoting=csv.QUOTE_MINIMAL)

	self.worldDataWriter.writerow(["time","row","col","dust","moisture"])
	


    def setVacuumFileName(self,name) :
	Agent.setVacuumFileName(self,name)

	self.vacuumDataWriter = csv.writer(self.vacuumDataFile, delimiter=',',
					   quotechar='\'',
					   quoting=csv.QUOTE_MINIMAL)

	self.vacuumDataWriter.writerow(["time","id","status","working",
				       "xpos","ypos","repairs","odomoter","missions"])


    ## Routine to get the required data.
    def getData(self,timeStep) :


	for vacuum in self.vacuumArray:
	    # Request info from the given vacuum.
	    vacuum.poll()

	# Get the appropriate data associated with the world.
        # self.A is the array of values for dirt levels
        # self.Moisture is the array of values for moisture level
	for row in range(self.N) :
	    for col in range(self.N) :
		self.worldDataWriter.writerow([timeStep,row,col,self.A[row][col],self.Moisture[row][col]])
		
	#self.vacuumDataWriter


    # Get data from a vacuum
    def getVacuumData(self,info) :
	self.vacuumDataWriter.writerow(info)
	


    # Static method that is used as a helper to make it easier to
    # create a data colelctor object.
    @staticmethod
    def spawnDataCollector() :
	data = DataCollector()
	channel = data.initializeChannel()
	return(data)



    
if (__name__ =='__main__') :

    pass
