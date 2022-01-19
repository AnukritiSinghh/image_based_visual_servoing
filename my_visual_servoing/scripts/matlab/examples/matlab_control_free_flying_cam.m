%Demo code for controlling free flying camera in gazebo using matlab.
clear
clc

% In another terminal run 
% roslaunch visual_servoing main.launch
addpath('../interactions')
addpath('../gazebo_helper')

gazebo_handle  = gazebo_init();

Tinit = eye(4);
Tcurr=Tinit;
pause(3)

iter = 1;
while(1)
    img = gazebo_getimage(gazebo_handle);
    imshow(img);
    pause(0.5);
    vc= [0.1 0 0 0 0 0];
    if(iter > 200) break; end
    Rotd = eul2rotm([vc(4), vc(5), vc(6)]);%ZYX
    Td = [Rotd [vc(1);vc(2);vc(3)]];
    Tcurr=Tcurr*[Td;0 0 0 1]
    status = gazebo_movecam(gazebo_handle ,Tcurr)
    iter = iter +1;
end
