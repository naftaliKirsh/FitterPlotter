function res=circleRes(ed,f,S,normFactor)
    S_no_ed = S.*exp(-1i*ed*normFactor*f);
    a = CircleFitByPratt([real(S_no_ed).' imag(S_no_ed).']);
    res = (real(S_no_ed)-a(1)).^2+(imag(S_no_ed).^2-a(2).^2)-a(3)^2;
end