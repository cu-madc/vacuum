#!/usr/bin/python
#
#  FalseColor.py
# 
#   Created on: 2 Feb, 2011
#       Author: black
# 
#       class definition for calculating the false color used in a
#       plot.
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


import math
import re


class FalseColor :

    def __init__(self,low=0.0,high=1.0) :
        self.setLow(low);
        self.setHigh(high)

        self.stripHex = re.compile(r'^0x')

    def setLow(self,low) :
        self.low = low

    def setHigh(self,high) :
        self.high = high

    def calcColor(self,value) :
        
        if (value > self.high) :
            angle = 240
        elif (value < self.low) :
            angle = 0.0
        elif (abs(self.high-self.low)< 1.0E-6) :
            angle = 0.0
        else :
            angle = 240.0*(self.high-value)/(self.high-self.low)
            
        if(angle < 60.0) :
            red = 255
            green = int(255.0/60.0*angle+0.5)
            blue = 0

        elif (angle < 120.0) :
            red = int(255.0/60.0*(120.0-angle)+0.5)
            green = 255
            blue = 0

        elif (angle < 180.0) :
            red = 0
            green = 255
            blue = int(255.0/60.0*(angle-120.0)+0.5)

        elif (angle < 240.0) :
            red = 0
            green = int(255.0/60.0*(240.0-angle)+0.5)
            blue = 255

        elif (angle < 300) :
            red = int(255.0/60.0*(angle-240.0)+0.5)
            green = 0
            blue = 255

        else :
            red = 255
            green = 0
            blue = int(255.0/60.0*(360.0-angle)+0.5)

        red   = self.stripHex.sub('',hex(red))
        while(len(red)<2) :
            red = '0' + red
            
        green = self.stripHex.sub('',hex(green))
        while(len(green)<2) :
            green = '0' + green
            
        blue  = self.stripHex.sub('',hex(blue))
        while(len(blue)<2) :
            blue = '0' + blue

        return('#'+red+green+blue)

        

    def calcColorBounds(self,value,low,high) :
        self.setLow(low)
        self.setHigh(high)
        return(self.calcColor(value))
    


    
if (__name__ =='__main__') :
    fc = FalseColor()
    print(fc.calcColorBounds(1.0,0.0,1.0))
    
