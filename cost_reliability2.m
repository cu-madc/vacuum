function C=cost_reliability2(x,W,chan1,chan2,chan3);
% Cost function to evaluate the reliability tradeoff associated with the
% three channels
M=50000;
c1=0;
chan1.reliability=x(1);
chan2.reliability=x(2);
chan3.reliability=max(2-x(1)-x(2),0);
    for j=1:1000; W.inc; end  %transient
    W.expenditure=0;
    for j=1:M;
        W.inc;
        c1=c1+sum(W.A(:));
    end %monte carlo
    C(1)=c1/M;
    C(2)=W.expenditure/M;
    