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
import errno


import re


## SocketRouter
#
# Creates a super class of the router, which is a medium through which
# simulated agents communicate.
#
# This channel uses TCP sockets for communication.
class SocketRouter(Router):

    acceptIncomingConnections = True # Start servers to receive XML over TCP?

    
    # Each agent has its own router and needs to keep information about its own network information.
    POLLING_SERVER_DEFAULT_PORT=9999
    POLLING_SERVER_BUFFER_SIZE = 4096
    DEBUG = False


    

    def __init__(self,channel,startThread=False,portNumber=POLLING_SERVER_DEFAULT_PORT,hostname='localhost') :
	Router.__init__(self,channel)


        if (SocketRouter.acceptIncomingConnections) :
            from comm import Comm
            self.myComm = Comm()


	self.incomingTCP = Queue()
	
	#  Variables for the state of the polling process
	self.setRunning(startThread)
	self.socketServer = None


	#  Variables used to keep track of the data.
	self.incomingDataList = Queue()
	self.dataLock = threading.Lock()


	#  Initialize the port number to use
	self.setPort(portNumber);
	self.setHostname(hostname) #socket.gethostname())

	if(startThread) :
	    if(SocketRouter.DEBUG) :
		print("Starting socket server")
	    self.createAndInitializeSocket()





    def __del__(self):
       # *********************************************************************
       # * class destructor.
       # ******************************************************************** */

       if(SocketRouter.DEBUG) :
	       print("Shutting down the SocketRouter object.");

       #  Send an empty message to send to the open socket and shut it down.
       self.setRunning(False);
       #XMLSendLocal *mySender = new XMLSendLocal(getPort());
       #mySender->sendNULLXMLTree();
       #delete mySender;

       if self.getRunning() :
	   self.stopServerSocket(-1,False)
	   self.destroyMutex()
	   print("Exiting the thread.")
	   #pthread_exit(None);


       #incomingDataList.clear();





    def createAndInitializeSocket(self) :
	# *********************************************************************
	# Set up and create the socket used for waiting for information.
	# If everything is okay returns zero. Otherwise it returns 1.
	# ******************************************************************** **/

	# Poll the queue periodically
	self.setRunning(True)
	#threading.Timer(1.0, self.checkIncomingQueue).start()
	if(SocketRouter.DEBUG) :
	    print("Timer started for checking the queue")


	# Start the server on a separate thread.
	#handler = LocalTCPHandler(self)
	self.socketServer = ThreadedTCPServer( \
	    (self.getHostname(),self.getPort()),LocalTCPHandler,self)

	self.serverThread = threading.Thread(target=self.socketServer.serve_forever)
	self.serverThread.setDaemon(True)
	self.serverThread.start()
	if(SocketRouter.DEBUG) :
	    print("Started thread: {0} listening on {1}:{2}".format
		  (self.serverThread.getName(),self.getHostname(),self.getPort()))

	    


    def createAndInitializeSocketForever(self) :
	# *********************************************************************
	# Set up and create the socket used for waiting for information.
	# it will loop and wait on the socket "forever."
	# ******************************************************************** **/

	# Poll the queue periodically
	self.setRunning(True)
	if(SocketRouter.DEBUG) :
	    	print("SocketRouter.createAndInitializeSocketForever - creating socket server {0}:{1}".format
		      (self.getHostname(),self.getPort()))


	# Start the server and set the handler.
	self.socketServer = BasicTCPServer( \
	    (self.getHostname(),self.getPort()),LocalTCPHandler,self)
	#print(self.socketServer)

	if(SocketRouter.DEBUG) :
	    print("SocketRouter.createAndInitializeSocketForever Started listener, listening on {0}:{1}".format
		  (self.getHostname(),self.getPort()))


	#self.socketServer.serve_forever()

	while(self.getRunning()) :
	    self.socketServer.handle_request()


	self.socketServer.socket.shutdown(socket.SHUT_RDWR)
	self.socketServer.socket.close()

	#import sys
	#print("exit again")
 	#sys.exit(0)




    def stopServerSocket(self,type,printError=False,debug=False):
	####################################################################
	## stopServerSocket(self,type,printError=False)
	##
	## Stop the existing socket server. 

	self.setRunning(False)
	if(debug) :
	    print("SocketRouter.stopServerSocket: Stopping the server socket: {0}".format(type))

	try:
	    self.socketServer.shutdown(socket.SHUT_RDWR)
	    self.socketServer.close()
	except:
	    if(SocketRouter.DEBUG or printError) :
		print("SocketRouter.stopServerSocket: Error - unable to shut down the socket server.")
	    return(False)

	return(True)




    ####################################################################
    ## checkIncomingQueue(self)
    ##
    ## Routine to check the queue for any completed requests
    def checkIncomingQueue(self,debug=False) :

	if(SocketRouter.DEBUG or debug) :
	    print("checking the incoming queue")

	numberItems = 0
	self.dataLock.acquire()
	entry = None
	while(not self.incomingTCP.empty()):
	    # Something has been passed in from the interwebz
	    entry = self.incomingTCP.get()
	    if(SocketRouter.DEBUG or debug) :
		print("Incoming queue: {0}".format(entry))
	    numberItems += 1
	    self.channel.receiveXMLReportParseAndDecide(entry)



	entry = None

	try:
	    self.dataLock.notify()
	except AttributeError:
	    pass

	self.dataLock.release()

	#if(self.getRunning()) :
	#    threading.Timer(1.0, self.checkIncomingQueue).start()

	return(numberItems);




    def destroyMutex(self) :
	# *********************************************************************
	# Destory the mutex that has been created in the constructor.
	# ******************************************************************** */

	if(self.dataLock) :
	    self.dataLock.release();
	    self.dataLock = None




    ## sendMessageOverSocket
    #
    # Sends message over TCP socket in our var len string format
    def sendMessageOverSocket(self,hostTuple,message) :
	if(SocketRouter.DEBUG) :
	    print("SocketRouter.sendMessageOverSocket, {1}, {2} - sending:\n{0}".format(
		"",hostTuple[0],hostTuple[1])) # message
	    
        import socket
        mySocket = socket.socket()
        try:
            mySocket.connect((hostTuple[0],hostTuple[1]))
            mySocket.send(message) #self.myComm.makeChunk(message))

        except EnvironmentError as exc:
            if(exc.errno == errno.ECONNREFUSED):
                print("SocketRouter.sendMessageOverSocket - Error trying to connect - {0}:{1}".format(
		    hostTuple[0],hostTuple[1]))
	    else :
		print("SocketRouter.sendMessageOverSocket - Unkown error trying to connect: {0}".format(exc.errno))
                
        mySocket.close()

    


    def setRunning(self,value) :
	#  Sets the value of the running variable.
	self.keepCheckingQueue = value


    def getRunning(self) :
	#  Returns the value of the running variable.
	return (self.keepCheckingQueue);


    def setPort(self,value) :
	# Sets the value of the port to use for the socket
	#print("Router - setting port: {0}".format(value))
	self.serverPort = value;


    def getPort(self) :
	# Returns the value of the port used for the socket
	return(self.serverPort);


    def setHostname(self,value) :
	# Sets the value of the port to use for the socket
	#print("Router - setting address: {0}".format(value))
	self.hostname = value;


    def getHostname(self) :
	# Returns the value of the port used for the socket
	return(self.hostname);



    def printThisHostInformation(self) :
	print("Host: {0} Port: {1}".format(self.hostname,self.serverPort))



########################################################################
## TCP Handler class
##
## This class handles the tcp requests coming through the threaded
## server class.
class LocalTCPHandler (BaseRequestHandler): 

    DEBUG = False
    
    #def __init__(self,parent):
    #	BaseRequestHandler.__init__(self)
    #    #self.incomingTCP = theQueue
    #	self.parent = parent

    def handle(self) :
	try:
	    socketInfo = socket.gethostbyaddr(self.client_address[0])
	except:
	    socketInfo = self.client_address[0]
	    
	if(LocalTCPHandler.DEBUG) :
		print("Heard from {0}".format(socketInfo))

	message = self.request.recv(SocketRouter.POLLING_SERVER_BUFFER_SIZE).strip()
	#message = self.server.myParent.myComm.readChunk(self.request)
	
	#if(LocalTCPHandler.DEBUG) :
	#     print("Confirmed Client: {0}".format(message))
		
	self.request.send("OK")
	#self.server.stopServerSocket()
	#print(self.server)
	#self.server.shutdown()


	self.finish()


	if(self.server.threaded):
	    #print("Lock requested: {0}".format(self.server.myParent))
	    self.server.myParent.dataLock.acquire()
	    self.server.myParent.incomingTCP.put(message)

	    try:
		self.server.myParent.dataLock.notify()
	    except AttributeError:
		pass
	    self.server.myParent.dataLock.release()
	    #print("Lock released:  {0}".format(self.server.myParent))

	else:
	    # This is a request that is coming into a blocking tcp server.
	    self.server.myParent.channel.receiveXMLReportParseAndDecide(message)
		



########################################################################
## Threaded Socket Server class
##
## This class keeps track of the incoming messages. It is run as a
## separate thread.
class ThreadedTCPServer (ThreadingMixIn, TCPServer): 

    DEBUG = False

    def __init__(self,connectionInfo,handler,parent) :
	self.setParentClass(parent)
        #ThreadingMixIn.__init__(self)
	if(ThreadedTCPServer.DEBUG) :
		print("Created the threaded socket server class: {0}".format(connectionInfo))

        TCPServer.__init__(self,connectionInfo,handler)
	self.threaded = True


    def setParentClass(self,myParent):
	self.myParent = myParent



########################################################################
## Basic Socket Server class
##
## This class keeps track of the incoming messages. It is a blocking
## server.
class BasicTCPServer (TCPServer): 

    DEBUG = False

    def __init__(self,connectionInfo,handler,parent) :
	self.setParentClass(parent)
        #ThreadingMixIn.__init__(self)
	if(BasicTCPServer.DEBUG) :
		print("Created the basic socket server class: {0}".format(connectionInfo))

        TCPServer.__init__(self,connectionInfo,handler)
	self.threaded = False


    def setParentClass(self,myParent):
	self.myParent = myParent




if (__name__ =='__main__') :
    import time
    import sys

    if (len(sys.argv)==1) :
	    sys.argv.append("client")

    if (sys.argv[1]=="server") :
	print("testing")

	if(not True) :
	    polling = SocketRouter(None,True)
	    steps = 4
	    while(steps>0) :
		time.sleep(4.0)
		steps -= 1
		print("Waiting Step {0}".format(10-steps))
	    polling.setRunning(False)

	else :
	    polling = SocketRouter(None,False,SocketRouter.POLLING_SERVER_DEFAULT_PORT,'10.0.1.18')
	    try:
		#polling.checkIncomingQueue()
		polling.createAndInitializeSocketForever()

	    except KeyboardInterrupt:
		print("Stopping the server socket.")
		polling.stopServerSocket(-1,False)

    else :
	print("client")
	HOST, PORT = "10.0.1.18", SocketRouter.POLLING_SERVER_DEFAULT_PORT
	data = "This is a test bubba" 

	# Create a socket (SOCK_STREAM means a TCP socket)
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

	# Connect to server and send data
	sock.connect((HOST, PORT))
	sock.send(data + "\n")

	# Receive data from the server and shut down
	received = sock.recv(1024)
	sock.shutdown(socket.SHUT_RDWR)
	sock.close()

	print("Sent:     {0}".format(data))
	print("Received: {0}".format(received))

