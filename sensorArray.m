classdef sensorArray < handle
    % sensor array processor
    
    properties
        accuracy; % multiplicative error measure*(1-accuracy) < actual <measured*(1+accuracy)
        % accuracy should be between 0 and 1
        isWorking;
        array; %array of measurements (simultaneous measured values at each location)
        Wet; %array of logicals, indicating location is wet
        chanPlan; % handle to channel to planner
    end
    
    events %sense
        sense; % sensor taking action - triggers action in planner
    end
    
    methods %setup
        function a=sensorArray(accuracy,world)%constructor (accuracy of measurement, world object)
            accuracy=mod(accuracy,1); %force to be within constraints
            a.accuracy=accuracy;
            N=world.N;
            a.array=zeros([N,N]); %initialize
            a.Wet=zeros([N,N]); %initialize
            a.isWorking=true;
            
        end
    end
    
    methods %operational
        function [dirtLevel,wetted]=measure(a,aWorld); %measure the world and return data
            if ~a.isWorking; dirtLevel=[];wetted=[];return ; end %not functioning
            
            actualdata=aWorld.A; %get real world values
            a.array=actualdata.*(1+2*a.accuracy.*(rand(aWorld.N)-.5)); %adjust for noise
            dirtLevel=a.array;
            a.Wet=(aWorld.Moisture>0);
            wetted=a.Wet;
        end
        function arrayOn(a,isStatus) % allows setting status
            a.isWorking=isStatus;
        end               
    end
end