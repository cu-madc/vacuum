#!/usr/bin/python
#
#  XMLMessageExternalCommand.py
# 
#   Created on: 31 May, 2011
#       Author: black
# 
#       Methods for the class that keeps track of the information
#       specific to external commands coming from the outside to
#       change execution or request information.
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

from xml.dom.minidom import Document
#from XMLIncomingDIF import XMLIncomingDIF
from XMLMessageCreator import XMLMessageCreator

import sys
import os
sys.path.append( os.path.join( os.getcwd(), '..' ) )
from Agent import Agent

class XMLMessageExternalCommand (XMLMessageCreator) :

    STOP, \
	  START, \
	  RESTART, \
	  RESET, \
	  POLL, \
	  EXIT = range(6)

    ParameterTitles = {STOP:'stop execution', \
                       START:'start execution', \
                       RESTART:'restart execution', \
                       RESET:'reset', \
                       POLL:'poll',
		       EXIT:'exit'}

    def __init__(self) :
	XMLMessageCreator.__init__(self)
	self.setMyInformationType(self.MESSAGE_EXTERNAL_COMMAND);
	self.dimensionsNode = None
	self.objectClassNode = None


        # Initialize the list of parameters that will be defined in
        # this XML tree. This is a list of things that will be
        # defined. Each entry in the list is a list of information
        # used to define a parameter.
        #
        #    An entry in the previous list has the following form:
        #        [parameter type (ex: DUST_RATE), parameter value (ex: 0.2)]
        #
        self.parameterList = []




    def __del__(self) :
        pass


    def setParameterValue(self,type) :

	# Check to see if this parameter has been defined
	for item in self.parameterList:
	    if(item == type) :
		# this parameter has already been defined
		item = type
		return

	# It has not been defined yet. Add it to the list.
        self.parameterList.append(type)




    def createObjectClass(self) :
        # Creates the node that contains the object class definition
        # and all of its children.
	self.createObjectClassElements(Agent.EXTERNAL,"command")


    def createDimensions(self):
        # Creates the dimensions node in the xml tree. It adds the
        # objectClass node as a child of the dimensions node. Finally
        # a "name" node is added as a child of the dimensions node.
	XMLMessageCreator.createDimensions(self)

        for type in self.parameterList:
            if(type in self.ParameterTitles) :
                self.makeNodeSingleValue(self.ParameterTitles[type])









if (__name__ =='__main__') :
    #DUST_RATE, DUST_SIZE, \
	#       RAIN_RATE, RAIN_SIZE, \
	#       GRID_SIZE, \
	#       NUMBER_OF_VACUUMS = range(6)

    parameter = XMLMessageExternalCommand()
    parameter.setParameterValue(XMLMessageExternalCommand.STOP)
    parameter.setParameterValue(XMLMessageExternalCommand.START)
    parameter.setParameterValue(XMLMessageExternalCommand.RESTART)
    parameter.setParameterValue(XMLMessageExternalCommand.RESET)
    parameter.setParameterValue(XMLMessageExternalCommand.POLL)
    print(parameter.parameterList)
    parameter.createRootNode()
    print(parameter.xml2Char(True))


    #print(parameter.xml2Char(True))
    ##root_node = parameter.root_node.cloneNode(True)
    ##parameter.copyXMLTree(root_node)
