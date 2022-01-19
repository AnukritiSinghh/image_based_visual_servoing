function Lsd=getinteraction_intensity(s,cam,sd_len,Z,truedepth,Zact)
KK=cam.K;
px = KK(1,1);
py = KK(2,2);
v0=KK(1,3);
u0=KK(2,3);
Zact=([Zact' Zact'])';

if(~truedepth)
    Zarr=Z*ones(sd_len,1);
else
    Zarr=Zact(:);
end
Lsd=zeros(sd_len,6);

for m=1:2:sd_len
    
    
    x = (s(m) - u0)/px ;
    y = (s(m+1) - v0)/py ;
    %Zinv =  1/Z;
    Zinv =  1/Zarr(m);
    
    Lsd(m,1) =  -Zinv;
    Lsd(m,2) =  0;
    Lsd(m,3) =  x*Zinv;
    Lsd(m,4) =  x*y;
    Lsd(m,5) =  -(1+x^2);
    Lsd(m,6) =  y;

    Zinv =  1/Zarr(m+1);
    
    Lsd(m+1,1) =  0;
    Lsd(m+1,2) =  -Zinv;
    Lsd(m+1,3) =  y*Zinv;
    Lsd(m+1,4) = 1+y^2;
    Lsd(m+1,5) = -x*y;
    Lsd(m+1,6)  = -x;
    
    
end

end
