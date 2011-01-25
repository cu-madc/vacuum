% script to run simulation

clear

numVacs=3;

for i=1:numVacs;vacArray(i)=vacuum(i,1);end


r=.5; s=10; %rate and size for dirtfall
v=.1; cloudsize=20; %rate constant and size for rain

W=world(r,s,v,cloudsize);
N=W.N; %gridsize

W.vacuumArray=vacArray;

sensor=sensorArray(.2,W);
%sensor=sensorArray(.2,W);
W.sensor=sensor;
plan=planner(r*s/N^2,r*s/N^2,sensor,vacArray,W);
W.planner=plan;

command=commander(plan);

for i=1:numVacs;registerWorld(vacArray(i),W,command);end


% channel setup
chan1=channel(W); %TODO register the channel to the world
chan2=channel(W);
chan3=channel(W); 

    %scenario ---  chan1 - wired;  chan2 - wireless; chan3 - satellite
%TODO fix for arbitary number of vacs    

for i=1:numVacs; vacArray(i).chanComm=chan2;end
plan.chanComm=chan1;
command.registerChannels(plan.chanComm, vacArray); 

plan.chanSens=chan3;
sensor.chanPlan=chan3;


  
% create drawing
figure(999);
subplot(1,3,1);colorbar;subplot(1,3,2);colorbar;subplot(1,3,3);colorbar  
draw(W)

%% testing
S=vacArray(1).missions;
S1=vacArray(1).repairs;
tic;
H=zeros(1000,1);R=H;


for i=1:1000;W.inc;H(i)=sum(sum(W.A));R(i)=sum(sum(W.Moisture>0)); end
mean(H)
T_est=1000/(vacArray(1).missions-S)
S1=vacArray(1).repairs-S1;
S=vacArray(1).missions-S;
toc
%%
figure(gcf)
for i=1:30;
    i;
W.inc;
W.draw;
end
W.draw;
%%
W.inc;
W.draw;

%% Test for an optimal weighting

p=linspace(.9,1.3,10);
C=p;%initialize array
H(100000,1)=0; %initialize
tic
for i=1:length(p);
    i
    plan.wDist=p(i);
    for j=1:1000; W.inc; end  %transient
    for j=1:100000;W.inc;H(j)=sum(sum(W.A));end %monte carlo
    C(i)=mean(H);
    toc
end
figure(1);
plot(p,C,'*')

%% make data for a surface;

X1=linspace(.5,.95,19);
X2=X1;

C1=zeros(19,19);
C2=C1;

for i=1:19;
    i
    for j=1:19;
        C=cost_reliability2([X1(i),X2(j)],W,chan1,chan2,chan3);
        C1(i,j)=C(1);
        C2(i,j)=C(2);
    end
end
%%

options = gaoptimset('display','iter','generations',100,'populationsize',30,'TimeLimit',18000,'PlotFcns',@gaplotpareto,...
    'ParetoFraction',0.6);

%options = gaoptimset('display','iter','generations',100,'populationsize',6,'TimeLimit',4000);

objfunc=@(x) cost_reliability2(x,W,chan1,chan2,chan3);

[X,FVAL] = gamultiobj(objfunc,2,[1 1],2,[],[],[.5 .5],[.95 .95],options);


    



