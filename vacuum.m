classdef vacuum < handle
    % robot vaccum object
   
    properties
        xPos
        yPos
        timeDone; % time it will be done with current operation
        status; % 1 - moving, 2-cleaning, 3-waiting, 4-repairing
        ghan; % graphics handle
        IDnum;
        commander;
        world;
        time;
        range; %maximum distance that can be travelled 
        queX;
        queY;
        chanComm; %channel to commander
        isWorking;
        timeToClean=8;
        timeToRepair=32;
        odometer=0; %tracks distance travelled
        missions=0; %number of cells than have been cleaned
        moveCost=1;%cost to move
        repairCost=30; %cost to conduct repair
        repairs=0;%number of repairs - running total
        
        
            
    end
   
    methods %setup
        function a=vacuum(IDnum,currentTime)%class constructor
            
            a.xPos=1;
            a.yPos=1;
            a.status=3;
            a.timeDone=currentTime+randi(10);
            a.ghan=[];
            a.IDnum=IDnum;
            a.range=3;
            a.queX=[];
            a.isWorking=true;
        end
        function registerWorld(a,W,command) %make vacuum aware of its world and who is its commander
            a.world=W;
            a.commander=command;
            timeHear= addlistener(W,'time','PostSet',@(src,evnt)timeStep(a,src,evnt));% listen to world time-tick    
        end
        function draw(a) %represent vacuum on a graph
             a.ghan=text(a.xPos,a.yPos,num2str(a.IDnum),'horizontalalignment','center',...
                'fontsize',18,'VerticalAlignment','Middle','backgroundcolor',[.7 .7 .7]);
        end
    end
    
    methods %operational
        
        function move(a,x,y) % allow for movment of vacuum without cleaning
            if ~a.isWorking; return ; end %not functioning
            ordered_distance=abs(a.xPos-x)+abs(a.yPos-y);
            if ordered_distance <= a.range
            a.xPos=x;
            a.yPos=y;
            a.world.expenditure  =a.world.expenditure+a.moveCost; %update funds expended
            a.timeDone=a.timeDone+1;
            a.status=1;
            end
        end        
        function moveandclean(a,x,y) % execute an order to move to new location and clean
            % note - this method will only be called if vacuum is working,
            % so no need to check status
            R=abs(a.xPos-x)+abs(a.yPos-y); % proposed distance to move
            if R <= a.range % move is not too far to achieve
            a.xPos=x;
            a.yPos=y;
            a.odometer=a.odometer+R;
            a.missions=a.missions+1;
            a.world.expenditure  =a.world.expenditure+a.moveCost;
            if a.world.Moisture(x,y)>0 % location is wet
                a.timeDone=a.world.time+a.timeToRepair; % repairs required before cleaning
                a.status=4;
                a.world.expenditure  =a.world.expenditure+a.repairCost;
                a.repairs=a.repairs+1;
            else
                a.timeDone=a.world.time+a.timeToClean;
                a.status=2;
            end
            
            a.queX=[]; % reset que
            end
        end       
           
        function moveord(a,xord,yord) %update que for new location to clean
                       
            a.queX=xord;
            a.queY=yord;
        end
        
        
        function a=timeStep(a,src,evnt) %vacuum action on each world time increment
            if ~a.isWorking; return ; end %not functioning
            
            t=a.world.time; 
            
            if t>=a.timeDone; % Vacuum operation is complete
                if a.status==2; %just finished cleaning
                  a.world.clean(a.xPos,a.yPos); %update world that location has been cleaned
                  a.status=3; %waiting new instruction
                  a.chanComm.send(a.commander,@getReport,a,a.xPos,a.yPos,2);% report that cleaning complete, recieve new instruction
                  %getReport(a.commander,a,a.xPos,a.yPos,2);% report that cleaning complete, recieve new instruction
                elseif a.status==3 && isempty(a.queX); %if nothing in que
                    a.chanComm.send(a.commander,@getReport,a,a.xPos,a.yPos,a.status); %report to commander that vac is waiting
                    %getReport(a.commander,a,a.xPos,a.yPos,a.status); %report to commander that vac is waiting
                elseif a.status==3 % next job is now qued
                    a.moveandclean(a.queX,a.queY);
                elseif a.status==4 %repairs complete
                    a.status=2; %start cleaning sequence
                    a.timeDone=t+a.timeToClean;
                    
                end
            else  % vacuum is still doing something
                if a.status==2 && a.world.Moisture(a.xPos,a.yPos)>0; % region still wet
                    a.timeDone=t+a.timeToClean; %assumes world will dry, then 8 more time units to complete cleaning
                    
                end
                
            end
        end
        
    end
end
            
    
    