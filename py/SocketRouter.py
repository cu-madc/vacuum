#!/usr/bin/python
#
#  SocketChannel.py
# 
#   Created on: 2 Feb, 2011
#       Author: Skufka - adapted by black - adapted by PW
# 
#       class definition for a super class of the router object using
#       sockets
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
#  ==========================================================================# 
# 
#  Helpful References:
#    http://docs.python.org/library/socketserver.html
# 
#

from Router import Router

from Queue import Queue
from SocketServer import *
import socket
import threading


import re


## SocketChannel
#
# Creates a super class of the router, which is a medium through which
# simulated agents communicate.
#
# This channel uses TCP sockets for communication.
class SocketRouter(Router):

    sendOverTCP = True # Send XML over TCP?  If not, uses local function calls
    sendBackplaneOverTCP = False # Send backplane data over TCP? If not, use local calls
    acceptIncomingConnections = True # Start servers to receive XML over TCP? 
    SERVERS_DETAILS = [("localhost",9999)] # Array of servers to start [(host,port), ...]
    # Each server corresponds to a single simulated agent (commander, planner, etc.)

    def __init__(self,channel) :
	Router.__init__(self,channel)


        if (self.acceptIncomingConnections) :
            from comm import Comm
            self.myComm = Comm()

            # self.servers = []

            # Create and activate server; will keep running until interrupted by Ctrl-C
            for i in self.SERVERS_DETAILS :
                server = ThreadedTCPServer((i[0], i[1]), LocalTCPHandler)
                server.setParentClass(self)
                # Start a thread with the server -- that thread will then start one
                # more thread for each request
                server_thread = threading.Thread(target=server.serve_forever)
                # Exit the server thread when the main thread terminates
                server_thread.setDaemon(True)
                server_thread.start()
                # self.servers.append(server)

        # initialize socket networking functionality, if going to be used
        if(self.sendOverTCP) :
            from comm import Comm    # import our variable-length string library
            self.myComm = Comm()  # instantiate variable-length string generator
            self.hosts = hostDataClass()




    ## sendMessageOverSocket
    #
    # Sends message over TCP socket in our var len string format
    def sendMessageOverSocket(self,hostTuple,message) :
        import socket
        mySocket = socket.socket()
        mySocket.connect((hostTuple[0],hostTuple[1]))
        mySocket.send(self.myComm.makeChunk(message))
        mySocket.close()

    
    ## genHostTuple
    #
    # This function is shorthand for creating host tuples
    def genHostTuple(hostName,hostPort):
        return (hostName,hostPort)




########################################################################
## TCP Handler class
##
## This class handles the tcp requests coming through the threaded
## server class.
class LocalTCPHandler (BaseRequestHandler): 

    #def __init__(self):
    #    #self.incomingTCP = theQueue
    #    pass

    def handle(self) :
	socketInfo = socket.gethostbyaddr(self.client_address[0])
	#if(PollingServer.DEBUG) :
	#	print("Heard from {0}-{1}".format(self.client_address[0],socketInfo[0]))

	message = self.request.recv(PollingServer.POLLING_SERVER_BUFFER_SIZE).strip()
	#message = self.server.myParent.myComm.readChunk(self.request)
	#if(PollingServer.DEBUG) :
	#	print("Confirmed Client: {0}".format(message))
	self.request.send("OK")

	self.server.myParent.dataLock.acquire()
	self.server.myParent.incomingTCP.put(message)

	try:
	    self.server.myParent.dataLock.notify()
        except AttributeError:
	    pass
        self.server.myParent.dataLock.release()



########################################################################
## Threaded Socket Server class
##
## This class keeps track of the incoming messages. It is run as a
## separate thread.
class ThreadedTCPServer (ThreadingMixIn, TCPServer): 


    def __init__(self,connectionInfo,handler,parent) :
	self.setParentClass(parent)
        #ThreadingMixIn.__init__(self)
	if(parent.DEBUG) :
		print("Created the socket server class: {0}".format(connectionInfo))

        TCPServer.__init__(self,connectionInfo,handler)


    def setParentClass(self,myParent):
	self.myParent = myParent




if (__name__ =='__main__') :
    world = World()
    world.inc()

    chan = SocketChannel(world)
 
    # Should add code to then test the communications.
    # Perhaps we could implement a DEBUG type message to send
    # as XML, which doesn't get passed?

    def silly(a, b) :
        print("type: {0}\n{1}".format(type(a),b))

