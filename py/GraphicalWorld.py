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


from Tkinter import *

from World import World

class  GraphicalWorld (World,Tk) :

    def __init__(self,r=1.0,s=1.0,v=1.0,cloudsize=1.0) :
        World.__init__(self,r,s,v,cloudsize)
        Tk.__init__(self)
        self.title("World")
        self.iconname("World")
        self.frame = Frame(self)
        self.setupMenu()
        self.setupWindow()


    def setupMenu(self) :
        self.menuBar = Frame(self.frame,relief=RAISED,borderwidth=2)
        self.menuBar.pack(side=TOP,expand=YES)
        pass
        

    def setupWindow(self) :
        self.frame.pack(expand=YES,fill=BOTH)
        self.realFrame = Frame(self.frame,borderwidth=2)
        self.realFrame.pack(side=LEFT,expand=YES,fill=BOTH)
        self.realView = Frame(self.realFrame)
        self.realView.pack(side=LEFT,expand=YES,fill=BOTH)
        self.realLevels = Frame(self.realFrame)
        self.realLevels.pack(side=LEFT,expand=YES,fill=BOTH)
        self.realLabel = Label(self.realView,text="Real")
        self.realLabel.pack(side=TOP)
        self.realCanvas = Canvas(self.realView,width=200,height=200)
        self.realCanvas.pack(side=BOTTOM)
        self.realCanvasLevels = Canvas(self.realLevels,width=20,height=200)
        self.realCanvasLevels.pack(side=BOTTOM)

        self.sensorFrame = Frame(self.frame,borderwidth=2)
        self.sensorFrame.pack(side=LEFT,expand=YES,fill=BOTH)
        self.sensorView = Frame(self.sensorFrame)
        self.sensorView.pack(side=LEFT,expand=YES,fill=BOTH)
        self.sensorLevels = Frame(self.sensorFrame)
        self.sensorLevels.pack(side=LEFT,expand=YES,fill=BOTH)
        self.sensorLabel = Label(self.sensorView,text="Sensor")
        self.sensorLabel.pack(side=TOP)
        self.sensorCanvas = Canvas(self.sensorView,width=200,height=200)
        self.sensorCanvas.pack(side=BOTTOM)
        self.sensorCanvasLevels = Canvas(self.sensorLevels,width=20,height=200)
        self.sensorCanvasLevels.pack(side=BOTTOM)


        self.plannerFrame = Frame(self.frame,borderwidth=2)
        self.plannerFrame.pack(side=LEFT,expand=YES,fill=BOTH)
        self.plannerView = Frame(self.plannerFrame)
        self.plannerView.pack(side=LEFT,expand=YES,fill=BOTH)
        self.plannerLevels = Frame(self.plannerFrame)
        self.plannerLevels.pack(side=LEFT,expand=YES,fill=BOTH)
        self.plannerLabel = Label(self.plannerView,text="Planner")
        self.plannerLabel.pack(side=TOP)
        self.plannerCanvas = Canvas(self.plannerView,width=200,height=200)
        self.plannerCanvas.pack(side=BOTTOM)
        self.plannerCanvasLevels = Canvas(self.plannerLevels,width=20,height=200)
        self.plannerCanvasLevels.pack(side=BOTTOM)



    def draw(self,world) :
        # produce standard three frame graphic
        if isempty(self.g_handle) or ~ishandle(self.g_handle) :
            #subplot(1,3,1)
            #imagesc(self.A') 
            for vacuum in self.vacuumArray :
                vacuum.draw()

            #set(gca,'Xtick',1:self.N,'Ytick',1:self.N,'color',[0 0 1]);
            #gridxy((0:self.N)+.5,(0:self.N)+.5);
            #caxis([0 max(max(self.A(:)),max(self.sensor.array(:)))]);
            #colorbar
            #title(['real   t=',num2str(self.time)]);
                
            #subplot(1,3,2)
            #imagesc(self.sensor.array')  # '
            for vacuum in self.vacuumArray :
                vacuum.draw()

                
            #set(gca,'Xtick',1:self.N,'Ytick',1:self.N,'color',[0 0 1]);
            #gridxy((0:self.N)+.5,(0:self.N)+.5);
            #caxis([0 max(max(self.A(:)),max(self.sensor.array(:)))]);
            #colorbar
            #title('sensor')
                
            #subplot(1,3,3)
            #imagesc(self.planner.worldview') 
            #vacs=self.vacuumArray;
            for vacuum in self.vacuumArray :
                vacuum.draw()

            #set(gca,'Xtick',1:self.N,'Ytick',1:self.N,'color',[0 0 1]);
            #gridxy((0:self.N)+.5,(0:self.N)+.5);
            #caxis([0 max(max(self.A(:)),max(self.sensor.array(:)))]);
            #colorbar
            #title('planner')
            #colormap('bone');c=colormap;colormap(flipud(c));
            #drawnow;
            #self.g_handle=gcf;
            
        else :
                
            for i in range(len(self.vacuumArray)) : 
                v=findobj(self.g_handle,'string',num2str(i)); #handle to vacuum text
                #set(v,'position',[self.vacuumArray(i).xPos self.vacuumArray(i).yPos]);
                #set(v,'backgroundcolor',[.7 .7 .7]+[.3 -.5 -.5]*(self.vacuumArray(i).status==4));
                
            #C_des=[0 max(max(self.A(:)),max(self.sensor.array(:)))];
                
            I=findobj(self.g_handle,'type','image'); #Image components
            #set(I(4),'CData',self.planner.worldview'); # '
            #set(I(5),'CData',self.sensor.array','AlphaData',(self.sensor.Wet'==0)); # '
            #set(I(6),'CData',self.A','AlphaData',(self.Moisture'==0)); # '
                
            ax=findobj(self.g_handle,'type','axes');
            for i in range(4,caxis(ax[i],C_des),6) :
            #    title(ax(6),['real   t=',num2str(self.time)]);
                drawnow;


if (__name__ =='__main__') :
    world = GraphicalWorld()
    world.inc()
    world.mainloop()
