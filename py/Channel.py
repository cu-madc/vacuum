#!/usr/bin/python
#
#  Channel.py
# 
#   Created on: 2 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the channel object
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

class Channel:
    
    
    
    def __init__(self,world=None) :
        self.world       = world;
        self.setWorking(True)
        self.reliability = 1.0   # Probability of properly transmitting the
                                 # message. Default is full reliability.
        
        self.delay=0;            # default delay

        self.delay = 0.0         # transmission delay - not yet implemented


    def setWorking(self,value) :
        self.isWorking = value

    def getWorking(self) :
        return(self.isWorking)

    def send(self,target,aMethod,varargin) :
        # assumes method is for the world
        
        if self.getWorking() and (self.reliability>random.rand(1)[0]) :
            aMethod(target,varargin)

            

        
    def sendReceive(self,target,returnChannel,aMethod,varargin) :
        # implements methods that also return values via a channel

        varargout = []
        if self.getWorking() and (self.reliability>random.rand(1)[0]) :
            varargout = aMethod(target,varargin)
            if ((not returnChannel.getWorking()) or
                 (returnChannel.reliability<random.rand(1)[0])) :
                 # execute method but don't return result
                 varargout=cell
                 
            else :
                varargout=cell

        return(varargout)
            
