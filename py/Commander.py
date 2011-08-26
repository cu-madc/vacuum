#!/usr/bin/python
#
#  Commander.py
# 
#   Created on: 2 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the Commander object.
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


from numpy import *
from numpy.linalg import *

from World import World
from Channel import Channel
from Router import Router
from Agent import Agent
from XML.XMLMessageForAgent import XMLMessageForAgent


class Commander (Agent) :
    
    # command and control object

    def __init__(self,channel=None) : 
	Agent.__init__(self,Router.COMMANDER)
        self.setChannel(channel) # handle to planner


    def getReport(self,xPos,yPos,status,IDnum) :
        # receive a report from a vac and take action
	#print("commander get report {0} {1} {2} {3}".format(xPos,yPos,status,IDnum))
        if (self.isWorking)  :
            # This commander is working
            
            if (status==2) :
                # just completed cleaning
                # update planner status that location is clean
                self.sendVacuumReportFromCommander2Planner(xPos,yPos,IDnum)


            # send recommended order to the planner
            self.sendRecommendOrderFromCommander2Planner(IDnum,xPos,yPos)


    def receiveReport(self,xord,yord,IDnum) :
        # pass order to vacuum and the planner
	#print("commander receive report {0} {1} {2}".format(xord,yord,IDnum))
        self.sendMoveOrderFromCommander2Vacuum(xord,yord,IDnum)
        self.sendMoveOrderFromCommander2Planner(xord,yord,IDnum)





    # Method to handle an incoming message and determine what to do
    def handleMessage(self,type,passedInformation) :
	#print("Commander.handleMessage: {0} - {1}".format(type,passedInformation))

	if (type=="Vacuum Recommendation") :
	    self.receiveReport(int(passedInformation['xPos']),
			       int(passedInformation['yPos']),
			       int(passedInformation['vacuumID']))


	elif(type=="Get Report") :
	    self.getReport(int(passedInformation['xPos']),
			   int(passedInformation['yPos']),
			   int(passedInformation['status']),
			   int(passedInformation['vacuumID']))




    # Static method that is used as a helper to make it easier to
    # create a commander object.
    @staticmethod
    def spawnCommander() :
	commander = Commander()
	channel = commander.initializeChannel()
	channel.addAgent(commander,Agent.COMMANDER,0,False)
	return(commander)



    ## sendVacuumReportFromCommander2Planner
    #
    # Routine that takes a report from the commander that identifies a
    # particular vacuum and converts it into XML and passes it along
    # to the planner so it will know where the vacuum was sent.
    #
    def sendVacuumReportFromCommander2Planner(self,xPos,yPos,IDnum) :
	#print("Commander.sendVacuumReportFromCommander2Planner - sending information.")
        network = XMLMessageForAgent()
	network.createRootNode(False)
	network.createObjectClassElements(Agent.PLANNER,"Vacuum Orders")
	network.addPosition(xPos,yPos)
	network.vacuumID(IDnum)
	#print(self.xml2Char())

	self.channel.sendString(Router.PLANNER,network.xml2Char())


    ## sendRecommendOrderFromCommander2Planner
    #
    # Routine that takes a recommendation order from the commander
    # that identifies a particular vacuum and converts it into XML and
    # passes the XML tree on to the planner.
    def sendRecommendOrderFromCommander2Planner(self,vacuumID,xPos,yPos) :
	#print("Commander.sendRecommendOrderFromCommander2Planner - sending information.")
	orders = XMLMessageForAgent()
	orders.createRootNode(False)
	orders.createObjectClassElements(Agent.PLANNER,"Vacuum Recommendation")
	orders.addPosition(xPos,yPos)
	orders.vacuumID(vacuumID)
	#print(self.xml2Char())

	self.channel.sendString(Router.PLANNER,orders.xml2Char())


    ## sendMoveOrderFromCommander2Vacuum
    #
    # Routine that takes an order from the commander and converts it
    # into XML and passed the XML to the vacuum.
    def sendMoveOrderFromCommander2Vacuum(self,xPos,yPos,vacuumID) :
	#print("Commander.sendMoveOrderFromCommander2Vacuum - sending information.")
	orders = XMLMessageForAgent()
	orders.createRootNode(False)
	orders.createObjectClassElements(Agent.VACUUM,"Move Order")
	orders.addPosition(xPos,yPos)
	orders.vacuumID(vacuumID)
	#print(self.xml2Char())


	self.channel.sendString(Router.VACUUM,orders.xml2Char(),vacuumID)



    ## sendMoveOrderFromCommander2Planner
    #
    # Routine to take a message from the commander that is an order to
    # move a vacuum and relay it to the planner.
    def sendMoveOrderFromCommander2Planner(self,xPos,yPos,IDnum) :
	#print("Commander.sendMoveOrderFromCommander2Planner - sending information.")
	report = XMLMessageForAgent()
	report.createRootNode(False)
	report.createObjectClassElements(Agent.PLANNER,"Move Order")
	report.addPosition(xPos,yPos)
	report.vacuumID(IDnum)
	#print(self.xml2Char())

	self.channel.sendString(Router.PLANNER,report.xml2Char(),IDnum)






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

    # Set the other mission parameters
    numVacs=len(vacummInterfaces)

    # Set the parameters associated with the world.
    # Set the rate and size for dirtfall
    r = 1.8
    s = 12.0

    # Set the rate constant and size for rain
    v         = .2
    cloudsize = 20


    # create and set the commander
    command = Commander.spawnCommander()   
    #print("Comander channel: {0}".format(command.getChannel()))
    command.setIPInformation(agentInterfaces)              # tell the agent's ip info to the commander
    command.getChannel().setNumberVacuums(numVacs)         # tell the commander  how many vac's to use


    
    # Create vacuums
    vacArray = []
    for i in range(numVacs) :
	pos = [0,0]                                        # get the default pos.

	# Let the commander know about this vacuum including it's ip information.
	command.setHostInformation(Router.VACUUM,vacummInterfaces[i][0],vacummInterfaces[i][1],i)



    # Set the ip info for the commander and start it in its own process
    command.setHostname(agentInterfaces[Router.COMMANDER][0])
    command.setPort(agentInterfaces[Router.COMMANDER][1])
    command.run()
