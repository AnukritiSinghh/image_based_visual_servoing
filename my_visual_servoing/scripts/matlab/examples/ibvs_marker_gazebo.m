%Barebone IBVS code with colored markers
%each marker has different color
%so color segmentation is used to get the 
clear
clc

% In another terminal run 
% roslaunch visual_servoing main.launch
addpath('../interactions')
addpath('../gazebo_helper')
addpath('../util')

gazebo_handle  = gazebo_init();

Tinit = eye(4);
Tcurr=Tinit;
pause(3)

%desired pose could be given in form of xy coordinates 
%xydes=[200 200; 600 200; 200 600; 600 600]';
%xydes=[560 360; 560 442; 642 360; 642 442]';
xydes=[560 560; 560 642; 642 560; 642 642]';

%Alternatively, desired pose could be given in form of image 
%imgd=imread('desired/??.png');

%Another option is to move the camera to a desired pose and get image.
%Tf = Tinit * [[eul2rotm([0,0,0]) [0.4;0;0]]; 0 0 0 1];
%status = gazebo_movecam(gazebo_handle ,Tf)
%imgd = gazebo_getimage(gazebo_handle);
%status = gazebo_movecam(gazebo_handle ,Tcurr)

%if you give the desired pose as image then you need to extract the
%keypoints.
%xydes = ??

kp_des=xydes(:);

%ibvs tuning parameters
lambda=0.0001;
desired_depth=10;

iter = 1;
while(1)
    img = gazebo_getimage(gazebo_handle);
    pause(0.5);
    xy_curr = (find_centre(img));
    kp_curr=xy_curr(:);
    img1=img;
    %displaying detected centeres
    img = insertShape(img,'FilledCircle',[xy_curr(1,1), xy_curr(2,1), 5],'Color',[1,1,0]);
    img = insertShape(img,'FilledCircle',[xy_curr(1,2), xy_curr(2,2), 5],'Color',[1,1,0]);
    img = insertShape(img,'FilledCircle',[xy_curr(1,3), xy_curr(2,3), 5],'Color',[1,1,0]);
    img = insertShape(img,'FilledCircle',[xy_curr(1,4), xy_curr(2,4), 5],'Color',[1,1,0]);

    %displaying desired centeres
    img = insertShape(img,'FilledCircle',[xydes(1,1), xydes(2,1), 5],'Color',[1,0,0]);
    img = insertShape(img,'FilledCircle',[xydes(1,2), xydes(2,2), 5],'Color',[1,0,0]);
    img = insertShape(img,'FilledCircle',[xydes(1,3), xydes(2,3), 5],'Color',[1,0,0]);
    img = insertShape(img,'FilledCircle',[xydes(1,4), xydes(2,4), 5],'Color',[1,0,0]);

    imshow(img);
    
    
    %getinteraction_intensity(<current keypoints>,<camera.intensic>,<length
    %of featurevector>,<estimate of camera depth if true depth not available>,
    %<flag to use true depth (1) or estmiate(0)>,<true depth of every keypoint>);
    Lsd=getinteraction_point(kp_curr,gazebo_handle.cam,length(kp_curr),desired_depth,0,desired_depth);
    
    error=kp_curr-kp_des;
    vc=-lambda*pinv(Lsd)*error;
    fprintf('error=%.2f, vc=%.2f,%.2f,%.2f,%.2f,%.2f,%.2f\n',norm(error),vc(1),vc(2),vc(3),vc(4),vc(5),vc(6));
    
    %vc= [0.1 0 0 0 0 0];
    if(iter > 200) break; end
    Rotd = eul2rotm([vc(4), vc(5), vc(6)]);%ZYX
    Td = [Rotd [vc(1);vc(2);vc(3)]];
    Tcurr=Tcurr*[Td;0 0 0 1];
    status = gazebo_movecam(gazebo_handle ,Tcurr);
    iter = iter +1;
end
