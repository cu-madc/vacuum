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

class Commander :
    
    # command and control object

    def __init__(self,plan=None) : 

        self.chanPlan = 0   # handle from channel to planner
        self.chanVac = []   # list  of handles to assigned vacuums

        self.setWorking(True)
        self.setChannel(plan)         # handle to planner


    def setWorking(self,value) :
        self.isWorking = value


    def getWorking(self) :
        return(self.isWorking)

    def addVacuum(self,vacuum) :
        self.chanVac.append(vacuum)


    def getChannel(self) :
        return(self.channel)

    def setChannel(self,value) :
        self.channel = value


    def registerChannels(self,chanPlan,vacArray) :
        # chanVac is an array, one element for each vac
        self.chanPlan=chanPlan;
        for vacuum in vacArray :
            self.addVacuum(vacuum.getChannel())
    



    def getReport(self,xPos,yPos,status,IDnum) :
        # receive a report from a vac and take action
        if (self.isWorking)  :
            # This commander is working
            
            
            if (status==2) :
                # just completed cleaning
                # update planner status that location is clean
                self.channel.sendVacuumReportFromCommander2Planner(xPos,yPos)


            # get recommended order from the planner
            # returns empty if comms problem
            xord = None
            xord = 4
            yord = 2
            
            self.channel.sendRecommendOrderFromCommander2Planner(IDnum)


    def receiveReport(self,xord,yord) :
        #[xord,yord]=self.chanPlan.sendReceive(self.planner,self.planner.channel,@recommendOrder,aVac); 
        #if (len(xord)==0) :
        #   # retry
        #    [xord,yord]=self.chanPlan.sendReceive(self.planner,self.planner.channel,@recommendOrder,aVac); 
        #end
            
            
        # pass order to vacuum
        self.channel.sendMoveOrderFromCommander2Vacuum(xord,yord,IDnum)
        ##aVac.moveord(xord,yord);
            
        #tell planner that vacuum has been ordered to new location
        if xord :
            self.channel.sendMoveOrderFromCommander2Planner(xord,yord,IDnum)



if (__name__ =='__main__') :
    commander = Commander()
