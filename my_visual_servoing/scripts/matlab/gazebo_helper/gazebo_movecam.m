%vc is with respect to camera frames [x->right y->down and z->into].
%Need to convert it to Gazebo coordinate system.
%Thanks Ayush Gaud for this conversion.
    
function status = gazebo_movecam(handle,Tf)
    angles=rotm2eul(Tf(1:3,1:3));%ZYX
    angles_new = [-angles(2) -angles(1) angles(3)];
    quat = eul2quat(angles_new);
    handle.msg.Pose.Position.Z = -Tf(2,4);
    handle.msg.Pose.Position.X = Tf(3,4);
    handle.msg.Pose.Position.Y = -Tf(1,4);
    handle.msg.Pose.Orientation.W = quat(1);
    handle.msg.Pose.Orientation.X = quat(2);
    handle.msg.Pose.Orientation.Y = quat(3);
    handle.msg.Pose.Orientation.Z = quat(4);
    try
        send(handle.pos_pub,handle.msg);
        status = 0;
    catch
        print('error on publishing pose');
        status = -1;
    pause(0.1);
end