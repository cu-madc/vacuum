#!/usr/bin/python
#
#  worldSimulator.py
# 
#   Created on: 3 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       script to set up and run a simulation of the vacuum cleaners.
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


from Channel import Channel
from Commander import Commander
from Planner import Planner
from SensorArray import SensorArray
from GraphicalWorld import GraphicalWorld
from Vacuum import Vacuum
from Router import Router


def setIPInformationAgents(agent,interfaces) :
    for agentType, ipInfo in interfaces.iteritems():
	agent.setHostInformation(agentType,ipInfo[0],ipInfo[1],None)


def setIPInformationVacuum(agent,host,port,number) :
    agent.setHostInformation(Router.VACUUM,host,port,number)



# Set the host addressesd and ports for the different agents
agentInterfaces = {Router.SENSORARRAY:['10.0.1.10',1000],
		   Router.PLANNER    :['10.0.1.11',1001],
		   Router.COMMANDER  :['10.0.1.12',1002]}

vacummInterfaces = [ ['10.0.1.13',1003],
		     ['10.0.1.14',1004],
		     ['10.0.1.15',1005]]

# Set the rate and size for dirtfall
r = 1.8
s = 12.0

# Set the rate constant and size for rain
v         = .2
cloudsize = 20

# Create the world and get the gridsize
W = GraphicalWorld.spawnWorld(r,s,v,cloudsize);
#print("World channel: {0}".format(W.getChannel()))
N = W.getNumber() 

# create and set the sensor

accuracy = 0.4
sensor = SensorArray.spawnSensorArray(accuracy)   #SensorArray(accuracy)
#print("Sensor Channel: {0}".format(sensor.getChannel()))
W.setSensor(sensor)

# channel setup
chan = W.getChannel()   # TODO register the channel to the world


# create the commander and planner
plan=Planner.spawnPlanner(r*s/float(N*N),r,s,accuracy,N)
#print("Planner channel: {0}".format(plan.getChannel()))
W.setPlanner(plan)

command = Commander.spawnCommander()   # Commander(chan)
#print("Comander channel: {0}".format(command.getChannel()))

command.setRouterInformation(Router.WORLD,W.getChannel())
plan.setRouterInformation(Router.WORLD,W.getChannel())
sensor.setRouterInformation(Router.WORLD,W.getChannel())

#setIPInformationAgents(command,agentInterfaces)
#setIPInformationAgents(plan,agentInterfaces)
#setIPInformationAgents(sensor,agentInterfaces)

command.setRouterInformation(Router.COMMANDER,command.getChannel())
command.setRouterInformation(Router.PLANNER,plan.getChannel())
command.setRouterInformation(Router.SENSORARRAY,sensor.getChannel())
command.setRouterInformation(Router.WORLD,W.getChannel())

sensor.setRouterInformation(Router.COMMANDER,command.getChannel())
sensor.setRouterInformation(Router.PLANNER,plan.getChannel())
sensor.setRouterInformation(Router.SENSORARRAY,sensor.getChannel())
sensor.setRouterInformation(Router.WORLD,W.getChannel())

plan.setRouterInformation(Router.COMMANDER,command.getChannel())
plan.setRouterInformation(Router.PLANNER,plan.getChannel())
plan.setRouterInformation(Router.SENSORARRAY,sensor.getChannel())
plan.setRouterInformation(Router.WORLD,W.getChannel())

#chan.setDebug(True)
chan.setRouterChannel(Router.SENSORARRAY,sensor.getChannel())
chan.setRouterChannel(Router.COMMANDER,command.getChannel())
chan.setRouterChannel(Router.PLANNER,plan.getChannel())
chan.setRouterChannel(Router.WORLD,chan)

#command.getChannel().printChannelInformation("commander ")
#sensor.getChannel().printChannelInformation("sensor ")
#plan.getChannel().printChannelInformation("planner")
#W.getChannel().printChannelInformation("world")


# Create vacuums
numVacs=3
vacArray = []

#print("setting commander vacuums")
command.getChannel().setNumberVacuums(numVacs)
#print("setting planner vacuums")
plan.getChannel().setNumberVacuums(numVacs)
#print("setting sensor vacuums")
sensor.getChannel().setNumberVacuums(numVacs)


for i in range(numVacs) :
    #print("Initializing vacuum {0}".format(i))
    vacuum = Vacuum.spawnVacuum(i,0)
    #print("\n\nNew Vacuum: {0} - {1}, {2}".format(vacuum,vacuum.getChannel(),i))
    vacuum.getChannel().setNumberVacuums(numVacs)
    vacArray.append(vacuum)
    pos = vacuum.getPosition()
    #chan.addVacuum(vacuum,i,pos[0],pos[1])

    #setIPInformationVacuum(plan,   vacummInterfaces[i][0],vacummInterfaces[i][1],i)
    #setIPInformationVacuum(sensor, vacummInterfaces[i][0],vacummInterfaces[i][1],i)
    #setIPInformationVacuum(command,vacummInterfaces[i][0],vacummInterfaces[i][1],i)
    #setIPInformationAgents(vacuum, agentInterfaces)

    vacuum.setRouterInformation(Router.COMMANDER,command.getChannel())
    vacuum.setRouterInformation(Router.PLANNER,plan.getChannel())
    vacuum.setRouterInformation(Router.SENSORARRAY,sensor.getChannel())
    vacuum.setRouterInformation(Router.WORLD,W.getChannel())

    command.setVacuumRouterInformation(vacuum.getChannel(),i)
    sensor.setVacuumRouterInformation(vacuum.getChannel(),i)
    plan.setVacuumRouterInformation(vacuum.getChannel(),i)

    chan.getRouter().addVacuum(vacuum.getChannel(),i)
    vacuum.getChannel().sendPlannerVacuumMovedPosition(i,pos[0],pos[1])

    #print("going to add vacuum {0} to the world".format(i))
    W.addVacuum(vacuum)

#import sys
#sys.exit(0)



#W.printVacuumInfo(0)
#command.printRouterInformation("commander")
#sensor.printRouterInformation("sensor")
#plan.printRouterInformation("planner")
#W.printRouterInformation("world")



W.mainloop()
exit(0)

# testing (??)
S=vacArray[1].missions;
S1=vacArray[1].repairs;


H = []
R = []
W.draw()
skip = 10;
for i in range(10000) :
    W.inc()
    if(i%skip==0) :
       W.draw()
    H.append(sum(sum(W.A)))
    R.append(sum(W.Moisture>0))
    
print("Mean of H: {0}".format(mean(H)))

try:
    T_est=1000.0/(vacArray[1].missions-S)
except ZeroDivisionError:
    T_est = 0.0
    
S1=vacArray[1].repairs-S1;
S=vacArray[1].missions-S;


W.draw()
W.mainloop()


