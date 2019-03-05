clear all; close all;

folder = '\\132.64.80.214\overlordcommon\Measurements\2017.dir\21_11_17 cooldown\Ant\PowerSweep1';

f = importdata(fullfile(folder,'6.25275e9_freq.out'));
d = importdata(fullfile(folder,'6.25275e9_-55.0_data.out'));
S = d(1:2:end-1)+1i*d(2:2:end);
figure; plot(real(S),imag(S),'.'); shg

ang = unwrap(angle(S));

%try a linear fit as an initial guess using first/last 10% of points
numPoints = length(S);
numPoints_10 = floor(numPoints/10);
startIdx = 1:numPoints_10;
[fit_ed_start,gof_start] = fit(f(startIdx)',ang(startIdx)','poly1'); 
endIdx = numPoints-numPoints_10+1:numPoints;
[fit_ed_end,gof_end] = fit(f(endIdx)',ang(endIdx)','poly1');

%choose the better fit as an initial guess
[~,minIdx] = min([gof_start.sse,gof_end.sse]);
p1_vals = [fit_ed_start.p1,fit_ed_end.p1];

options = optimset('Tolfun',1e-15,'MaxFunEvals',1e4,'MaxIter',1e4,'TolX',1e-20);
normFactor = p1_vals(minIdx); %for the parameters to be of order 1
[ed_fitted,resnorm,residual,exitflag,output] = lsqnonlin(@(ed) circleRes(ed,f,S,normFactor),1,...
    [],[],options);

S_no_ed = S.*exp(-1i*ed_fitted*normFactor*f);
figure; plot(real(S_no_ed),imag(S_no_ed),'.'); shg; title('Fit');

S_no_ed2 = S.*exp(-1i*fit_ed_start.p1*f);
figure; plot(real(S_no_ed2),imag(S_no_ed2),'.'); shg; title('Fit start');

S_no_ed3 = S.*exp(-1i*fit_ed_end.p1*f);
figure; plot(real(S_no_ed3),imag(S_no_ed3),'.'); shg; title('Fit end');



