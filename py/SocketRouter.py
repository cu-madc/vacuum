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
            import threading
            import SocketServer
            self.myComm = Comm()

	    
            class MyTCPHandler(SocketServer.BaseRequestHandler):
                # The RequestHandler class for our server.
                # It is instantiated once per connection to the server, and must
                # override the handle() method to implement communication to the
                # client.
                def handle(self):
                    # self.request is the TCP socket connected to the client
                    message = self.server.myParent.myComm.readChunk(self.request)
                    self.server.myParent.receiveXMLReportParseAndDecide(message)
                    #print "Message dispatched!  Length: ",len(message) # DEBUG

		    
            class ThreadedTCPServer(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
                def setParentClass(self,myParent):
                    self.myParent = myParent

            # self.servers = []

            # Create and activate server; will keep running until interrupted by Ctrl-C
            for i in self.SERVERS_DETAILS :
                server = ThreadedTCPServer((i[0], i[1]), MyTCPHandler)
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
            import socket         # import socket network communication library
            self.myComm = Comm()  # instantiate variable-length string generator


            class hostDataClass:
                def __init__(self):
                    Commander2Vacuums = None
                    Commander2Planner = None
                    Planner2Commander = None
                    Vacuums2Commander = None

		    
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

    ## initializeSockets
    #
    # Initialize variables for host tuples and prepare for socket communication
    def initializeSockets(self,Commander2Vacuums=[], Vacuums2Commander=[], 
                          Commander2Planner=None, Planner2Commander=None):
        print "Debug: Initializing host data structure for socket communication." # DEBUG
        #import socket
        self.hosts.Commander2Vacuums = Commander2Vacuums
        self.hosts.Vacuums2Commander = Vacuums2Commander
        self.hosts.Commander2Planner = Commander2Planner
        self.hosts.Planner2Commander = Planner2Commander
    
    ## genHostTuple
    #
    # This function is shorthand for creating host tuples
    def genHostTuple(hostName,hostPort):
        return (hostName,hostPort)


if (__name__ =='__main__') :
    world = World()
    world.inc()

    chan = SocketChannel(world)
 
    # Should add code to then test the communications.
    # Perhaps we could implement a DEBUG type message to send
    # as XML, which doesn't get passed?

    def silly(a, b) :
        print("type: {0}\n{1}".format(type(a),b))

