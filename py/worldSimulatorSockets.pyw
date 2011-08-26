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


from numpy import *
from numpy.linalg import *


from Channel import Channel
from Commander import Commander
from Planner import Planner
from SensorArray import SensorArray
from World import World
from Vacuum import Vacuum
from Router import Router
from DataCollector import DataCollector

from MissionUtilities import MissionUtilities



# Handle the command line arguments
# The assumed form for the command line is the following
#
# ./worldSimulatorSocket.pyw --worldData=worldOutput-#DATESTAMP#.csv --vacuumData=vacuumOutput-#DATESTAMP#.csv --ipInfo=ipInfo.dat
#
#

DEBUG = False


# Set the host addresses and ports for the different vacuums 
vacuumInterfaces = [ ['10.0.1.15',10004],
		     ['10.0.1.16',10005],
		     ['10.0.1.17',10006]]

# Set the host addresses and ports for the different agents
agentInterfaces = {Router.SENSORARRAY  :['10.0.1.10',10000],
		   Router.PLANNER      :['10.0.1.11',10001],
		   Router.COMMANDER    :['10.0.1.12',10002],
		   Router.WORLD        :['10.0.1.13',10003],
		   Router.DATACOLLECTOR:['10.0.1.14',10004],
		   Router.VACUUM       : vacuumInterfaces}


# Create the parser to help fix the default ip values and parse the
# configuration files.
utilityHelper = MissionUtilities()
utilityHelper.setDefaultIPInformation(agentInterfaces,Router.SENSORARRAY)
utilityHelper.setDefaultIPInformation(agentInterfaces,Router.PLANNER)
utilityHelper.setDefaultIPInformation(agentInterfaces,Router.COMMANDER)
utilityHelper.setDefaultIPInformation(agentInterfaces,Router.WORLD)
utilityHelper.setDefaultIPInformation(agentInterfaces,Router.DATACOLLECTOR)

utilityHelper.setDefaultIPInformation(agentInterfaces,Router.VACUUM,0)
utilityHelper.setDefaultIPInformation(agentInterfaces,Router.VACUUM,1)
utilityHelper.setDefaultIPInformation(agentInterfaces,Router.VACUUM,2)


# Go through the command line options and act on them.
utilityHelper.parseCommandLine()


# Defing the ip information that will be used for each agent.
sensorInterfaces        = utilityHelper.getAgentInformation(Router.SENSORARRAY)
plannerInterfaces       = utilityHelper.getAgentInformation(Router.PLANNER)
commanderInterfaces     = utilityHelper.getAgentInformation(Router.COMMANDER)
worldInterfaces         = utilityHelper.getAgentInformation(Router.WORLD)
dataCollectorInterfaces = utilityHelper.getAgentInformation(Router.DATACOLLECTOR)
vacuumInterfaceList     = [utilityHelper.getAgentInformation(Router.VACUUM,0),
			   utilityHelper.getAgentInformation(Router.VACUUM,1),
			   utilityHelper.getAgentInformation(Router.VACUUM,2)]


if(DEBUG) :
    # Print out the ip information to see if it is correct
    print("Sensor:        {0}".format(sensorInterfaces))
    print("Planner:       {0}".format(plannerInterfaces))
    print("Commander:     {0}".format(commanderInterfaces))
    print("World:         {0}".format(worldInterfaces))
    print("data collector:{0}".format(dataCollectorInterfaces))

    print("vacuum 0:      {0}".format(vacuumInterfaceList[0]))
    print("vacuum 1:      {0}".format(vacuumInterfaceList[1]))
    print("vacuum 2:      {0}".format(vacuumInterfaceList[2]))





# Set the other mission parameters
numVacs=len(vacuumInterfaces)

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
W.setIPInformation(worldInterfaces)       # Let the world know all the ip info about the agents.

# Set up the world to collect data. This is necessary because the
# world controls the information that is sent out to the vacuums.
W.setDataCollection(True)
W.setDataCollectionFrequency(1)


# Create the data collector and set it up to record data
dataCollector = DataCollector.spawnDataCollector()            # create the data collector
dataCollector.setVacuumFileName(                              # Set the relevant file names
    utilityHelper.getvacuumOutputFileName())                  # to be used by the data collector.
dataCollector.setWorldFileName(
    utilityHelper.getWorldOutputFileName())
dataCollector.setIPInformation(dataCollectorInterfaces)       # give it all the relevant ip info.
dataCollector.setRouterChannel(Router.WORLD,W.getChannel())   # inform the sensor about the
                                                              # world's channel
dataCollector.setDataCollection(True)                         # Make sure the data collector
                                                              # knows it has to receive the data.



# create and set the sensor
accuracy = 0.4
sensor = SensorArray.spawnSensorArray(accuracy) 
#print("Sensor Channel: {0}".format(sensor.getChannel()))
sensor.setRouterChannel(Router.WORLD,W.getChannel())   # inform the sensor about the world's channel
W.setSensor(sensor)                                    # tell the world what its sensor is
sensor.setIPInformation(sensorInterfaces)              # set the agent's ip info on the sensor.
sensor.getChannel().setNumberVacuums(numVacs)          # tell the sensor how many vac's to use
sensor.setQueueUse(True)                               # tell the sensor to use the queue's
                                                       # information to get input from the world
						       # as to what is happening.



# create and set the planner
plan=Planner.spawnPlanner(r*s/float(N*N),r,s,accuracy,N)
#print("Planner channel: {0}".format(plan.getChannel()))
plan.setRouterChannel(Router.WORLD,W.getChannel())     # inform the planner about the world's channel
W.setPlanner(plan)                                     # tell the world what its planner is
plan.setIPInformation(plannerInterfaces)               # tell the agent's ip info to the planner
plan.getChannel().setNumberVacuums(numVacs)            # tell the planner how many vac's to use
plan.setQueueUse(True)                                 # tell the planner to use the queue's
                                                       # information to get input from the world
						       # as to what is happening.



# create and set the commander
command = Commander.spawnCommander()   
#print("Comander channel: {0}".format(command.getChannel()))
command.setRouterChannel(Router.WORLD,W.getChannel())  # inform the commander about the world's channel
command.setIPInformation(commanderInterfaces)          # tell the agent's ip info to the commander
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

    # QUESTION: Are these calls to the other agents necessary? This
    # should be set above in the calls to the ip setting
    # routines. (???)
    
    # Let the planner know about this vacuum including it's ip information.
    plan.setVacuumLocation(i,0,0)
    if(DEBUG) :
	print("Vacuum {2} Planner ip info: {0}-{1}".format(
	    vacuumInterfaceList[i][Router.PLANNER][0],
	    vacuumInterfaceList[i][Router.PLANNER][1],i))
    plan.setHostInformation(Router.VACUUM,
			    vacuumInterfaceList[i][Router.PLANNER][0],
			    vacuumInterfaceList[i][Router.PLANNER][1],i)
    

    # Let the sensor know about this vacuum including it's ip information.
    if(DEBUG) :
	print("Vacuum {2} Sensor ip info: {0}-{1}".format(
	    vacuumInterfaceList[i][Router.SENSORARRAY][0],
	    vacuumInterfaceList[i][Router.SENSORARRAY][1],i))
    sensor.setHostInformation(Router.VACUUM,
			      vacuumInterfaceList[i][Router.SENSORARRAY][0],
			      vacuumInterfaceList[i][Router.SENSORARRAY][1],i)


    # Let the commander know about this vacuum including it's ip information.
    if(DEBUG) :
	print("Vacuum {2} Commander ip info: {0}-{1}".format(
	    vacuumInterfaceList[i][Router.COMMANDER][0],
	    vacuumInterfaceList[i][Router.COMMANDER][1],i))
    command.setHostInformation(Router.VACUUM,
			       vacuumInterfaceList[i][Router.COMMANDER][0],
			       vacuumInterfaceList[i][Router.COMMANDER][1],i)


    # Let the world know about this vacuum including it's ip information.
    # (uncomment out this line if it is not running in the current process. ex: on an other machine.)
    #W.setHostInformation(Router.VACUUM,vacuumInterfaces[i][Router.WORLD][0],vacuumInterfaces[i][Router.WORLD][1],i)

    # Let this vacuum know about the ip information about all of the other agents and the world.
    vacuum.setIPInformation(vacuumInterfaceList[i])
    vacuum.setRouterChannel(Router.WORLD,W.getChannel())
    vacuum.setRouterChannel(Router.DATACOLLECTOR,dataCollector.getChannel())

    # Let the data collector know about this vacuum's channel information.
    dataCollector.setVacuumRouterInformation(vacuum.getChannel(),i)


    # Set the ip information for this particular vacuum.
    if(DEBUG) :
	print("Setting vacuum {0} - {1}:{2}".format(
	    i,vacuumInterfaceList[i][Router.VACUUM][i][0],
	    vacuumInterfaceList[i][Router.VACUUM][i][1]))
    vacuum.setHostname(vacuumInterfaceList[i][Router.VACUUM][i][0])
    vacuum.setPort(vacuumInterfaceList[i][Router.VACUUM][i][1])

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
command.setHostname(commanderInterfaces[Router.COMMANDER][0])
command.setPort(commanderInterfaces[Router.COMMANDER][1])
command.start()

# Set the ip info for the sensor and start it in its own process
sensor.setHostname(sensorInterfaces[Router.SENSORARRAY][0])
sensor.setPort(sensorInterfaces[Router.SENSORARRAY][1])
sensor.start()

# Set the ip info for the planner and start it in its own process
plan.setHostname(plannerInterfaces[Router.PLANNER][0])
plan.setPort(plannerInterfaces[Router.PLANNER][1])
plan.start()

# Set the ip info for the data collector and start it in its own process
dataCollector.setHostname(dataCollectorInterfaces[Router.DATACOLLECTOR][0])
dataCollector.setPort(dataCollectorInterfaces[Router.DATACOLLECTOR][1])
dataCollector.start()


# Set the ip info for the world and start up the graphical interface
W.setHostname(worldInterfaces[Router.WORLD][0])
W.setPort(worldInterfaces[Router.WORLD][1])
W.getChannel().getRouter().createAndInitializeSocket()



W.stepInTime(10,0,1)
W.quit()
