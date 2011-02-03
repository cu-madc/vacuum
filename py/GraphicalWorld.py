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



    def setupMenu(self) :
        self.menuBar = Frame(self.frame,relief=RAISED,borderwidth=2)
        self.menuBar.pack(side=TOP,expand=YES)
        


    def setupWindow(self) :
        self.timeLabel = Label(self.frame,"t=0")
        self.timeLabel.pack(side=TOP,expand=YES)
        
        self.realView = WorldView(self.frame,self,"Real")
        self.realView.pack(side=LEFT,expand=YES,fill=BOTH)

        self.sensorView = WorldView(self.frame,self,"Sensor")
        self.sensorView.pack(side=LEFT,expand=YES,fill=BOTH)

        self.plannerView = WorldView(self.frame,self,"Planner")
        self.plannerView.pack(side=LEFT,expand=YES,fill=BOTH)

        legendFrame = Frame(self.frame)
        legendFrame.pack(side=LEFT,expand=YES)
        Label(legendFrame,text="Legend").pack(side=TOP)
        self.legend = Canvas(legendFrame,width=20,height=200)
        self.legend.pack(side=TOP,expand=YES)
        self.makeLegend(0.0,1.0);


    def makeLegend(self,lower,upper) :
        color = FalseColor(lower,upper)
        for scale in range(255) :
            self.legend.create_rectangle(0,200*scale/255,
                                         20,200*(scale+1)/255,
                                         fill=color.calcColor(float(scale)/255.0),
                                         outline="")


    def draw(self) :
        # Get the arrays that need to be plotted
        sensorArray = self.getSensor().getArray()
        plannerArray = self.getPlanner().getArray()

        # Figure out the bounds for the color scale.
        low  = amin([amin(self.A),amin(sensorArray),amin(plannerArray)])
        high = amax([amax(self.A),amax(sensorArray),amax(plannerArray)])

        # Draw each depiction of the world
        self.realView.draw(self.vacuumArray,self.A,[low,high])
        self.sensorView.draw(self.vacuumArray,self.getSensor().getArray(),[low,high])
        self.plannerView.draw(self.vacuumArray,plannerArray,[low,high])

        self.update()
        #time.sleep(1.0)



if (__name__ =='__main__') :
    world = GraphicalWorld()
    world.inc()
    world.randomDust()
    world.draw()
    world.mainloop()
