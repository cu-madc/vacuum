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




# Set the rate and size for dirtfall
r = 0.5
s = 10.0

# Set the rate constant and size for rain
v         = .1
cloudsize = 20

# Create the world and get the gridsize
W = GraphicalWorld.spawnWorld(r,s,v,cloudsize);
N = W.getNumber()
chan = W.getChannel()


# create and set the sensor
accuracy = 0.4
sensor = SensorArray.spawnSensorArray(accuracy)
W.setSensor(sensor)


# create the planner
plan=Planner.spawnPlanner(r*s/float(N*N),r,s,accuracy,N)
W.setPlanner(plan)


# create the commander
command = Commander.spawnCommander()  
#W.setCommander(command)


# Create the vacuums
numVacs=3
vacArray = []
for i in range(numVacs) :
    vacuum = Vacuum.spawnVacuum(i,0)               # Create the next vacuum 
    vacArray.append(vacuum)                        # Add it to the list that I am keeping
    W.addVacuum(vacuum)                            # Add it to the world's list  
    vacuum.getChannel().setNumberVacuums(numVacs)  # Let the vacuum know how many others there will be

    pos = vacuum.getPosition()                        # Get this one's position.
    chan.getRouter().addVacuum(vacuum.getChannel(),i) # Add the vac's channel to the world's list 
    chan.addVacuum(vacuum,i,pos[0],pos[1],False)      # Let the channel know its position.

    # Let the planner know the relevant information about the vacuum.
    plan.setVacuumLocation(i,pos[0],pos[1])
    plan.setVacuumRouterInformation(vacuum.getChannel(),i,pos[0],pos[1])

    # Let the commander know the relevant information about the vacuum.
    command.setVacuumRouterInformation(vacuum.getChannel(),i,pos[0],pos[1])

    # Let the sensor know the relevant information about the vacuum.
    sensor.setVacuumRouterInformation(vacuum.getChannel(),i,pos[0],pos[1])

    # Let the Vacuum know the relevant information about all of the other agents.
    vacuum.setRouterChannel(Router.WORLD,W.getChannel())
    vacuum.setRouterChannel(Router.COMMANDER,command.getChannel())
    vacuum.setRouterChannel(Router.PLANNER,plan.getChannel())
    vacuum.setRouterChannel(Router.SENSORARRAY,sensor.getChannel())


    #vacuum.registerWorld(W,command)


# Set the channel pointers for the sensor array
sensor.setRouterChannel(Router.WORLD,W.getChannel())
sensor.setRouterChannel(Router.COMMANDER,command.getChannel())
sensor.setRouterChannel(Router.PLANNER,plan.getChannel())

# Set the channel pointers for the planner
plan.setRouterChannel(Router.WORLD,W.getChannel())
plan.setRouterChannel(Router.COMMANDER,command.getChannel())
plan.setRouterChannel(Router.SENSORARRAY,sensor.getChannel())

# Set the channel pointers for the commander
command.setRouterChannel(Router.WORLD,W.getChannel())
command.setRouterChannel(Router.PLANNER,plan.getChannel())
command.setRouterChannel(Router.SENSORARRAY,sensor.getChannel())

# Set the channel pointers for the world
W.setRouterChannel(Router.SENSORARRAY,sensor.getChannel())
W.setRouterChannel(Router.PLANNER,plan.getChannel())
W.setRouterChannel(Router.COMMANDER,command.getChannel())


# Create the window and enter the event polling loop for the window manager.
H = []
R = []
W.draw()
W.mainloop()


