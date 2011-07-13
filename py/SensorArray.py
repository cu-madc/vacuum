#!/usr/bin/python
#
#  SensorArray.py
# 
#   Created on: 2 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the Sensor Array object.
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
from Router import Router
from Agent import Agent
from XML.XMLMessageForAgent import XMLMessageForAgent


class SensorArray (Agent):

    def __init__(self,accuracy=0.0) :
	Agent.__init__(self,Router.SENSORARRAY)
        # constructor (accuracy of measurement)
        self.accuracy=accuracy-float(int(accuracy))  #force to be within constraints

        self.N = 5
        self.array = zeros((self.N,self.N),dtype=float64) # array of values for dirt levels
        self.Wet = zeros((self.N,self.N),dtype=float64)   # array of values for dirt levels




    def setGridSize(self,N):
	# Routine to set the grid size.
	if(N > self.N) :
	    # Need to add more grids.
	    while(self.N < N) :
		# Add a row and then a column to A and Moisture
		self.array = append(self.array,zeros((1,self.N),dtype=float64),axis=0)
		self.array = append(self.array,zeros((self.N+1,1),dtype=float64),axis=1)

		self.Wet = append(self.Wet,zeros((1,self.N),dtype=float64),axis=0)
		self.Wet = append(self.Wet,zeros((self.N+1,1),dtype=float64),axis=1)
		self.N += 1

	
	elif (N < self.N) :
	    # Need to delete grids
	    while(self.N > N) :
		# Delete a row and then delete a column from A and Moisture
		self.array = delete(self.array,self.N-1,axis=0)
		self.array = delete(self.array,self.N-1,axis=1)

		self.Wet = delete(self.Wet,self.N-1,axis=0)
		self.Wet = delete(self.Wet,self.N-1,axis=1)

		self.N -= 1


    def getArray(self) :
	while(not self.queue.empty()):
	    self.array = self.queue.get()

        return(self.array)

    def setArray(self,value) :
        self.array = value
	#print(self.array)
	if(self.queueUse) :
	    self.queue.put(self.array)

    def getWet(self) :
        return(self.Wet)

    def setWet(self,value) :
        self.Wet = value
	#print(self.Wet)


    
    
    def measure(self) :
        # measure the world and return data

        dirtLevel=None
        wetted=None
        if (self.isWorking):
            #adjust for noise
            #print(self.Wet)
            noisyView =self.array*(
                1.0+2.0*self.accuracy*(random.rand(self.N*self.N).reshape(self.N,self.N)-0.5))
            #print("SensorArray.measure:\n{0}\n{1}\n\n".format(self.array,noisyView))
            self.sendStatusSensor2Planner(noisyView)
         
            self.Wet = self.Wet>0;
            wetted=self.Wet;
	    # TODO - why is this sending the information back to itself???
            # self.channel.sendWorldWetnessToSensor(wetted)

            
            #return([noisyView,wetted])

        return(None)


    # Method to handle an incoming message and determine what to do
    def handleMessage(self,type,passedInformation) :
	#print("Sensor.handleMessage: {0} - {1}".format(type,passedInformation))

	if (type=="Send Planner Update") :
	    self.measure()

	elif (type=="World Wetness") :
	    self.setWet(passedInformation["array"])

	elif (type=="World Status") :
	    self.setArray(passedInformation["array"])



    ## sendStatusSensor2Planner
    #
    # Routine to send a noisy view of the world's grids to the planner
    # from the sensor.
    def sendStatusSensor2Planner(self,noisyView) :
	#print("SensorArray.sendStatusSensor2Planner - sending information")
        sensorData = XMLMessageForAgent()
        sensorData.createRootNode(False)
	sensorData.createObjectClassElements(Agent.PLANNER,"Sensor Status")
	sensorData.addArrayNode(noisyView)
	#print(self.xml2Char())

	self.channel.sendString(Router.PLANNER,sensorData.xml2Char()) #,-1,True)




    # Static method that is used as a helper to make it easier to
    # create a sensor array object.
    @staticmethod
    def spawnSensorArray(accuracy=0.0) :
	sensor = SensorArray(accuracy)
	channel = sensor.initializeChannel()
	#channel.addAgent(sensor,Agent.SENSORARRAY,0,False)
	return(sensor)






if (__name__ =='__main__') :
    # Set the host addresses and ports for the different agents
    agentInterfaces = {Router.SENSORARRAY:['10.0.1.10',10000],
		       Router.PLANNER    :['10.0.1.11',10001],
		       Router.COMMANDER  :['10.0.1.12',10002],
		       Router.WORLD      :['10.0.1.13',10003]}

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


    # create and set the sensor
    accuracy = 0.4
    sensor = SensorArray.spawnSensorArray(accuracy) 
    #print("Sensor Channel: {0}".format(sensor.getChannel()))
    sensor.setIPInformation(agentInterfaces)               # set the agent's ip info on the sensor.
    sensor.getChannel().setNumberVacuums(numVacs)          # tell the sensor how many vac's to use
    sensor.setQueueUse(False)                              # tell the sensor to not use the queue's
                                                           # information to  get input from the world
			  			           # as to what is happening.

    # Create vacuums
    vacArray = []
    for i in range(numVacs) :
	pos = [0,0]                                        # get the default pos.
	# Let the sensor know about this vacuum including it's ip information.
	sensor.setHostInformation(Router.VACUUM,vacummInterfaces[i][0],vacummInterfaces[i][1],i)


    # Set the ip info for the sensor and start it in its own process
    sensor.setHostname(agentInterfaces[Router.SENSORARRAY][0])
    sensor.setPort(agentInterfaces[Router.SENSORARRAY][1])
    sensor.run()
