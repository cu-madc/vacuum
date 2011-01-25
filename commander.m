classdef commander < handle
    % command and control object
    
    properties
        isWorking; 
        planner; % handle to the planning processor
        chanPlan; % handle from channel to planner
        chanVac; % array of handles to assigned vacuums
    end
    
    methods  % setup 
        function a=commander(plan) % constructor
            a.isWorking=true;
            a.planner=plan; %handle to planner
        end
        function registerChannels(a,chanPlan,vacArray); % chanVac is an array, one element for each vac
            a.chanPlan=chanPlan;
            B=[];for i=1:length(vacArray);B=[B, vacArray(i).chanComm];end
            a.chanVac=B; %array - one element for each
        end
    end
    
    methods  % operational 
        function getReport(a,aVac,xPos,yPos,status) %receive a report from a vac and take action
            if ~a.isWorking; return ; end %not functioning
            
            
            if status==2; %just completed cleaning
                a.chanPlan.send(a.planner,@receiveReport,xPos,yPos);%update planner status that location is clean
            end
            % get recommended order from the planner
            [xord,yord]=a.chanPlan.sendReceive(a.planner,a.planner.chanComm,@recommendOrder,aVac); % returns empty if comms problem
            if isempty(xord)
                [xord,yord]=a.chanPlan.sendReceive(a.planner,a.planner.chanComm,@recommendOrder,aVac); % retry
            end
            
            
            % pass order to vacuum
            a.chanVac(aVac.IDnum).send(aVac,@moveord,xord,yord);
            %aVac.moveord(xord,yord);
            
            %tell planner that vacuum has been ordered to new location
            if ~isempty(xord)
            a.chanPlan.send(a.planner,@receiveOrder,aVac.IDnum,xord,yord); 
            end
            
        end
    end
    
end