#!/usr/bin/python
#
#  Router.py
# 
#   Created on: 2 June, 2011
#       Author:  black
# 
#       class definition for the router object. This object will send
#       a string to the correct agent.
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

class Router:

    COMMANDER, \
	       PLANNER, \
	       SENSORARRAY, \
	       VACUUM, \
	       WORLD = range(5)

    DEBUG = False

    def __init__(self,channel) :
	self.channel = channel
	self.agents = [dict(),dict(),dict(),dict(),dict()]
	self.vacuumArray = []     # array of object handles

	self.host_address = ''
	self.port_number  = ''

    def setCommander(self,commander) :
	self.agents[self.COMMANDER]['parent'] = commander

    def setPlanner(self,planner) :
	if(self.DEBUG) :
	    print("Setting planner: {0}".format(planner))
	self.agents[self.PLANNER]['parent'] = planner

    def setSensorArray(self,sensorArray) :
	self.agents[self.SENSORARRAY]['parent'] = sensorArray

    def setVacuum(self,vacuum) :
	self.agents[self.VACUUM]['parent'] = vacuum

    def setWorld(self,world) :
	self.agents[self.WORLD]['parent'] = world

    def setChannel(self,type,channel) :
	if(self.DEBUG) :
	    print("Setting channel: {0}-{1}".format(type,channel))

	self.agents[type]['parent'] = channel

    def getChannel(self,type) :
	return(self.agents[type]['parent'])

    def setDebug(self,value) :
	self.DEBUG = value

    def getDebug(self) :
	return(self.DEBUG)


    def setHost(self,address) :
	#print("setting address: {0}".format(address))
	self.host_address = address


    def setPort(self,port) :
	#print("setting port: {0}".format(port))
	self.port_number  = port


    def addVacuum(self,vacuum,id) :

	for definedVacuum in self.vacuumArray :
	    # Check to see if this vacuum is already defined. We can
	    # get into this routine from a variety of places. It might
	    # be possible to have already called this routine.
	    if(vacuum == definedVacuum) :
		#print("Found this one...")
		return

        while(id>=len(self.vacuumArray)) :
            # There are not enough vacuum objects defined. Create
            # place holders.
            self.vacuumArray.append(None)
        self.vacuumArray[id] = vacuum


    def setNumberVacuums(self,number) :
	# Routine to set the number of vacuums that are being tracked.
	if(number > len(self.vacuumArray)) :
	    # There are more vacuums to be used than currently
	    # defined. Add the extras to the list.
	    for i in range(number-len(self.vacuumArray)):
		#vacuum = Vacuum(len(self.vacuumArray))
		self.addVacuum(None,len(self.vacuumArray))

	elif (number < len(self.vacuumArray)) :
	    # Need to have fewer vacuums than what are currently
	    # defined. Delete the extras.
	    while(len(self.vacuumArray)>number) :
		vacuum = self.vacuumArray.pop()

		# TODO - this needs to be updated somewhere.... The world is not updating now!
		#if (self.world):
		#    self.world.deleteVacuum(vacuum)
		    

	
    def sendString(self,destination,message,vacuumID=-1,debug=False):

	if((destination == self.VACUUM) and
	   (vacuumID>-1) and
	   (vacuumID < len(self.vacuumArray))) :
	    if(debug) :
		print("Router.sendString: {0}".format(vacuumID))
		self.vacuumArray[vacuumID].checkInfoType = True

	    self.vacuumArray[vacuumID].receiveXMLReportParseAndDecide(message)
	
	elif('parent' in self.agents[destination]):
	    if(self.agents[destination]['parent']) :
		if(debug) :
		    self.agents[destination]['parent'].checkInfoType = True
		self.agents[destination]['parent'].receiveXMLReportParseAndDecide(message)



