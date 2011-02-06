#!/usr/bin/python
#
#  Planner.py
# 
#   Created on: 1 Feb, 2011
#       Author: Skufka - adapted by black
# 
#       class definition for the planner object used in the vacuum
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

class Planner :


    def __init__(self,errGrowth,dirtRate,sensor,world) :
        
        # define the
        #     variance growth parameter,
        #     average dirt fall,
        #     handle to sensor,
        #     handle to array of vacuums)
        N = world.getNumber()
        self.setNumber(N)

        self.worldview = zeros(N*N,dtype=float64);
        self.worldview = self.worldview.reshape(N,N)

        self.wetview = zeros(N*N,dtype=float64);
        self.wetview = self.wetview.reshape(N,N)

        self.viewPrecision = zeros(N*N,dtype=float64);
        self.viewPrecision = self.viewPrecision.reshape(N,N)
        
        self.errGrowth=errGrowth      # estimated growth in variance
        self.dirtRate=dirtRate        #
        
        self.setWorld(world)
        #eventsense = addlistener(sensor,'sense',@(src,evnt)updateView(a,src,evnt)); % triggered by sensor array report
        #timehear = addlistener(self.world,'time','PostSet',@(src,evnt)updateView(a,src,evnt)); % triggered by world time tick
        self.setSensor(sensor)
        self.setChannel(None)

        self.setWorking(True)
        self.vacuumlocation = []
        
        #create distance matrix
        #[self.I,self.J]=ind2sub([self.N self.N],1:(self.N^2));
        ##self.Z=squareform(pdist([I;J]','cityblock')); % replace to allow
        
        #non-stats toolbox commands
        #self.Z=ipdm([I',J'],'metric',1) #'
        #self.wDist=0; %default

    def setNumber(self,value) :
        self.N = value

    def getNumber(self) :
        return(self.N)
    
    def setWorking(self,value) :
        self.isWorking = value

    def getWorking(self) :
        return(self.isWorking)

    def setSensor(self,value) :
        self.sensor = value

    def getSensor(self) :
        return(self.sensor)

    def setWorld(self,value) :
        self.world = value

    def getWorld(self) :
        return(self.world)

    def getWorldView(self) :
        return(self.worldview)

    def getArray(self) :
        return(self.worldview)

    def setChannel(self,value) :
        self.channel = value

    def getChannel(self) :
        return(self.channel)

    def updateView(self,src,evnt) :
        # triggered by world time tick - update planner's view of world
        if not self.getWorking() :
            return

        # update for error growth due to dynamics
        self.viewPrecision=self.viewPrecision/(1+self.errGrowth*self.viewPrecision); 
        mu_0=self.worldview+self.dirtRate;
        tau_0=self.viewPrecision;
            
        # get data from sensor, if available
        levels = self.channel.sendMeasuredFromPlanner2Sensor()
        if(levels) :
            dirtLevel = levels[0]
            wetted    = levels[1]

        else :
            return
            
        # update levels based on sensor information
        if len(dirtLevel) == 0 :
            # no data available  
            self.worldview=mu_0; # adjust dirt ONLY FOR DYNAMICS
        else :
            # data available 
            # bayes update on dirt  
            tau=3./((self.sensor.accuracy**2)*self.sensor.array+1.0);
            mu=dirtLevel;
            self.worldview=(tau_0*mu_0+tau*mu)/(tau_0+tau);
            self.viewPrecision=tau+tau_0;
            self.wetview=wetted;  # when sensor data available, accept as valid


            
    def receiveReport(self,x,y) :
        # update worldview based on report that location was cleaned
        if not self.getWorking() :
            return
            
        self.worldview[x,y]=0;                     # update level
        self.viewPrecision[x,y]=1/self.errGrowth;  # updated modelled error



    def receiveOrder(self,IDnum,x,y) :
        # report of order to a vacuum to clean a location
        # keep updated status on expected vacuum locations
        if not self.getWorking() :
            return
            
        self.vacuumlocation[IDnum,:] = [x,y];



    def recommendOrder(self,id) :
        # decide on recommended order for a vacuum
        if not self.getWorking() :
            return([])

        if(len(self.vacuumlocation)>id) :
            pos = self.vacuumlocation[id]
        else :
            return
            
        A=self.worldview
        x=pos[0]
        y=pos[1]
        
        #s=sub2ind(size(A),x,y); %index of current location
        #ID=aVacuum.IDnum;
#             B=zeros(self.N);%initialize
#             for i=1:self.N; % decide on which locations are within range of vacuum
#                 for j=1:self.N; 
#                     if abs(i-x)+abs(j-y) <=3
#                         B(i,j)=1;
#                     end
#                 end
#             end
#             % value of -1 for dirt level implies location is not viable
#             A(~B)=-1; % out of range locations

        #A(self.Z[s,:]>aVacuum.range)=-1;    # out of range
        A[self.wetview>0] = -1               # exclude wetted locations
        L=self.vacuumlocation;
        #A(sub2ind(size(A),L(:,1),L(:,2)))=-1;% exclude where robot already assigned.
            
        # distance weighting
        #for i in range(len(aVacuum)) :
        #    A[self.Z(s,:)==i]=A[self.Z(s,:)==i]*(1+self.wDist*i);
            
                
        #[~, I]=max(A(:));    #determine viable location with max weight adjusted dirt
        #[xord,yord]=ind2sub(size(A),I);
        xord = x
        yord = y

        self.channel.sendRecommendOrderFromPlanner2Commander(xord,yord)
        return
    
