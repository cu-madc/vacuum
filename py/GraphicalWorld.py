#!/usr/bin/python
#
#  GraphicalWorld.py
# 
#   Created on: 2 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the world object used in the vacuum
#       simulation that implements the graphical view.
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

#import time

from numpy import *
from numpy.linalg import *
from Tkinter import *

from World import World
from WorldView import WorldView
from FalseColor import FalseColor
from Channel import Channel
from Router import Router

class  GraphicalWorld (World,Tk) :

    def __init__(self,r=1.0,s=1.0,v=1.0,cloudsize=1.0) :
        World.__init__(self,r,s,v,cloudsize)
        Tk.__init__(self)
        self.title("World")
        self.iconname("World")
        self.frame = Frame(self)
        self.frame.pack(side=TOP,expand=YES,fill=BOTH)
        self.setupMenu()
        self.setupWindow()
        self.setupOptionsEntry()




    def setupMenu(self) :
        # Add a menu bar that gives the user some basic options.
        self.menuBar = Menu(self)
        self.config(menu=self.menuBar)

        # Add a "file" submenu.
        self.fileMenu = Menu(self.menuBar)
        self.fileMenu.add_command(label="Start",command=self.start)
        self.fileMenu.add_command(label="Quit",command=self.quit)
        self.menuBar.add_cascade(label="File",menu=self.fileMenu)
	self.protocol("WM_DELETE_WINDOW", self.quit)



    def start(self) :
	# Get the parameters from the inputs in the window.
        N = int(self.NValue.get())
        self.r = float(self.rValue.get())
        self.s = float(self.sValue.get())
        self.v = float(self.vValue.get())
        self.cloudSize = float(self.cloudSizeValue.get())

        self.intializeVariables(self.r,self.s,self.v,self.cloudsize)

	from XML.XMLMessageExternalCommand import XMLMessageExternalCommand
	parameter = XMLMessageExternalCommand()
	parameter.setParameterValue(XMLMessageExternalCommand.RESTART)
	parameter.createRootNode()
        for vacuum in self.vacuumArray:
	    # Turn on each of the vacuums - i.e. reset the vacuum.
	    # print("GraphicalWorld.start - Vacuum: {0}".format(vacuum))
            #vacuum.setWorking(True)
            #vacuum.setStatus(3)
            #vacuum.initializeTime(0.0)
	    self.channel.getRouter().sendString(
		Router.VACUUM,parameter.xml2Char(False),vacuum.getID())

        H = []
        R = []
        self.draw()
        skip = 10;
        for i in range(N) :
            #import time # DEBUG
            #time.sleep(1) # DEBUG
            self.inc()
            #if(i%skip==0) :
	    self.draw()

            H.append(sum(sum(self.A)))
            R.append(sum(self.Moisture>0))

	    #self.printVacuumInfo(i)
	    
        print("Mean of H: {0}".format(mean(H)))




    def setupWindow(self) :
        # Define the frame that holds all of the world views.
        self.worldView = Frame(self.frame)
        self.worldView.pack(side=TOP,expand=YES)

        # Define the label that displays the current time step.
        self.timeLabel = Label(self.worldView,text="t=0")
        self.timeLabel.pack(side=TOP,expand=YES)

        # Define the view for the world as seen by the "world" object.
        self.realView = WorldView(self.worldView,self,"Real")
        self.realView.pack(side=LEFT,expand=YES,fill=BOTH)

        # Define the view of the world as seen by the sensor.
        self.sensorView = WorldView(self.worldView,self,"Sensor")
        self.sensorView.pack(side=LEFT,expand=YES,fill=BOTH)

        # Define the view of the world as seen by the planner.
        self.plannerView = WorldView(self.worldView,self,"Planner")
        self.plannerView.pack(side=LEFT,expand=YES,fill=BOTH)

        # Define the legend which displays the values with respect to
        # the color coding.
        legendFrame = Frame(self.worldView)
        legendFrame.pack(side=LEFT,expand=YES)
        Label(legendFrame,text="Legend").pack(side=TOP)
        self.legend = Canvas(legendFrame,width=80,height=200)
        self.legend.pack(side=TOP,expand=YES)
        self.makeLegend(0.0,1.0);


    def setupOptionsEntry(self) :
        # Create the frame that holds the options that can be changed
        # in the graphical view.
        self.entryFrame = Frame(self)
        self.entryFrame.pack(side=TOP,expand=YES)

        # Define the entry for the number of time steps.
        self.NValue = StringVar()
        self.NValue.set("30")
        Label(self.entryFrame,text="N=").pack(side=LEFT,padx=5)
        self.NValueEntry = Entry(self.entryFrame,textvariable=self.NValue,width=7)
        self.NValueEntry.pack(side=LEFT,expand=NO)

        # Define the entry for the value of r
        self.rValue = StringVar()
        self.rValue.set(str(self.r))
        Label(self.entryFrame,text="r=").pack(side=LEFT,padx=5)
        self.rValueEntry = Entry(self.entryFrame,textvariable=self.rValue,width=7)
        self.rValueEntry.pack(side=LEFT,expand=NO)

        # Define the entry for the value of s.
        self.sValue = StringVar()
        self.sValue.set(str(self.s))
        Label(self.entryFrame,text="s=").pack(side=LEFT,padx=5)
        self.sValueEntry = Entry(self.entryFrame,textvariable=self.sValue,width=7)
        self.sValueEntry.pack(side=LEFT,expand=NO)

        # Define the entry for the value of v.
        self.vValue = StringVar()
        self.vValue.set(str(self.v))
        Label(self.entryFrame,text="v=").pack(side=LEFT,padx=5)
        self.vValueEntry = Entry(self.entryFrame,textvariable=self.vValue,width=7)
        self.vValueEntry.pack(side=LEFT,expand=NO)

        # Define the entry for the value of the cloud size.
        self.cloudSizeValue = StringVar()
        self.cloudSizeValue.set(str(self.cloudsize))
        Label(self.entryFrame,text="cloud size=").pack(side=LEFT,padx=5)
        self.cloudSizeValueEntry = Entry(self.entryFrame,textvariable=self.cloudSizeValue,width=7)
        self.cloudSizeValueEntry.pack(side=LEFT,expand=NO)

        # Define the button that will start the simulation when clicked.
        Button(self,text="Start",command=self.start).pack(side=TOP)



    def makeLegend(self,lower,upper) :
        # Routine to show the color scale and associated values that
        # are displayed in the world views.

        # Delete the current view and define the colors to be displayed.
        self.legend.delete(ALL)
        color = FalseColor(lower,upper)
        for scale in range(255) :
            # For each color go through and create a sliver of a
            # rectangle with the given color.
            self.legend.create_rectangle(65,200*scale/255,
                                         80,200*(scale+1)/255.0,
                                         fill=color.calcColor(upper-float(scale)/255.0*(upper-lower)),
                                         outline="")

        # Display the values for the min, max, and middle values.
        self.legend.create_text(30,190,text="{0:8.1E}".format(lower),justify=LEFT)
        self.legend.create_text(30,100,text="{0:8.1E}".format((upper+lower)*0.5),justify=LEFT)
        self.legend.create_text(30, 10,text="{0:8.1E}".format(upper),justify=LEFT)


    def draw(self) :
        # Get the arrays that need to be plotted
	sensor = self.getSensor()
	if(sensor):
	    sensorArray = self.getSensor().getArray()

	planner = self.getPlanner()
	if(planner) :
	    plannerArray = self.getPlanner().getArray()
	
        # Figure out the bounds for the color scale.
	if(planner and sensor) :
	    low  = amin([amin(self.A),amin(sensorArray),amin(plannerArray)])
	    high = amax([amax(self.A),amax(sensorArray),amax(plannerArray)])

	else:
	    low = amin(self.A)
	    high = amax(self.A)

        # Draw each depiction of the world
        self.realView.draw(self.vacuumArray,self.A,[low,high])
	if(sensor):
	    self.sensorView.draw(self.vacuumArray,sensor.getArray(),[low,high])

	if(planner):
	    self.plannerView.draw(self.vacuumArray,plannerArray,[low,high])

        # Update the view of the time and the legend
        self.timeLabel.config(text="t= {0}".format(self.time))
        self.makeLegend(low,high)

        self.update()
        #time.sleep(1.0)


    @staticmethod
    def spawnWorld(r=1.0,s=1.0,v=1.0,cloudsize=1.0) :
	world = GraphicalWorld(r,s,v,cloudsize)
	channel = Channel(world)
	world.setChannel(channel)
	return(world)


if (__name__ =='__main__') :
    world = GraphicalWorld()
    world.inc()
    world.randomDust()
    world.draw()
    world.mainloop()
