classdef planner < handle
    % sensor array processor
    
    properties
        N; %gridsize
        worldview;% estimated dirt levels on N x N array
        wetview; % estimated wet/dry condition  (1 - wet, 0 - dry)
        viewPrecision; % array of precision (1/variance) estimates for each location
        vacuumlocation; % #vacs x 2 array of ordered [x,y] locations
        dirtRate; % estimate of amount of dirt falling per square per unit time
        errGrowth; % estimate of error growth
        sensor; % handle to sensor
        chanComm; % handle to channel from planner to commander
        chanSens; % channel planner to sensor
        world;
        isWorking;
        Z; %distance matrix used for determining strategy
        wDist; %distance weighting factor - for use in determining where to assign vacuum
    end
    
    methods %setup
        function a=planner(errGrowth,dirtRate,sensor,Vacs,world) % constructor 
            %(variance growth parameter, average dirt fall,handle to sensor, handle to array of vacuums)
            a.N=world.N;
            a.worldview=zeros(a.N);
            a.wetview=zeros(a.N);
            a.viewPrecision=zeros(a.N);
            a.errGrowth=errGrowth; % estimated growth in variance
            a.dirtRate=dirtRate;
            a.world=world;
            %eventsense = addlistener(sensor,'sense',@(src,evnt)updateView(a,src,evnt)); % triggered by sensor array report
            timehear = addlistener(a.world,'time','PostSet',@(src,evnt)updateView(a,src,evnt)); % triggered by world time tick
            a.sensor=sensor;
            
            for i=1:length(a.world.vacuumArray);
            a.vacuumlocation(i,:)=[Vacs(i).xPos  Vacs(i).yPos];
            end
            a.isWorking=true;
            %create distance matrix
            [I,J]=ind2sub([a.N a.N],1:(a.N^2));
            %a.Z=squareform(pdist([I;J]','cityblock')); % replace to allow
            %non-stats toolbox commands
            a.Z=ipdm([I',J'],'metric',1);
            a.wDist=0; %default
            
        end  
    end
    
    methods %operational
        function updateView(a,src,evnt) % triggered by world time tick - update planner's view of world
            if ~a.isWorking; return ; end %not functioning
                        
            a.viewPrecision=a.viewPrecision./(1+a.errGrowth*a.viewPrecision); % update for error growth due to dynamics
            mu_0=a.worldview+a.dirtRate;
            tau_0=a.viewPrecision;
            
            %get data from sensor, if available
            [dirtLevel,wetted]=a.chanSens.sendReceive(a.sensor,a.sensor.chanPlan,@measure,a.world);
            
             % update levels based on sensor information
             if isempty(dirtLevel); % no data available  
                 a.worldview=mu_0; % adjust dirt ONLY FOR DYNAMICS
             else % data available 
                %bayes update on dirt  
                tau=3./(a.sensor.accuracy^2*a.sensor.array+1);
                mu=dirtLevel;
                a.worldview=(tau_0.*mu_0+tau.*mu)./(tau_0+tau);
                a.viewPrecision=tau+tau_0;
                a.wetview=wetted; %when sensor data available, accept as valid
             end
        end
        function receiveReport(a,x,y) %update worldview based on report that location was cleaned
            if ~a.isWorking; return ; end %not functioning
            
            a.worldview(x,y)=0; %update level
            a.viewPrecision(x,y)=1/a.errGrowth; %updated modelled error
        end       
        function receiveOrder(a,IDnum,x,y) %report of order to a vacuum to clean a location
            %keep updated status on expected vacuum locations
            if ~a.isWorking; return ; end %not functioning
            
            a.vacuumlocation(IDnum,:)=[x y];
        end      
        function [xord,yord]=recommendOrder(a,aVacuum) %decide on recommended order for a vacuum
            if ~a.isWorking; xord=[];yord=[];return ; end %not functioning
            
            A=a.worldview;
            x=aVacuum.xPos;
            y=aVacuum.yPos;
            s=sub2ind(size(A),x,y); %index of current location
            %ID=aVacuum.IDnum;
%             B=zeros(a.N);%initialize
%             for i=1:a.N; % decide on which locations are within range of vacuum
%                 for j=1:a.N; 
%                     if abs(i-x)+abs(j-y) <=3
%                         B(i,j)=1;
%                     end
%                 end
%             end
%             % value of -1 for dirt level implies location is not viable
%             A(~B)=-1; % out of range locations
            A(a.Z(s,:)>aVacuum.range)=-1; %out of range
            A((a.wetview>0))=-1; %exclude wetted locations
            L=a.vacuumlocation;
            A(sub2ind(size(A),L(:,1),L(:,2)))=-1;% exclude where robot already assigned.
            
            %distance weighting
            for i=1:aVacuum.range;
                A(a.Z(s,:)==i)=A(a.Z(s,:)==i)*(1+a.wDist*i);
            end
            
            
            [~, I]=max(A(:)); %determine viable location with max weight adjusted dirt
            [xord,yord]=ind2sub(size(A),I);                
        end              
    end
end