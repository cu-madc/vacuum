#!/usr/bin/python
#
#  Commander.py
# 
#   Created on: 2 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the Commander object.
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


from numpy import *
from numpy.linalg import *

from World import World
from Channel import Channel
from Router import Router
from Agent import Agent


class Commander (Agent) :
    
    # command and control object

    def __init__(self,channel=None) : 
	Agent.__init__(self,Router.COMMANDER)
        self.setChannel(channel) # handle to planner


    def getReport(self,xPos,yPos,status,IDnum) :
        # receive a report from a vac and take action
        if (self.isWorking)  :
            # This commander is working
            
            if (status==2) :
                # just completed cleaning
                # update planner status that location is clean
                self.channel.sendVacuumReportFromCommander2Planner(xPos,yPos,IDnum)


            # send recommended order to the planner
            self.channel.sendRecommendOrderFromCommander2Planner(IDnum,xPos,yPos)


    def receiveReport(self,xord,yord,IDnum) :
        # pass order to vacuum and the planner
        self.channel.sendMoveOrderFromCommander2Vacuum(xord,yord,IDnum)
        self.channel.sendMoveOrderFromCommander2Planner(xord,yord,IDnum)


    # Static method that is used as a helper to make it easier to
    # create a commander object.
    @staticmethod
    def spawnCommander() :
	commander = Commander()
	channel = commander.initializeChannel()
	channel.setCommander(commander)
	return(commander)



if (__name__ =='__main__') :
    from Vacuum import Vacuum
    
    commander = Commander()
    commander = Commander.spawnCommander()
    commander.setHostInformation(Router.PLANNER,  "10.0.1.11",10001,None)
    commander.setHostInformation(Router.COMMANDER,"10.0.1.12",10002,None)
    commander.setHostname("10.0.1.12")
    commander.setPort(10002)

    commander.getChannel().setNumberVacuums(1)

    vacuum = Vacuum.spawnVacuum(0,0)
    vacuum.getChannel().setNumberVacuums(1)
    vacuum.setRouterChannel(Router.COMMANDER,commander.getChannel())
    commander.setVacuumRouterInformation(vacuum.getChannel(),0,0,0)

    commander.start()
    print("The commander is running")
    commander.join()
