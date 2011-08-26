#!/usr/bin/python
#
#  XMLMessageForAgent.py
# 
#   Created on: 7 July, 2011
#       Author: black
# 
#       Methods for the class that is used to create specific nodes of
#       the xml tree based on what they are supposed to provide.
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

#from xml.dom.minidom import Document
from XMLMessageCreator import XMLMessageCreator

import sys
import os
sys.path.append( os.path.join( os.getcwd(), '..' ) )

from Agent import Agent


class XMLMessageForAgent (XMLMessageCreator) :


    def __init__(self) :
        XMLMessageCreator.__init__(self)


    def __del__(self) :
        pass



    def addPosition(self,posX,posY) :
	self.addNodeWithValue("xPos",posX)
	self.addNodeWithValue("yPos",posY)

    def vacuumID(self,IDnum) :
	self.addNodeWithValue("vacuumID",IDnum)

    def addStatus(self,status):
	self.addNodeWithValue("status",status)

    def addExpenditure(self,expenditure) :
	self.addNodeWithValue("expenditure",str(expenditure))

    def addTime(self,time) :
	self.addNodeWithValue("time",time)

    def addData(self,value) :
	self.addNodeWithValue("data",value)





if (__name__ =='__main__') :
    from XMLParser import XMLParser
    
    IDnum  = 0
    xPos   = 1
    yPos   = 2
    status = 4
    T      = 5

    N = 3;
    A = zeros((N,N),dtype=float64)        # array of values for dirt levels
    for i in range(N) :
        for j in range(N) :
            A[i,j] = i*N+j


    from XMLMessageWorldVacuumCurrentTime import XMLMessageWorldVacuumCurrentTime
    newTime = XMLMessageWorldVacuumCurrentTime(T,A)
    newTime.setVacuumID(IDnum)
    newTime.createRootNode()
    print(newTime.xml2Char(True))


    network = XMLMessageForAgent()
    network.sendVacuumWorldTime(T,IDnum,A)
    print(network.xml2Char(True))

    
#    from XMLIncomingDIF import XMLIncomingDIF
#    dif = XMLIncomingDIF()
#    dif.parseXMLString(network.xml2Char())
#    for dimension in dif:
#	print(dimension)
