 classdef channel < handle
    % channel object
    
    properties
        isWorking; %logical
        reliability; %probability of properly transmitting the message
        delay; %transmission delay - not yet implemented
        world; %handle to world object
    end
    
    methods
        function aChannel=channel(world) % constructor 
            aChannel.world=world;
            aChannel.isWorking=1;
            aChannel.reliability=1; % default is full reliability
            aChannel.delay=0; %default delay
        end  
        function send(aChannel,target,aMethod,varargin)
            % aMethod should be a function handle
            %assumes method is for the world
            if aChannel.isWorking && (aChannel.reliability>rand(1));
                aMethod(target,varargin{:})
            end
            
        end
        
        function varargout=sendReceive(aChannel,target,returnChannel,aMethod,varargin)
            % implements methods that also return values via a channel
            
                                    
            if aChannel.isWorking && (aChannel.reliability>rand(1));
                [varargout{1:nargout}]=aMethod(target,varargin{:}); 
                if ~returnChannel.isWorking || (returnChannel.reliability<rand(1));%execute method but don't return result
                    varargout=cell(1:nargout);
                end
            else
                 varargout=cell(1:nargout);
            end
        end
            
    end
end