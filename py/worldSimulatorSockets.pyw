#!/usr/bin/python
#
#  worldSimulatorSockets.py
# 
#   Created on: 3 Feb, 2011
#       Author: Skufka - adapted by black - adapted by PW
# 
#       script to set up and run a simulation of the vacuum cleaners
#       over network sockets.
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







# Set the host addressesd and ports for the different agents
agentInterfaces = {Router.SENSORARRAY:['10.0.1.10',10000],
		   Router.PLANNER    :['10.0.1.11',10001],
		   Router.COMMANDER  :['10.0.1.12',10002],
		   Router.WORLD      :['10.0.1.13',10003]}

vacummInterfaces = [ ['10.0.1.14',10004],
		     ['10.0.1.15',10005],
		     ['10.0.1.16',10006]]

# Set the other mission parameters
numVacs=3

# Set the parameters associated with the world.
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
chan = W.getChannel()   # TODO register the channel to the world



# create and set the sensor
accuracy = 0.4
sensor = SensorArray.spawnSensorArray(accuracy)   #SensorArray(accuracy)
#print("Sensor Channel: {0}".format(sensor.getChannel()))
sensor.setRouterChannel(Router.WORLD,W.getChannel())
W.setSensor(sensor)
sensor.setIPInformation(agentInterfaces)
sensor.getChannel().setNumberVacuums(numVacs)



# create the planner
plan=Planner.spawnPlanner(r*s/float(N*N),r,s,accuracy,N)
#print("Planner channel: {0}".format(plan.getChannel()))
plan.setRouterChannel(Router.WORLD,W.getChannel())
W.setPlanner(plan)
plan.setIPInformation(agentInterfaces)
plan.getChannel().setNumberVacuums(numVacs)



# create the commander
command = Commander.spawnCommander()   # Commander(chan)
#print("Comander channel: {0}".format(command.getChannel()))
command.setRouterChannel(Router.WORLD,W.getChannel())
command.setIPInformation(agentInterfaces)
command.getChannel().setNumberVacuums(numVacs)




# Set the channel that links each agent with the world. The world
# sends information to the agents directly rather than use the
# network.
#chan.setDebug(True)
chan.setRouterChannel(Router.SENSORARRAY,sensor.getChannel())
chan.setRouterChannel(Router.COMMANDER,command.getChannel())
chan.setRouterChannel(Router.PLANNER,plan.getChannel())
chan.setRouterChannel(Router.WORLD,chan)



# Create vacuums
vacArray = []
for i in range(numVacs) :
    print("Initializing vacuum {0}".format(i))
    vacuum = Vacuum.spawnVacuum(i,0)
    print("New Vacuum: {0} - {1}, {2}".format(vacuum,id(vacuum),i))
    vacuum.getChannel().setNumberVacuums(numVacs)
    vacArray.append(vacuum)
    pos = vacuum.getPosition()
    #chan.addVacuum(vacuum,i,pos[0],pos[1])
    plan.setVacuumLocation(i,pos[0],pos[1])

    plan.setHostInformation(Router.VACUUM,vacummInterfaces[i][0],vacummInterfaces[i][1],i)
    sensor.setHostInformation(Router.VACUUM,vacummInterfaces[i][0],vacummInterfaces[i][1],i)
    command.setHostInformation(Router.VACUUM,vacummInterfaces[i][0],vacummInterfaces[i][1],i)
    
    vacuum.setIPInformation(agentInterfaces)
    vacuum.setRouterChannel(Router.WORLD,W.getChannel())
    chan.getRouter().addVacuum(vacuum.getChannel(),i)
    chan.addVacuum(vacuum,i,0,0)
    vacuum.getChannel().sendPlannerVacuumMovedPosition(i,pos[0],pos[1])

    #print("going to add vacuum {0} to the world".format(i))
    W.addVacuum(vacuum)
    print("Setting vacuum {0} - {1}:{2}".format(i,vacummInterfaces[i][0],vacummInterfaces[i][1]))
    vacuum.setHostname(vacummInterfaces[i][0])
    vacuum.setPort(vacummInterfaces[i][1])
    vacuum.start()

#command.printRouterInformation("commander ")
#sensor.printRouterInformation("sensor ")
#plan.printRouterInformation("planner")
#W.getChannel().printChannelInformation("world")


#import sys
#sys.exit(0)



#W.printVacuumInfo(0)
#command.printRouterInformation("commander")
#sensor.printRouterInformation("sensor")
#plan.printRouterInformation("planner")
#W.printRouterInformation("world")


command.setHostname(agentInterfaces[Router.COMMANDER][0])
command.setPort(agentInterfaces[Router.COMMANDER][1])
command.start()

sensor.setHostname(agentInterfaces[Router.SENSORARRAY][0])
sensor.setPort(agentInterfaces[Router.SENSORARRAY][1])
sensor.start()


plan.setHostname(agentInterfaces[Router.PLANNER][0])
plan.setPort(agentInterfaces[Router.PLANNER][1])
plan.start()

W.setHostname(agentInterfaces[Router.WORLD][0])
W.setPort(agentInterfaces[Router.WORLD][1])
W.mainloop()
