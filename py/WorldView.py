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

from numpy import *
from numpy.linalg import *
from Tkinter import *

from FalseColor import FalseColor

class  WorldView (Frame) :


    def __init__(self,container,parent=None,label="Real") :
        Frame.__init__(self,container,borderwidth=2)

        self.container = container
        self.view = Frame(self)
        self.view.pack(side=LEFT,expand=YES,fill=BOTH)
        self.levels = Frame(self)
        self.levels.pack(side=RIGHT,expand=YES,fill=BOTH)
        self.label = Label(self.view,text=label)
        self.label.pack(side=TOP)
        self.canvas = Canvas(self.view,width=200,height=200)
        self.canvas.pack(side=BOTTOM)
        self.canvasLevels = Canvas(self.levels,width=20,height=200)
        self.canvasLevels.pack(side=BOTTOM)

        self.setParent(parent)



    def setParent(self,parent) :
        self.parent = parent
        


    def draw(self,vacuumArray,levels,limits=False) :
        # produce standard three frame graphic
        self.canvas.delete(ALL)
        dim = levels.shape
        minVal = amin(levels)
        maxVal = amax(levels)
        if(limits) :
            minVal = limits[0]
            maxVal = limits[1]
            
        color = FalseColor(minVal,maxVal)

        for i in range(dim[0]):
            for j in range(dim[1]) :
                self.canvas.create_rectangle(200*i/dim[0],200*j/dim[1],
                                             200*(i+1)/dim[0],200*(j+1)/dim[1],
                                             fill=color.calcColor(levels[i,j]))

        which = 0
        for vacuum in vacuumArray :
            which += 1
            coords = vacuum.getPosition()
            self.canvas.create_text(100/dim[0]+200*(coords[0])/dim[0],
                                    100/dim[1]+200*(coords[1])/dim[1],
                                    text="V"+str(which),
                                    justify=CENTER)


