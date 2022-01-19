
function handle = gazebo_init()
try
    rosinit;
end

    handle.pos_pub = rospublisher('/gazebo/set_model_state','gazebo_msgs/ModelState');
    %pos_pub = rospublisher('/gazebo/set_link_state','gazebo_msgs/ModelState');
    handle.msg = rosmessage(handle.pos_pub);
    handle.img_sub = rossubscriber('/rrbot/camera1/image_raw','BufferSize', 1);
    handle.msg.ModelName = 'free_flying_cam';
    handle.msg.ReferenceFrame = 'world';
    handle.cam.K=[476.7030836014194, 0.0, 400.5; 0.0, 476.7030836014194, 400.5; 0.0, 0.0, 1.0];
end
