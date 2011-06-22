#!/usr/bin/python
#
#  Agent.py
# 
#   Created on: 15 June, 2011
#       Author: Kelly Black
# 
#       class definition for the base object used by all of the agents.
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

from multiprocessing import Process, Queue

class Agent (Process):

    DEBUG = False

    def __init__(self,type) :
	# Define the other objects that need to be tracked.
	Process.__init__(self)
        self.setChannel(None)
	self.setMyType(type)
	self.queue = Queue()
	self.queueUse = False


    def setChannel(self,value) :
        self.channel = value

    def getChannel(self) :
        return(self.channel)

    def setMyType(self,type) :
	self.myType = type

    def getMyType(self) :
	return(self.myType)

    def setQueueUse(self,value) :
	self.queueUse = value

    def getQueueUse(self) :
	return(queueUse)


    def run(self) :
	self.channel.getRouter().createAndInitializeSocketForever()

    def setHostname(self,hostname) :
	#print("Setting agent hostname: {0}".format(hostname))
        self.channel.getRouter().setHostname(hostname)

    def setPort(self,port) :
	#print("Setting agent port number: {0}".format(port))
        self.channel.getRouter().setPort(port)


    def setHostInformation(self,hostType,host,port,vacuumID=None) :

	if(self.channel and self.channel.getRouter()) :
	    self.channel.getRouter().setHostInformation(hostType,host,port,vacuumID)


    def setRouterChannel(self,type,channel) :

	if(self.channel and self.channel.getRouter()) :
	    self.channel.getRouter().setChannel(type,channel)


    def setVacuumRouterInformation(self,channel,vacuumID=None,xPos=0,yPos=0) :

	if(self.channel) :
	    if(Agent.DEBUG):
		print("Adding vacuum: {0} - {1}".format(channel,vacuumID))
            self.channel.addVacuum(channel,vacuumID,xPos,yPos)
            self.channel.getRouter().addVacuum(channel,vacuumID)


    def printRouterInformation(self,toPrint) :
        if(self.channel) :
            self.channel.getRouter().printHostInformation(toPrint)


    def initializeChannel(self):
	from Channel import Channel
	channel = Channel()
	self.setChannel(channel)
	channel.setMyAgent(self)
	return(channel)


    def run(self) :
	#self.channel.getRouter().printThisHostInformation()
	self.channel.getRouter().createAndInitializeSocketForever()


    def setIPInformation(self,interfaces) :
	for agentType, ipInfo in interfaces.iteritems():
	    self.setHostInformation(agentType,ipInfo[0],ipInfo[1],None)
