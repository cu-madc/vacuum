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

import random

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

	self.setReliability(1.0)   # Probability of properly transmitting the
                                   # message. Default is full reliability.


    def setReliability(self,value) :
        self.reliability = value

    def getReliability(self) :
        return(self.reliability)

    def setCommander(self,commander) :
	self.agents[self.COMMANDER]['parent'] = commander

    def setPlanner(self,planner) :
	if(Router.DEBUG) :
	    print("Router, Setting planner: {0}".format(planner))
	self.agents[self.PLANNER]['parent'] = planner

    def setSensorArray(self,sensorArray) :
	self.agents[self.SENSORARRAY]['parent'] = sensorArray

    def setVacuum(self,vacuum) :
	self.agents[self.VACUUM]['parent'] = vacuum

    def setWorld(self,world) :
	self.agents[self.WORLD]['parent'] = world

    def setChannel(self,type,channel) :
	if(Router.DEBUG) :
	    print("Router, Setting channel: {0}-{1}".format(type,channel))

	self.agents[type]['parent'] = channel

    def getChannel(self,type) :
	return(self.agents[type]['parent'])

    def setDebug(self,value) :
	Router.DEBUG = value

    def getDebug(self) :
	return(Router.DEBUG)




    ## sendMessageOverSocket
    #
    # This method is to be over ridden by a super class.
    def sendMessageOverSocket(self,hostTuple,message) :
	pass

    ## sendMessage(self)
    #
    # This generates a random number to determine if a message should
    # be sent. It is used when the system is in debug mode, and we
    # want to make some local runs under one process.
    def sendMessage(self) :
        if(self.reliability>random.random()) :
            return(True)
        return(False)


    def printHostInformation(self,toPrint) :
        print("Host information {0} : {1}\nVacuums{2}".format(
                toPrint,self.agents,self.vacuumArray))


    ## setHostInformation(self,hostType,host,port,vacuumID)
    #
    # Routine to take information about another agent and add it to
    # the agents list.
    def setHostInformation(self,hostType,host,port,vacuumID):

	#print("\n\n\nInitial Vacuums: {0}".format(self.vacuumArray))

	if((hostType>-1) and (hostType<len(self.agents))) :

	    if(hostType == Router.VACUUM):

		if((vacuumID>-1) and (vacuumID < len(self.vacuumArray))) :
		    # This is a well formed message for a vacuum.
		    self.vacuumArray[vacuumID] = {'host':host,
						  'port':port}

		#print("Router.setHostInformation: this is a vacuum - {0}, {1}\n{2}".format(
		#        vacuumID,self.vacuumArray,self.channel))

	    else:
		self.agents[hostType]['host'] = host
		self.agents[hostType]['port'] = port


	if(Router.DEBUG) :
	    print("Agents: {0}".format(self.agents))
	    print("Vacuums: {0}".format(self.vacuumArray))



    def addVacuum(self,vacuum,id) :

	if(vacuum != None):
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

	#if((hostType<0) or (hostType>=len(self.agents))) :
	#    # This is not a valid destination. Just return.
	#    return

	if(debug):
	    if(destination == self.VACUUM):
		print("Send to Vacuum:  {0}".format(self.vacuumArray))
	    else :
		print("Dest: {0} - {1}".format(destination,self.agents[destination]))


	if(destination == self.VACUUM):
	    # This is a message for a vacuum. Need to check to see if
	    # it has a proper ID.

	    if(debug):
		print("Router.sendString, Send message to vacuum {0} , {1}".format(vacuumID,self.channel))
		
	    if((vacuumID>-1) and (vacuumID < len(self.vacuumArray))) :
		# This is a well formed message for a vacuum.

		if((type(self.vacuumArray[vacuumID]) is dict) and
		   ('host' in self.vacuumArray[vacuumID]) and
		   ('port' in self.vacuumArray[vacuumID])) :
		    # IP iformation is available for this
		    # agent. Send the information over the
		    # network.

		    if(debug) :
			print("Router.sendString, Send tcp message to vacuum {0} {1}".format(
			    self.vacuumArray[vacuumID]['host'],self.vacuumArray[vacuumID]['port']))
		    self.sendMessageOverSocket([self.vacuumArray[vacuumID]['host'],
						self.vacuumArray[vacuumID]['port']],
					       message)

		elif(self.sendMessage()) :
		    # The information held for this object is a
		    # pointer to the vacuums channel.

		    if(debug) :
			print("Router.sendString: {0}".format(vacuumID))
			self.vacuumArray[vacuumID].checkInfoType = True

		    #print("Router.sendString vacuum array: {0}  channel: {1}".format(self.vacuumArray,self.channel))
		    if((vacuumID > -1) and (vacuumID < len(self.vacuumArray)) and self.vacuumArray[vacuumID]) :
			if(debug):
			    print("Sending message to {0}".format(self.vacuumArray[vacuumID]))
			    
			self.vacuumArray[vacuumID].receiveXMLReportParseAndDecide(message)

		    else :
			print("Router.sendString bad vacuum id: {0}".format(vacuumID))



	elif (('host' in self.agents[destination]) and
	      ('port' in self.agents[destination])) :
	    # IP iformation is available for this
	    # agent. Send the information over the
	    # network.

	    if(debug) :
		print("SENDING TO {0} {1} ".format(self.agents[destination]['host'],self.agents[destination]['port']))
	    self.sendMessageOverSocket([self.agents[destination]['host'],self.agents[destination]['port']],
				       message)


	elif('parent' in self.agents[destination]):
		# This is a message for an agent that is not a vacuum.
		if(debug):
		    print("Sending to an agent directly: {0}".format(self.agents[destination]))

		if((self.agents[destination]['parent']) and (self.sendMessage())) :

		    # The information held for this object is a
		    # pointer to the agent's channel.

		    if(debug) :
			print("Send message directly to agent")
			self.agents[destination]['parent'].checkInfoType = True

		    self.agents[destination]['parent'].receiveXMLReportParseAndDecide(message)


	elif(debug) :
	    print("Router.sendMessage: Message not sent?")



