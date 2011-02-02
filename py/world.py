#!/usr/bin/python
#
#  world.py
# 
#   Created on: 1 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the world object used in the vacuum
#       simulation.
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

class  World :  # (handle) :



    def __init__(self,r=1.0,s=1.0,v=1.0,cloudsize=1.0) :

        self.time = 0
    
        self.N=5                   # %size of grid
        self.vacuumArray = []      # array of object handles
        self.sensor = []           # data as recorded on sensor
        self.planner = None        # handle to planning processor
        self.g_handle = None       # handle to worlddraw graph
        self.expenditure = 0.0     # cummulative funds expended since last reset
        self.intializeVariables(r,s,v,cloudsize)

    
    def intializeVariables(self,r,s,v,cloudsize) :
        # initialize the variables this class keeps track of (input rate and size constants)
        self.time=0;
        self.r = r                 # rate constant for - events per unit time(world wide)
        self.s = s                 # size constant for exponential distribution of sizes
        self.v = v                 # rate constant for RAIN events - events per unit
                                   # time (world wide)
        self.cloudsize = cloudsize # average size of rain event

        self.A = zeros(self.N*self.N,dtype=float64)        # array of values for dirt levels
        self.A.reshape(self.N,self.N)
        self.Moisture = zeros(self.N*self.N,dtype=float64) # array of values for moisture level
        self.Moisture.reshape(self.N,self.N)




        
    def clean(self,x,y) :
        # reset location x,y dirt level to 0
        self.A[x,y] = 0.0


    def inc(self) :
        # single time step of simulated world
            
        # dustfall procedure -----
        t=self.time;               # start time
        T=t+1;                     # final time
        tau=-log(random.rand(1)[0])/self.r ; #time until first event
        t=t+tau;
            
        while(t<T) :
            # accumulate dirt until next event falls past final time
            dustball=-log(random.rand(1.0)[0])*self.s; # dustball size
            I=random.randint(self.N**2);               # select site
            self.A[I] = self.A[I]+dustball;            # update the dustlevel
            tau=-log(random.rand(1.0)[0])/self.r ;     # time until next event
            t=t+tau;
            # end dustfall
            
        # drying
        self.Moisture[self.Moisture>0]=self.Moisture[self.Moisture>0]-1;
            
        # rainfall procedure -----
        t=self.time;                           # start time
        tau=-log(random.rand(1.0)[0])/self.v   #time until first event
        t=t+tau

            
        while (t<T) :
            # accumulate dirt until next event falls past final time
            I=random.randint(self.N^2);              #select site
            self.Moisture[I] = self.Moisture[I] + \  #uniform 0# to 200# of average
                               ceil(2*random.rand(1.0)[0]*self.cloudsize); 
            tau=-log(random.rand(1.0)[0])/self.v ;   #time until next event
            t=t+tau;
            # end rainfall
            
            
        self.time=T;

        
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
    world = World()
    world.inc(1)
