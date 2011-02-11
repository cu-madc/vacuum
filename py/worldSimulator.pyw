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





# Set the rate and size for dirtfall
r = 1.8
s = 12.0

# Set the rate constant and size for rain
v         = .2
cloudsize = 20

# Create the world and get the gridsize
W = GraphicalWorld(r,s,v,cloudsize);
N = W.getNumber() 

# create and set the sensor

sensor = SensorArray(.4,W)
W.setSensor(sensor)

# channel setup
chan = Channel(W);   # TODO register the channel to the world


# create the commander and planner
plan=Planner(r*s/float(N*N),r*s/float(N*N),sensor,W);
chan.setPlanner(plan)
plan.setChannel(chan)
W.setPlanner(plan)
W.setChannel(chan)

command=Commander(chan);
chan.setCommander(command)
sensor.setChannel(chan)
chan.setSensor(sensor)


# Create vacuums
numVacs=3
vacArray = []
for i in range(numVacs) :
    vacuum = Vacuum(i,1.0)
    vacuum.setChannel(chan)
    vacuum.registerWorld(W)
    vacArray.append(vacuum)
    W.addVacuum(vacuum)


command.setNumberVacuums(len(vacArray))


W.mainloop()

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


