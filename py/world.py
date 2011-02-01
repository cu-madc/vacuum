classdef world < dynamicprops % dynamicprops is subclass of handle
    % world object - tracks actual state of simulation
    
    properties (SetObservable = true)
        time; % keep track of world time
    end
    
    properties
        N=5; %size of grid
        r; %rate constant for - events per unit time(world wide)
        s; %size constant for exponential distribution of sizes
        v; %rate constant for RAIN events - events per unit time (world wide)
        cloudsize; %average size of rain event
        A; %array of values for dirt levels
        Moisture; %array of values for moisture level
        vacuumArray; %array of object handles
        sensor; % data as recorded on sensor
        planner; % handle to planning processor
        g_handle; %handle to worlddraw graph
        expenditure; %cummulative funds expended since last reset
    end
    
    methods % methods
        function a=world(r,s,v,cloudsize) % constructor (input rate and size constants)
            a.time=0;
            a.r=r;
            a.s=s;
            a.v=v;
            a.cloudsize=cloudsize;
            a.A=zeros(a.N);
            a.Moisture=zeros(a.N);
        end
        
        function clean(a,x,y) % reset location x,y dirt level to 0
            a.A(x,y)=0;
        end
        
        function inc(a) % single time step of simulated world
            
            % dustfall procedure -----
            t=a.time; % start time
            T=t+1; % final time
            tau=-log(rand(1))/a.r ; %time until first event
            t=t+tau;
            
            while t<T % accumulate dirt until next event falls past final time
                dustball=-log(rand(1))*a.s; % dustball size
                I=randi(a.N^2); %select site
                a.A(I)=a.A(I)+dustball;
                tau=-log(rand(1))/a.r ; %time until next event
                t=t+tau;
            end
            % end dustfall
            
            % drying
            a.Moisture(a.Moisture>0)=a.Moisture(a.Moisture>0)-1;
            
             % rainfall procedure -----
            t=a.time; % start time
            tau=-log(rand(1))/a.v ; %time until first event
            t=t+tau;
            
            while t<T % accumulate dirt until next event falls past final time
                I=randi(a.N^2); %select site
                a.Moisture(I)=a.Moisture(I)+ceil(2*rand(1)*a.cloudsize); %uniform 0% to 200% of average
                
                
                tau=-log(rand(1))/a.v ; %time until next event
                t=t+tau;
            end
            % end rainfall
            
            
            a.time=T;
        end
        
        function draw(world) % produce standard three frame graphic
            if isempty(world.g_handle) || ~ishandle(world.g_handle);
                subplot(1,3,1)
                imagesc(world.A')
                vacs=world.vacuumArray;
                for i=1:length(vacs);
                    vacs(i).draw
                end
                set(gca,'Xtick',1:world.N,'Ytick',1:world.N,'color',[0 0 1]);
                gridxy((0:world.N)+.5,(0:world.N)+.5);
                caxis([0 max(max(world.A(:)),max(world.sensor.array(:)))]);
                colorbar
                title(['real   t=',num2str(world.time)]);
                
                subplot(1,3,2)
                imagesc(world.sensor.array')
                vacs=world.vacuumArray;
                for i=1:length(vacs);
                    vacs(i).draw
                end
                
                set(gca,'Xtick',1:world.N,'Ytick',1:world.N,'color',[0 0 1]);
                gridxy((0:world.N)+.5,(0:world.N)+.5);
                caxis([0 max(max(world.A(:)),max(world.sensor.array(:)))]);
                colorbar
                title('sensor')
                
                subplot(1,3,3)
                imagesc(world.planner.worldview')
                vacs=world.vacuumArray;
                for i=1:length(vacs);
                    vacs(i).draw
                end
                set(gca,'Xtick',1:world.N,'Ytick',1:world.N,'color',[0 0 1]);
                gridxy((0:world.N)+.5,(0:world.N)+.5);
                caxis([0 max(max(world.A(:)),max(world.sensor.array(:)))]);
                colorbar
                title('planner')
                colormap('bone');c=colormap;colormap(flipud(c));
                drawnow;
                world.g_handle=gcf;
            else
                
                for i=1:length(world.vacuumArray);
                    v=findobj(world.g_handle,'string',num2str(i)); %handle to vacuum text
                    set(v,'position',[world.vacuumArray(i).xPos world.vacuumArray(i).yPos]);
                    set(v,'backgroundcolor',[.7 .7 .7]+[.3 -.5 -.5]*(world.vacuumArray(i).status==4));
                   
                end
                
                C_des=[0 max(max(world.A(:)),max(world.sensor.array(:)))];
                
                I=findobj(world.g_handle,'type','image'); %Image components
                set(I(4),'CData',world.planner.worldview');
                set(I(5),'CData',world.sensor.array','AlphaData',(world.sensor.Wet'==0));
                set(I(6),'CData',world.A','AlphaData',(world.Moisture'==0));
                
                ax=findobj(world.g_handle,'type','axes');
                for i=4:6;caxis(ax(i),C_des);end
                title(ax(6),['real   t=',num2str(world.time)]);
                drawnow;
            end
            
            
            
        end
    end
    
end