%pure IBVS synthetic code
clear
clc

addpath('../interactions')

cam.K=[800 0 320; 0 800 240; 0 0 1];


%use for simple target
Xc=[-3 -3 100; 3 -3 100; 3 3 100;-3 3 100];


curr_roll=0;
curr_yaw=0;
curr_pitch=0;

%initial target tuned for car
T_OC=[eul2rotm([0,0,0]) [0; 0; 60]]; %rot_ZYX
Tdes_OC=[eul2rotm([0,-13,0]*pi/180) [1; 0; 60]]; %rot_ZYX
cam.T= [(T_OC(1:3,1:3))' -(T_OC(1:3,1:3))'*(T_OC(1:3,4))];
cam_des.T= [(Tdes_OC(1:3,1:3))' -(Tdes_OC(1:3,1:3))'*(Tdes_OC(1:3,4))];


xt_init=cam.K*T_OC(1:3,:)*[Xc';ones(1,size(Xc',2))]; %remember camera center is -R't
xinit=[xt_init(1,:)./xt_init(3,:)];
yinit=[xt_init(2,:)./xt_init(3,:)];
xyinit=([xinit' yinit'])';
kp_init=xyinit(:);


xt_des=cam.K*Tdes_OC(1:3,:)*[Xc';ones(1,size(Xc',2))]; %remember camera center is -R't
xdes=[xt_des(1,:)./xt_des(3,:)];
ydes=[xt_des(2,:)./xt_des(3,:)];


xydes=([xdes' ydes'])';
kp_des=xydes(:);
    
kp_curr=kp_init;
iter=1;

lambda=0.0001;
while(1)
    T_OC_curr=pinv([cam.T;0 0 0 1]);
    xt=cam.K*T_OC_curr(1:3,:)*[Xc';ones(1,size(Xc',2))]; %remember camera center is -R't
    x1=[xt(1,:)./xt(3,:)];
    y1=[xt(2,:)./xt(3,:)];
    xy1=([x1' y1'])';
    kp_curr=xy1(:);
    Z=cam.T(3,4);
    
    %getinteraction_intensity(<current keypoints>,<camera.intensic>,<length
    %of featurevector>,<estimate of camera depth if true depth not available>,
    %<flag to use true depth (1) or estmiate(0)>,<true depth of every keypoint>);
    Lsd=getinteraction_point(kp_curr,cam,length(kp_curr),Z,1,xt(3,:));
    
    error=kp_curr-kp_des;
    vc=-lambda*pinv(Lsd)*error;
    fprintf('error=%.2f, vc=%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n',norm(error),vc(1),vc(2),vc(3),vc(4),vc(5),vc(6));
    clf;
    scatter(xy1(1,:),xy1(2,:),20,'b','filled');
    hold on
    scatter(xydes(1,:),xydes(2,:),20,'r','filled');
    hold off
    axis([0 640 0 480])
    set(gca,'Ydir','reverse')
    pause(0.1);
    
    curr_yaw=curr_yaw+vc(4);
    curr_pitch=curr_pitch+vc(5);    
    curr_roll=curr_roll+vc(6);
    
    Tdiff=[eul2rotm([vc(6),vc(5),vc(4)]) [vc(1); vc(2); vc(3)]]; %rot_ZYX
    
    temp=(([cam.T;[0 0 0 1]])*[Tdiff;[0 0 0 1]]); 
    cam.T(1:3,:)=temp(1:3,:);
    if(norm(error)<1),break;end
    iter=iter+1; 
end
