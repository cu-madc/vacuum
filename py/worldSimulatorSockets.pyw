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

import sys
from datetime import date
import ConfigParser

from numpy import *
from numpy.linalg import *


from Channel import Channel
from Commander import Commander
from Planner import Planner
from SensorArray import SensorArray
from World import World
from Vacuum import Vacuum
from Router import Router




# Handle the command line arguments
# The assumed form for the command line is the following
#
# ./worldSimulatorSocket.pyw worldOutput.txt vacuumOutput.txt
#
#  where the first argument is the name of the output file for the
#  world data, and the second argument is the name of the output file
#  for the vacuum data.
#
theDate = date.today()
worldOutputFileName  = "./worldOutput-" + \
    str(theDate.year) + "-" + str(theDate.month) + "-" + str(theDate.day) + ".txt" 
vacuumOutputFileName = "./vacuumOutput-" + \
    str(theDate.year) + "-" + str(theDate.month) + "-" + str(theDate.day) + ".txt"

if(len(sys.argv) >= 4) :
    # The name of the vacuum data file is specified.
    vacuumOutputFileName = sys.argv[3]

if(len(sys.argv) >= 3) :
    # The name of the world data file is specified
    worldOutputFileName = sys.argv[2]

if(len(sys.argv) >= 2) :
    # The name of the config file is specified
    configFileName = sys.argv[1]
else:
    configFileName = False

#print(worldOutputFileName)
#print(vacuumOutputFileName)


# Set the host addresses and ports for the different agents
#agentInterfaces = {Router.SENSORARRAY:['10.0.1.10',10000],
#		   Router.PLANNER    :['10.0.1.11',10001],
#		   Router.COMMANDER  :['10.0.1.12',10002],
#		   Router.WORLD      :['10.0.1.13',10003]}

if(configFileName == False) :
    worldAgentInterfaces = {Router.SENSORARRAY:['10.0.1.10',10000],
                            Router.PLANNER    :['10.0.1.11',10001],
                            Router.COMMANDER  :['10.0.1.12',10002],
                            Router.WORLD      :['10.0.1.13',10003]}
    sensorAgentInterfaces = {Router.SENSORARRAY:['10.0.1.10',10000],
                             Router.PLANNER    :['10.0.1.11',10001],
                             Router.COMMANDER  :['10.0.1.12',10002],
                             Router.WORLD      :['10.0.1.13',10003]}
    plannerAgentInterfaces = {Router.SENSORARRAY:['10.0.1.10',10000],
                              Router.PLANNER    :['10.0.1.11',10001],
                              Router.COMMANDER  :['10.0.1.12',10002],
                              Router.WORLD      :['10.0.1.13',10003]}
    commanderAgentInterfaces = {Router.SENSORARRAY:['10.0.1.10',10000],
                                Router.PLANNER    :['10.0.1.11',10001],
                                Router.COMMANDER  :['10.0.1.12',10002],
                                Router.WORLD      :['10.0.1.13',10003]}
    vacuumAgentInterfaces = {Router.WORLD      :['10.0.1.13',10003]}
    commander2Vacuums = [ ['10.0.1.14',10004],
                          ['10.0.1.15',10005],
                          ['10.0.1.16',10006]]
    vacuums2Commander = [ ['10.0.1.11',10001],
                          ['10.0.1.11',10001],
                          ['10.0.1.11',10001]]
else:
    config = ConfigParser.SafeConfigParser()
    config.read(configFileName)
    worldAgentInterfaces = {Router.SENSORARRAY:[config.get('world','sensorAddress'),config.getint('world','sensorPort')],
                            Router.PLANNER    :[config.get('world','plannerAddress'),config.getint('world','plannerPort')],
                            Router.COMMANDER  :[config.get('world','commanderAddress'),config.getint('world','commanderPort')],
                            Router.WORLD      :[config.get('world','worldAddress'),config.getint('world','worldPort')]}
    sensorAgentInterfaces = {Router.SENSORARRAY:[config.get('sensor','sensorAddress'),config.getint('sensor','sensorPort')],
                             Router.PLANNER    :[config.get('sensor','plannerAddress'),config.getint('sensor','plannerPort')],
                             Router.COMMANDER  :[config.get('sensor','commanderAddress'),config.getint('sensor','commanderPort')],
                             Router.WORLD      :[config.get('sensor','worldAddress'),config.getint('sensor','worldPort')]}
    plannerAgentInterfaces = {Router.SENSORARRAY:[config.get('planner','sensorAddress'),config.getint('planner','sensorPort')],
                              Router.PLANNER    :[config.get('planner','plannerAddress'),config.getint('planner','plannerPort')],
                              Router.COMMANDER  :[config.get('planner','commanderAddress'),config.getint('planner','commanderPort')],
                              Router.WORLD      :[config.get('planner','worldAddress'),config.getint('planner','worldPort')]}
    commanderAgentInterfaces = {Router.SENSORARRAY:[config.get('commander','sensorAddress'),config.getint('commander','sensorPort')],
                                Router.PLANNER    :[config.get('commander','plannerAddress'),config.getint('commander','plannerPort')],
                                Router.COMMANDER  :[config.get('commander','commanderAddress'),config.getint('commander','commanderPort')],
                                Router.WORLD      :[config.get('commander','worldAddress'),config.getint('commander','worldPort')]}
    vacuumAgentInterfaces = {Router.WORLD    :[config.get('vacuums','worldAddress'),config.getint('vacuums','worldPort')]}    
    commander2Vacuums = [ [config.get('commander2vacuums','vacuum1Address'),config.getint('commander2vacuums','vacuum1Port')],
                          [config.get('commander2vacuums','vacuum2Address'),config.getint('commander2vacuums','vacuum2Port')],
                          [config.get('commander2vacuums','vacuum3Address'),config.getint('commander2vacuums','vacuum3Port')]]
    vacuums2Commander = [ [config.get('vacuums2commander','vacuum1toCommanderAddress'),config.getint('vacuums2commander','vacuum1toCommanderPort')],
                          [config.get('vacuums2commander','vacuum2toCommanderAddress'),config.getint('vacuums2commander','vacuum2toCommanderPort')],
                          [config.get('vacuums2commander','vacuum3toCommanderAddress'),config.getint('vacuums2commander','vacuum3toCommanderPort')]]

# Set the host addresses and ports for the different vacuums 
#vacummInterfaces = [ ['10.0.1.14',10004],
#		     ['10.0.1.15',10005],
#		     ['10.0.1.16',10006]]


# Set the other mission parameters
numVacs=len(commander2Vacuums)

# Set the parameters associated with the world.
# Set the rate and size for dirtfall
r = 1.8
s = 12.0

# Set the rate constant and size for rain
v         = .2
cloudsize = 20


# Create the world and get the gridsize
W = World.spawnWorld(r,s,v,cloudsize);
#print("World channel: {0}".format(W.getChannel()))
N = W.getNumber()
chan = W.getChannel()                     # Get the world's channel object
W.getChannel().setNumberVacuums(numVacs)  # Let the world's channel know how many vac's to use
W.setIPInformation(worldAgentInterfaces)  # Let the world know all the ip info about the agents.

# Set the world up to record data
W.setVacuumFileName(vacuumOutputFileName)
W.setWorldFileName(worldOutputFileName)
W.setDataCollection(True)
W.setDataCollectionFrequency(1)



# create and set the sensor
accuracy = 0.4
sensor = SensorArray.spawnSensorArray(accuracy) 
#print("Sensor Channel: {0}".format(sensor.getChannel()))
sensor.setRouterChannel(Router.WORLD,W.getChannel())   # inform the sensor about the world's channel
W.setSensor(sensor)                                    # tell the world what its sensor is
sensor.setIPInformation(sensorAgentInterfaces)         # set the agent's ip info on the sensor.
sensor.getChannel().setNumberVacuums(numVacs)          # tell the sensor how many vac's to use
sensor.setQueueUse(True)                               # tell the sensor to use the queue's
                                                       # information to get input from the world
						       # as to what is happening.



# create and set the planner
plan=Planner.spawnPlanner(r*s/float(N*N),r,s,accuracy,N)
#print("Planner channel: {0}".format(plan.getChannel()))
plan.setRouterChannel(Router.WORLD,W.getChannel())     # inform the planner about the world's channel
W.setPlanner(plan)                                     # tell the world what its planner is
plan.setIPInformation(plannerAgentInterfaces)          # tell the agent's ip info to the planner
plan.getChannel().setNumberVacuums(numVacs)            # tell the planner how many vac's to use
plan.setQueueUse(True)                                 # tell the planner to use the queue's
                                                       # information to get input from the world
						       # as to what is happening.



# create and set the commander
command = Commander.spawnCommander()   
#print("Comander channel: {0}".format(command.getChannel()))
command.setRouterChannel(Router.WORLD,W.getChannel())  # inform the commander about the world's channel
command.setIPInformation(commanderAgentInterfaces)     # tell the agent's ip info to the commander
command.getChannel().setNumberVacuums(numVacs)         # tell the commander  how many vac's to use




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
    vacuum = Vacuum.spawnVacuum(i,0)
    #print("New Vacuum: {0} - {1}, {2}".format(vacuum,id(vacuum),i))
    vacuum.getChannel().setNumberVacuums(numVacs)      # Tell the vacuum how many other
                                                       # vacuums there will be
    vacuum.setQueueUse(True)                           # Tell the vacuum to get info
                                                       # from the world through the queue.
    vacArray.append(vacuum)                            # Append this to the vac's kept track of here.
    pos = vacuum.getPosition()                         # get the default pos.
    chan.getRouter().addVacuum(vacuum.getChannel(),i)  # Tell the world where the vacuum starts.

    W.addVacuum(vacuum,False)                          # Add the vacuum to the world's list of vac's


    chan.addVacuum(vacuum,i,pos[0],pos[1],False)       # Let the world's channel know about this vac

    # Let the planner know about this vacuum including it's ip information.
    plan.setVacuumLocation(i,pos[0],pos[1])        
    #PW#plan.setHostInformation(Router.VACUUM,vacummInterfaces[i][0],vacummInterfaces[i][1],i)

    # Let the sensor know about this vacuum including it's ip information.
    #PW#sensor.setHostInformation(Router.VACUUM,vacummInterfaces[i][0],vacummInterfaces[i][1],i)

    # Let the commander know about this vacuum including it's ip information.
    command.setHostInformation(Router.VACUUM,commander2Vacuums[i][0],commander2Vacuums[i][1],i)

    # Let the world know about this vacuum including it's ip information.
    # (uncomment out this line if it is not running in the current process. ex: on an other machine.)
    #W.setHostInformation(Router.VACUUM,vacummInterfaces[i][0],vacummInterfaces[i][1],i)

    # Let this vacuum know about the ip information about all of the other agents and the world.
    vacuum.setIPInformation(vacuumAgentInterfaces)
    vacuum.setRouterChannel(Router.WORLD,W.getChannel())
    vacuum.setHostInformation(Router.COMMANDER,vacuums2Commander[i][0],vacuums2Commander[i][1],i)

    # Set the ip information for this particular vacuum.
    #print("Setting vacuum {0} - {1}:{2}".format(i,vacummInterfaces[i][0],vacummInterfaces[i][1]))
    vacuum.setHostname(commander2Vacuums[i][0])
    vacuum.setPort(commander2Vacuums[i][1])

    # If you want the vacuum to run in its own process then uncomment out the next line (.start)
    #vacuum.start()

    # If you want the vacuum to run in this process with a direct
    # connection to the world then uncomment out the next line.
    vacuum.getChannel().getRouter().createAndInitializeSocket()


# Print out some debug information.
#command.printRouterInformation("commander ")
#sensor.printRouterInformation("sensor ")
#plan.printRouterInformation("planner")
#W.getChannel().printChannelInformation("world")


# Set the ip info for the commander and start it in its own process
command.setHostname(agentInterfaces[Router.COMMANDER][0])
command.setPort(agentInterfaces[Router.COMMANDER][1])
command.start()

# Set the ip info for the sensor and start it in its own process
sensor.setHostname(agentInterfaces[Router.SENSORARRAY][0])
sensor.setPort(agentInterfaces[Router.SENSORARRAY][1])
sensor.start()

# Set the ip info for the planner and start it in its own process
plan.setHostname(agentInterfaces[Router.PLANNER][0])
plan.setPort(agentInterfaces[Router.PLANNER][1])
plan.start()

# Set the ip info for the world and start up the graphical interface
W.setHostname(agentInterfaces[Router.WORLD][0])
W.setPort(agentInterfaces[Router.WORLD][1])
W.getChannel().getRouter().createAndInitializeSocket()



W.stepInTime(20,0,1)
W.quit()
